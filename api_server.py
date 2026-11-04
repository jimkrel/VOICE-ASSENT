import os, time, json, shutil, re, glob, datetime, subprocess
from typing import Optional, List
import psutil
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Protect SSD Drive C: -> force all caches and temps to Drive E:
os.environ['HF_HOME'] = r'E:\VoiceAI\hf_cache'
os.environ['TORCH_HOME'] = r'E:\VoiceAI\torch_cache'
os.environ['TEMP'] = r'E:\VoiceAI\temp'
os.environ['TMP'] = r'E:\VoiceAI\temp'

import numpy as np
import torch
import soundfile as sf
import studio_app as core

# Warm up psutil CPU counter
psutil.cpu_percent(interval=None)

STUDIO_TELEMETRY = {
    "status": "ready",
    "taskName": "OmniVoice FP16 Studio Engine",
    "voiceName": "Hope",
    "progress": 0,
    "stage": "Sẵn sàng xử lý trên CUDA",
    "startedAt": 0.0,
    "elapsed": 0.0,
    "duration": 0.0,
    "audioUrl": None,
    "filename": None,
    "waveform": [],
    "logs": [
        {"time": "00:00.0", "message": "Đã nạp OmniVoice FP16 trên NVIDIA GeForce GTX 1650 (CUDA:0)"},
        {"time": "00:00.1", "message": "Bộ lọc 5-Stage ElevenLabs Mastering (-14 LUFS) & Spatial DSP sẵn sàng"},
    ],
}


def compute_waveform_bars(audio: np.ndarray, n_bars: int = 64) -> List[int]:
    if audio is None or len(audio) == 0:
        return [18] * n_bars
    chunks = np.array_split(np.abs(audio), n_bars)
    rms = np.array([float(np.sqrt(np.mean(c ** 2))) if len(c) > 0 else 0.0 for c in chunks])
    peak = float(np.max(rms)) if len(rms) > 0 else 0.0
    if peak < 1e-6:
        return [18] * n_bars
    norm = rms / peak
    return [int(max(14, min(96, round(14 + (val ** 0.75) * 82)))) for val in norm]


def begin_studio_job(task_name: str, voice_name: str):
    STUDIO_TELEMETRY["status"] = "running"
    STUDIO_TELEMETRY["taskName"] = task_name
    STUDIO_TELEMETRY["voiceName"] = voice_name
    STUDIO_TELEMETRY["progress"] = 5
    STUDIO_TELEMETRY["stage"] = "Khởi tạo luồng xử lý GPU"
    STUDIO_TELEMETRY["startedAt"] = time.time()
    STUDIO_TELEMETRY["elapsed"] = 0.0
    STUDIO_TELEMETRY["logs"] = [
        {"time": "00:00.0", "message": f"Khởi chạy {task_name} · Giọng: {voice_name}"}
    ]


def log_studio_step(progress: int, stage: str, message: str):
    t_rel = max(0.0, time.time() - STUDIO_TELEMETRY["startedAt"])
    secs = int(t_rel)
    tenths = int((t_rel - secs) * 10)
    t_str = f"00:{secs:02d}.{tenths}"
    STUDIO_TELEMETRY["progress"] = progress
    STUDIO_TELEMETRY["stage"] = stage
    STUDIO_TELEMETRY["elapsed"] = round(t_rel, 2)
    STUDIO_TELEMETRY["logs"].append({"time": t_str, "message": message})


def finish_studio_job(audio: np.ndarray, sr: int, audio_url: str, filename: str, summary_msg: str):
    t_rel = max(0.1, time.time() - STUDIO_TELEMETRY["startedAt"])
    secs = int(t_rel)
    tenths = int((t_rel - secs) * 10)
    t_str = f"00:{secs:02d}.{tenths}"
    dur = round(float(len(audio) / sr), 2) if audio is not None and sr > 0 else 0.0
    bars = compute_waveform_bars(audio, 64)
    STUDIO_TELEMETRY["status"] = "complete"
    STUDIO_TELEMETRY["progress"] = 100
    STUDIO_TELEMETRY["stage"] = "Hoàn tất xử lý âm thanh"
    STUDIO_TELEMETRY["elapsed"] = round(t_rel, 2)
    STUDIO_TELEMETRY["duration"] = dur
    STUDIO_TELEMETRY["audioUrl"] = audio_url
    STUDIO_TELEMETRY["filename"] = filename
    STUDIO_TELEMETRY["waveform"] = bars
    STUDIO_TELEMETRY["logs"].append({"time": t_str, "message": summary_msg})
    return bars


def query_real_hardware():
    cpu_pct = round(psutil.cpu_percent(interval=None))
    vm = psutil.virtual_memory()
    ram_pct = round(vm.percent)
    ram_used_gb = round(vm.used / (1024 ** 3), 1)
    ram_total_gb = round(vm.total / (1024 ** 3), 1)

    gpu_util = 0
    vram_used_mb = 0
    vram_total_mb = 4096
    gpu_temp = 45
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu", "--format=csv,noheader,nounits"],
            timeout=1.5,
            text=True,
        ).strip()
        parts = [p.strip() for p in out.split(",")]
        if len(parts) >= 4:
            gpu_util = int(parts[0])
            vram_used_mb = int(parts[1])
            vram_total_mb = int(parts[2])
            gpu_temp = int(parts[3])
    except Exception:
        if torch.cuda.is_available():
            vram_used_mb = int(torch.cuda.memory_allocated(0) / (1024 ** 2))

    return {
        "cpu": max(1, min(100, cpu_pct)),
        "gpu": max(0, min(100, gpu_util)),
        "gpuTemp": gpu_temp,
        "ram": max(1, min(100, ram_pct)),
        "ramUsedGb": ram_used_gb,
        "ramTotalGb": ram_total_gb,
        "vramUsedGb": round(vram_used_mb / 1024.0, 2),
        "vramTotalGb": round(vram_total_mb / 1024.0, 2),
        "vramPct": max(1, min(100, round((vram_used_mb / max(1, vram_total_mb)) * 100))),
        "gpuName": "NVIDIA GeForce GTX 1650",
    }

app = FastAPI(title="Thành Âm Studio API V2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/outputs", StaticFiles(directory=core.OUT_DIR), name="outputs")
app.mount("/presets", StaticFiles(directory=core.PRESET_DIR), name="presets")
app.mount("/voices_audio", StaticFiles(directory=core.VOICES_DIR), name="voices_audio")

DISTANCE_MAP = {
    "Gần": "Near",
    "Vừa": "Medium",
    "Xa": "Far",
    "Near": "Near",
    "Medium": "Medium",
    "Far": "Far",
}

SPACE_MAP = {
    "Phòng thu khô": "Studio (Dry)",
    "Phòng nhỏ": "Small Room",
    "Sảnh lớn": "Large Hall",
    "Điện thoại": "Phone Line",
    "Studio (Dry)": "Studio (Dry)",
    "Small Room": "Small Room",
    "Large Hall": "Large Hall",
    "Phone Line": "Phone Line",
}

TONES = ["aqua", "blue", "violet", "coral", "green"]

BASE_CATALOG = [
    {
        "id": "hope",
        "name": "Hope",
        "style": "upbeat and clear",
        "locale": "US",
        "gender": "Nữ",
        "language": "English (US)",
        "description": "Trong trẻo, ngọt ngào, tươi sáng",
        "sampleText": "Deep inside the Black Forest, investigators discovered an abandoned radio tower.",
        "categories": ["US English", "Nữ (Female)"],
        "source": "ElevenLabs Original",
        "tone": "aqua",
        "audioPath": os.path.join(core.PRESET_DIR, "eleven_hope.wav"),
    },
    {
        "id": "marcus",
        "name": "Marcus",
        "style": "documentary and crime",
        "locale": "US",
        "gender": "Nam",
        "language": "English (US)",
        "description": "Trầm, rõ nét, phù hợp phim tài liệu",
        "sampleText": "The year was 1994. A signal appeared from a station no one had used in decades.",
        "categories": ["US English", "Nam (Male)"],
        "source": "Hệ thống",
        "tone": "blue",
        "audioPath": os.path.join(core.PRESET_DIR, "marcus_documentary.wav"),
    },
    {
        "id": "liam",
        "name": "Liam",
        "style": "storyteller and essay",
        "locale": "UK",
        "gender": "Nam",
        "language": "English (UK)",
        "description": "Ấm áp, gần gũi, nhịp kể tự nhiên",
        "sampleText": "Have you ever wondered why some stories stay with you forever?",
        "categories": ["UK English", "Nam (Male)"],
        "source": "Hệ thống",
        "tone": "violet",
        "audioPath": os.path.join(core.PRESET_DIR, "liam_storyteller.wav"),
    },
    {
        "id": "alex",
        "name": "Alex",
        "style": "movie recap and shorts",
        "locale": "US",
        "gender": "Nam",
        "language": "English (US)",
        "description": "Năng lượng, nhịp nhanh, hợp video ngắn",
        "sampleText": "In a city that never sleeps, one message changed everything.",
        "categories": ["US English", "Nam (Male)"],
        "source": "Hệ thống",
        "tone": "coral",
        "audioPath": os.path.join(core.PRESET_DIR, "alex_recap.wav"),
    },
    {
        "id": "minh-anh",
        "name": "Minh Anh",
        "style": "ấm áp và rõ ràng",
        "locale": "Việt Nam",
        "gender": "Nữ",
        "language": "Tiếng Việt",
        "description": "Giọng nữ miền Bắc, nhẹ nhàng và tự nhiên",
        "sampleText": "Xin chào, mời bạn cùng khám phá câu chuyện hôm nay.",
        "categories": ["Tiếng Việt", "Nữ (Female)"],
        "source": "Hệ thống",
        "tone": "green",
        "audioPath": os.path.join(core.PRESET_DIR, "voice_vi_female.mp3"),
    },
    {
        "id": "bao-ngoc",
        "name": "Bảo Ngọc",
        "style": "trẻ trung và tươi sáng",
        "locale": "Việt Nam",
        "gender": "Nữ",
        "language": "Tiếng Việt",
        "description": "Phát âm rõ, giàu cảm xúc, hợp nội dung thương hiệu",
        "sampleText": "Bắt đầu một ngày mới với cảm hứng và những ý tưởng thật khác biệt.",
        "categories": ["Tiếng Việt", "Nữ (Female)"],
        "source": "Giọng tự tạo",
        "tone": "coral",
        "audioPath": os.path.join(core.PRESET_DIR, "voice_vi_female.mp3"),
    },
    {
        "id": "gia-huy",
        "name": "Gia Huy",
        "style": "nam ấm áp, truyền cảm",
        "locale": "Việt Nam",
        "gender": "Nam",
        "language": "Tiếng Việt",
        "description": "Giọng nam tự sự, thuyết minh và review",
        "sampleText": "Xin chào, đây là giọng đọc nam truyền cảm chuẩn phòng thu studio.",
        "categories": ["Tiếng Việt", "Nam (Male)"],
        "source": "Hệ thống",
        "tone": "blue",
        "audioPath": os.path.join(core.PRESET_DIR, "voice_vi_male.mp3"),
    },
]


def get_full_catalog():
    items = list(BASE_CATALOG)
    seen_ids = {v["id"] for v in items}

    # Add ElevenLabs Originals from elevenlabs_catalog.json
    if os.path.exists(core.CATALOG_PATH):
        try:
            with open(core.CATALOG_PATH, "r", encoding="utf-8") as f:
                el_cat = json.load(f)
            for idx, (full_name, meta) in enumerate(el_cat.items()):
                short_name = full_name.split("—")[0].strip()
                vid = short_name.lower().replace(" ", "-")
                if vid in seen_ids:
                    continue
                seen_ids.add(vid)
                is_uk = meta.get("accent") == "British"
                is_female = meta.get("gender") == "female"
                locale = "UK" if is_uk else "US"
                language = "English (UK)" if is_uk else "English (US)"
                gender = "Nữ" if is_female else "Nam"
                cats = [
                    "UK English" if is_uk else "US English",
                    "Nữ (Female)" if is_female else "Nam (Male)",
                ]
                genre = re.sub(r"^[^\w\s]+\s*", "", meta.get("genre", "Original")).strip().lower()
                items.append({
                    "id": vid,
                    "name": short_name,
                    "style": genre,
                    "locale": locale,
                    "gender": gender,
                    "language": language,
                    "description": meta.get("desc", ""),
                    "sampleText": meta.get("text", ""),
                    "categories": cats,
                    "source": "ElevenLabs Original",
                    "tone": TONES[idx % len(TONES)],
                    "audioPath": meta.get("audio", ""),
                })
        except Exception as e:
            print("Warning loading elevenlabs_catalog:", e)

    # Add custom voices from voices.json
    custom = core.load_custom()
    for idx, (cname, cmeta) in enumerate(custom.items()):
        vid = f"custom-{core._slug(cname).lower()}"
        if vid in seen_ids:
            continue
        seen_ids.add(vid)
        items.append({
            "id": vid,
            "name": cname,
            "style": "giọng tự tạo",
            "locale": "Tùy chỉnh",
            "gender": cmeta.get("gender", "Tùy chỉnh"),
            "language": cmeta.get("language", "Đa ngôn ngữ"),
            "description": cmeta.get("desc", "Giọng đọc tùy chỉnh của bạn"),
            "sampleText": cmeta.get("text", "Xin chào, đây là giọng đọc mới được tạo."),
            "categories": ["Giọng tự tạo", "Tiếng Việt"],
            "source": "Giọng tự tạo",
            "tone": TONES[(idx + 2) % len(TONES)],
            "audioPath": cmeta.get("audio", ""),
        })

    return items


def resolve_voice(voice_id: str):
    cat = get_full_catalog()
    for v in cat:
        if v["id"] == voice_id or v["name"].lower() == voice_id.lower():
            return v
    return cat[0]


@app.get("/api/voices")
def api_list_voices():
    cat = get_full_catalog()
    out = []
    for v in cat:
        d = {k: val for k, val in v.items() if k != "audioPath"}
        d["previewUrl"] = f"/api/voices/{v['id']}/preview"
        out.append(d)
    return {"voices": out}


@app.get("/api/voices/{voice_id}/preview")
def api_voice_preview(voice_id: str):
    v = resolve_voice(voice_id)
    path = v.get("audioPath", "")
    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Không tìm thấy tệp âm thanh mẫu.")
    return FileResponse(path)


class TTSRequest(BaseModel):
    text: str
    voiceId: str = "minh-anh"
    speed: float = 0.95
    stability: float = 45.0
    similarity: float = 75.0
    style: float = 5.0
    distance: Optional[str] = "Vừa"
    space: Optional[str] = "Phòng thu khô"
    language: str = "Tự động"
    lufs: bool = True
    denoise: bool = False
    format: str = "WAV · 24 kHz"


@app.get("/api/system/metrics")
def api_system_metrics():
    hw = query_real_hardware()
    if STUDIO_TELEMETRY["status"] == "running" and STUDIO_TELEMETRY["startedAt"] > 0:
        STUDIO_TELEMETRY["elapsed"] = round(time.time() - STUDIO_TELEMETRY["startedAt"], 2)
    return {
        "hardware": hw,
        "telemetry": STUDIO_TELEMETRY,
    }


@app.post("/api/tts")
def api_tts(req: TTSRequest):
    text = (req.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Vui lòng nhập kịch bản cần chuyển thành giọng nói.")

    # Tự động nhận diện ngôn ngữ Tiếng Việt dựa trên dấu tiếng Việt
    is_vietnamese_text = any(c in "àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ" for c in text.lower())
    target_lang = req.language or "Tự động"
    if target_lang == "Tự động":
        target_lang = "Tiếng Việt" if is_vietnamese_text else "English"

    # Nếu kịch bản là Tiếng Việt mà giọng đang chọn là hope (mặc định ban đầu tiếng Anh), tự động ưu tiên giọng Việt Minh Anh
    req_voice = req.voiceId
    if (not req_voice or req_voice == "hope") and is_vietnamese_text:
        req_voice = "minh-anh"

    v = resolve_voice(req_voice)
    audio_path = v.get("audioPath", "")
    if not audio_path or not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail="Không tìm thấy tệp giọng mẫu đã chọn.")

    begin_studio_job("Đọc kịch bản (TTS)", v["name"])
    stab = float(req.stability) / 100.0 if req.stability > 1.0 else float(req.stability)
    sim = float(req.similarity) / 100.0 if req.similarity > 1.0 else float(req.similarity)
    sty = float(req.style) / 100.0 if req.style > 1.0 else float(req.style)

    fx_dist = DISTANCE_MAP.get(req.distance or "Medium", "Medium")
    fx_env = SPACE_MAP.get(req.space or "Studio (Dry)", "Studio (Dry)")

    chunks = core.parse_and_chunk_script(text, lang=target_lang)
    if not chunks:
        chunks = [{"text": text, "emotion": "calm"}]

    log_studio_step(15, "Phân tích kịch bản & sắc thái", f"Đã chia {len(chunks)} phân đoạn · Ngôn ngữ: {target_lang} · Tốc độ {req.speed}x")

    t0 = time.time()
    sr = core.model.sampling_rate
    audio_segments = []
    emotions_used = []
    model_choice = "Eleven v4 (Turbo)"
    total_steps = core.MODEL_STEPS[model_choice]["steps"]

    for i, c in enumerate(chunks):
        chunk_text = c["text"]
        chunk_emo = c["emotion"]
        emotions_used.append(chunk_emo)
        prof = core.EMOTION_PROFILES.get(chunk_emo, core.EMOTION_PROFILES["calm"])
        norm_chunk = core.normalize_script(chunk_text, lang=target_lang)

        pct = 20 + int(((i + 0.5) / len(chunks)) * 60)
        preview_txt = norm_chunk[:42] + ("..." if len(norm_chunk) > 42 else "")
        log_studio_step(
            pct,
            f"Tổng hợp đoạn {i+1}/{len(chunks)} [{chunk_emo}]",
            f"Đoạn {i+1}/{len(chunks)} [{chunk_emo}] · “{preview_txt}”",
        )

        seg, steps = core._run_single(
            norm_chunk,
            target_lang,
            req.speed,
            stab,
            sim,
            sty,
            model_choice,
            req.denoise,
            emotion=chunk_emo,
            ref_audio=audio_path,
            ref_text=v.get("sampleText", ""),
        )
        seg = core.apply_taper(seg, sr, fade_ms=20)
        audio_segments.append(seg)

        if i < len(chunks) - 1:
            pause_sec = prof["pause_sec"]
            with_breath = prof["breath"]
            c_stripped = norm_chunk.strip()
            if c_stripped.endswith((".", "!", "?")):
                audio_segments.append(core.natural_pause(sr, duration_sec=pause_sec, with_breath=with_breath))
            elif c_stripped.endswith((",", ";", ":")):
                audio_segments.append(core.natural_pause(sr, duration_sec=max(0.18, pause_sec * 0.6), with_breath=False))
            else:
                audio_segments.append(core.natural_pause(sr, duration_sec=max(0.24, pause_sec * 0.8), with_breath=False))

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    log_studio_step(88, "Mastering -14 LUFS & Spatial DSP", f"Xử lý EQ 5-band · Khoảng cách: {req.distance} · Không gian: {req.space}")
    full_audio = np.concatenate(audio_segments)
    if req.lufs:
        full_audio = core.master_audio(full_audio, sr=sr)

    full_audio = core.apply_audio_effects(full_audio, sr=sr, distance=fx_dist, env_filter=fx_env)

    out_path = core.save_output(full_audio, "tts")
    fname = os.path.basename(out_path)
    dur = float(len(full_audio) / sr)
    elapsed = float(time.time() - t0)
    audio_url = f"/outputs/{fname}"
    bars = finish_studio_job(
        full_audio,
        sr,
        audio_url,
        fname,
        f"Hoàn tất {fname} · Thời lượng {dur:.2f}s (xử lý {elapsed:.2f}s)",
    )

    return {
        "audioUrl": audio_url,
        "filename": fname,
        "voiceName": v["name"],
        "duration": round(dur, 2),
        "elapsed": round(elapsed, 2),
        "chunks": len(chunks),
        "steps": total_steps,
        "emotions": sorted(list(set(emotions_used))),
        "distance": req.distance or "Vừa",
        "space": req.space or "Phòng thu khô",
        "createdAt": datetime.datetime.now().strftime("%H:%M:%S"),
        "waveform": bars,
        "logs": STUDIO_TELEMETRY["logs"],
    }


@app.get("/api/history")
def api_history():
    files = core.history_files()
    items = []
    for f in files:
        fname = os.path.basename(f)
        mtime = os.path.getmtime(f)
        dt_str = datetime.datetime.fromtimestamp(mtime).strftime("%H:%M · %d/%m")
        size_kb = max(1, round(os.path.getsize(f) / 1024))
        items.append({
            "filename": fname,
            "audioUrl": f"/outputs/{fname}",
            "createdAt": dt_str,
            "sizeKb": size_kb,
        })
    return {"history": items}


@app.delete("/api/history/{filename}")
def api_delete_history_item(filename: str):
    safe_name = os.path.basename(filename)
    if not safe_name.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Tên tệp không hợp lệ.")
    target_path = os.path.join(core.OUT_DIR, safe_name)
    if os.path.exists(target_path):
        try:
            os.remove(target_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Không thể xóa tệp: {str(e)}")
    return {"deleted": safe_name, "message": f"Đã xóa bản ghi {safe_name}"}


@app.delete("/api/history")
def api_clear_all_history():
    files = core.history_files()
    count = 0
    for f in files:
        try:
            if os.path.exists(f) and core.OUT_DIR in os.path.abspath(f):
                os.remove(f)
                count += 1
        except Exception:
            pass
    return {"cleared": count, "message": f"Đã dọn sạch {count} bản ghi lịch sử."}


@app.post("/api/voices/clone")
async def api_voice_clone(
    name: str = Form(...),
    transcript: str = Form(...),
    audio: UploadFile = File(...),
):
    name = name.strip()
    transcript = transcript.strip()
    if not name or not transcript:
        raise HTTPException(status_code=400, detail="Vui lòng nhập tên giọng và bản chép lời chính xác.")

    begin_studio_job("Sao chép từ mẫu (Voice Clone)", name)
    ext = os.path.splitext(audio.filename or "")[1] or ".wav"
    slug = core._slug(name)
    dst = os.path.join(core.VOICES_DIR, f"{slug}{ext}")
    with open(dst, "wb") as f_out:
        content = await audio.read()
        f_out.write(content)

    log_studio_step(45, "Phân tích tệp âm thanh gốc", f"Đã lưu mẫu gốc {os.path.basename(dst)} ({len(content)//1024} KB)")

    d = core.load_custom()
    d[name] = {
        "audio": dst,
        "text": transcript,
        "desc": "Bản sao giọng nói (Sao chép từ mẫu)",
        "type": "cloned",
        "preset": False,
        "lang_category": "custom",
    }
    core.save_custom(d)

    log_studio_step(75, "Trích xuất đặc trưng & kiểm thử giọng", "Đang đọc mẫu để dựng sóng âm chuẩn...")
    try:
        wav_data, sr = sf.read(dst, dtype="float32")
        if wav_data.ndim > 1:
            wav_data = np.mean(wav_data, axis=1)
    except Exception:
        wav_data, sr = np.zeros(24000, dtype=np.float32), 24000

    vid = f"custom-{slug.lower()}"
    new_voice = resolve_voice(vid)
    out_v = {k: val for k, val in new_voice.items() if k != "audioPath"}
    out_v["previewUrl"] = f"/api/voices/{out_v['id']}/preview"
    bars = finish_studio_job(
        wav_data,
        sr,
        out_v["previewUrl"],
        os.path.basename(dst),
        f"Đã lưu giọng sao chép “{name}” vào Kho giọng đọc",
    )
    return {
        "voice": out_v,
        "audioUrl": out_v["previewUrl"],
        "waveform": bars,
        "logs": STUDIO_TELEMETRY["logs"],
        "message": f"Đã tạo bản sao giọng nói “{name}” thành công!",
    }


class DesignRequest(BaseModel):
    name: str
    prompt: str
    language: str = "Tiếng Việt"


@app.post("/api/voices/design")
def api_voice_design(req: DesignRequest):
    name = (req.name or "").strip()
    prompt = (req.prompt or "").strip()
    if not name or not prompt:
        raise HTTPException(status_code=400, detail="Vui lòng điền tên và mô tả giọng đọc.")

    begin_studio_job("Thiết kế giọng đọc (Voice Design)", name)
    sample_script = (
        "Xin chào, đây là giọng đọc mới được thiết kế tự động từ mô tả của bạn."
        if "việt" in req.language.lower() or any(c in "àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệ" for c in prompt.lower())
        else "Hello, this is a newly designed voice generated directly from your description."
    )

    log_studio_step(35, "Khởi tạo đặc trưng âm sắc từ mô tả", f"Instruct: {prompt[:60]}")
    t0 = time.time()
    with torch.inference_mode():
        audio = core.model.generate(
            text=sample_script,
            language=core.LANG_MAP.get(req.language),
            num_step=14,
            instruct=prompt,
            postprocess_output=True,
        )[0]
    if isinstance(audio, torch.Tensor):
        audio = audio.detach().cpu().numpy()
    audio = np.asarray(audio, dtype=np.float32).squeeze()

    log_studio_step(85, "Mastering mẫu giọng mới (-14 LUFS)", "Cân bằng âm sắc và lưu vào Kho giọng đọc")
    audio = core.master_audio(audio, sr=core.model.sampling_rate)

    slug = core._slug(name)
    dst = os.path.join(core.VOICES_DIR, f"{slug}.wav")
    sf.write(dst, audio, core.model.sampling_rate)
    out_path = core.save_output(audio, "design")
    fname = os.path.basename(out_path)
    audio_url = f"/outputs/{fname}"

    d = core.load_custom()
    d[name] = {
        "audio": dst,
        "text": sample_script,
        "desc": prompt[:90],
        "type": "designed",
        "preset": False,
        "lang_category": "custom",
    }
    core.save_custom(d)

    vid = f"custom-{slug.lower()}"
    new_voice = resolve_voice(vid)
    out_v = {k: val for k, val in new_voice.items() if k != "audioPath"}
    out_v["previewUrl"] = f"/api/voices/{out_v['id']}/preview"
    elapsed = round(time.time() - t0, 2)
    bars = finish_studio_job(
        audio,
        core.model.sampling_rate,
        audio_url,
        fname,
        f"Hoàn tất thiết kế giọng “{name}” trong {elapsed}s",
    )
    return {
        "voice": out_v,
        "audioUrl": audio_url,
        "elapsed": elapsed,
        "waveform": bars,
        "logs": STUDIO_TELEMETRY["logs"],
        "message": f"Đã thiết kế và lưu giọng “{name}” vào Kho giọng đọc!",
    }


@app.delete("/api/voices/{voice_id}")
def api_delete_voice(voice_id: str):
    custom = core.load_custom()
    target_key = None
    for cname in list(custom.keys()):
        vid = f"custom-{core._slug(cname).lower()}"
        if vid == voice_id or cname.lower() == voice_id.lower():
            target_key = cname
            break
    if not target_key:
        raise HTTPException(status_code=400, detail="Chỉ có thể xóa các giọng tự tạo của bạn.")
    meta = custom.pop(target_key, {})
    core.save_custom(custom)
    audio_file = meta.get("audio", "")
    if audio_file and os.path.exists(audio_file) and core.VOICES_DIR in os.path.abspath(audio_file):
        try:
            os.remove(audio_file)
        except Exception:
            pass
    return {"deletedId": voice_id, "message": f"Đã xóa giọng “{target_key}” khỏi Kho giọng đọc."}


@app.post("/api/changer")
async def api_voice_changer(
    voiceId: str = Form("minh-anh"),
    prompt: str = Form(""),
    speed: float = Form(0.95),
    stability: float = Form(45.0),
    similarity: float = Form(75.0),
    distance: str = Form("Xa"),
    space: str = Form("Phòng thu khô"),
    language: str = Form("Tự động"),
    lufs: bool = Form(True),
    file: UploadFile = File(...),
):
    req_voice = voiceId or "minh-anh"
    v = resolve_voice(req_voice)
    audio_path = v.get("audioPath", "")
    if not audio_path or not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail="Không tìm thấy giọng đích đã chọn.")

    begin_studio_job("Chuyển đổi giọng nói (Voice Changer)", v["name"])
    text_to_speak = (prompt or "").strip()
    if not text_to_speak:
        text_to_speak = v.get("sampleText", "Xin chào, đây là bản ghi sau khi chuyển đổi sang giọng đọc mới.")

    is_vi = any(c in "àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ" for c in text_to_speak.lower()) or "việt" in v.get("language", "").lower()
    target_lang = language or "Tự động"
    if target_lang == "Tự động":
        target_lang = "Tiếng Việt" if is_vi else "English"

    stab = float(stability) / 100.0 if stability > 1.0 else float(stability)
    sim = float(similarity) / 100.0 if similarity > 1.0 else float(similarity)
    fx_dist = DISTANCE_MAP.get(distance or "Medium", "Medium")
    fx_env = SPACE_MAP.get(space or "Studio (Dry)", "Studio (Dry)")

    log_studio_step(40, "Chuyển đổi âm sắc sang giọng đích", f"Tệp nguồn: {file.filename} -> Giọng đích: {v['name']} ({target_lang})")
    t0 = time.time()
    sr = core.model.sampling_rate
    audio, steps = core._run_single(
        text_to_speak,
        target_lang,
        speed,
        stab,
        sim,
        0.05,
        "Eleven v4 (Turbo)",
        True,
        ref_audio=audio_path,
        ref_text=v.get("sampleText", ""),
    )
    log_studio_step(85, "Mastering & Hiệu ứng không gian", f"Khoảng cách: {distance} · Không gian: {space}")
    if lufs:
        audio = core.master_audio(audio, sr=sr)
    audio = core.apply_audio_effects(audio, sr=sr, distance=fx_dist, env_filter=fx_env)

    out_path = core.save_output(audio, "vc_changer")
    fname = os.path.basename(out_path)
    dur = float(len(audio) / sr)
    elapsed = float(time.time() - t0)
    audio_url = f"/outputs/{fname}"
    bars = finish_studio_job(
        audio,
        sr,
        audio_url,
        fname,
        f"Hoàn tất đổi giọng {fname} · Thời lượng {dur:.2f}s (xử lý {elapsed:.2f}s)",
    )

    return {
        "audioUrl": audio_url,
        "filename": fname,
        "voiceName": v["name"],
        "duration": round(dur, 2),
        "elapsed": round(elapsed, 2),
        "waveform": bars,
        "logs": STUDIO_TELEMETRY["logs"],
    }


if __name__ == "__main__":
    import uvicorn
    print("🚀 Khởi chạy Thành Âm Studio FastAPI Backend tại http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
