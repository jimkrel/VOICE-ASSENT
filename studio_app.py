import os, time, json, shutil, re, glob, socket, datetime

# Protect SSD Drive C: -> force all caches and temps to Drive E:
os.environ['HF_HOME'] = r'E:\VoiceAI\hf_cache'
os.environ['TORCH_HOME'] = r'E:\VoiceAI\torch_cache'
os.environ['TEMP'] = r'E:\VoiceAI\temp'
os.environ['TMP'] = r'E:\VoiceAI\temp'
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:128'

import numpy as np
import torch
if torch.cuda.is_available():
    torch.backends.cudnn.benchmark = True
import soundfile as sf
from scipy import signal
import gradio as gr
from omnivoice.models.omnivoice import OmniVoice

BASE = r"E:\VoiceAI"
VOICES_DIR = os.path.join(BASE, "voices")
OUT_DIR = os.path.join(BASE, "outputs")
PRESET_DIR = os.path.join(BASE, "presets")
DB_PATH = os.path.join(VOICES_DIR, "voices.json")
for d in (VOICES_DIR, OUT_DIR, PRESET_DIR):
    os.makedirs(d, exist_ok=True)


def lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


LAN_URL = f"http://{lan_ip()}:7860"

print("🔄 Đang nạp mô hình OmniVoice trên NVIDIA GeForce GTX 1650 (fp16)...")
model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cuda:0", dtype=torch.float16)
print("✅ OmniVoice đã sẵn sàng trên CUDA")

# ------------------------------------------------------------------
# Kho giọng đọc: Đưa English Vocals YouTube lên hàng đầu
# ------------------------------------------------------------------
PRESETS = {
    "Hope — upbeat and clear": {
        "audio": os.path.join(PRESET_DIR, "eleven_hope.wav"),
        "text": "Deep inside the Black Forest, investigators discovered an abandoned radio tower broadcasting an unbroken seven-digit code.",
        "desc": "US Nữ • Trong trẻo, ngọt ngào, lôi cuốn, tươi sáng • Social Media, TikTok, Reels, Podcast",
        "gender": "female",
        "accent": "American",
        "genre": "✨ Upbeat & Clear",
        "lang_category": "en",
        "type": "elevenlabs",
        "preset": True,
    },
    "Marcus — documentary and crime": {
        "audio": os.path.join(PRESET_DIR, "marcus_documentary.wav"),
        "text": "The year was 1994. Deep inside the mountain, investigators discovered something that defies all rational explanation.",
        "desc": "English (US) • Nam trầm uy quyền • True Crime, Documentary",
        "lang_category": "en",
        "type": "default",
        "preset": True,
    },
    "Liam — storyteller and essay": {
        "audio": os.path.join(PRESET_DIR, "liam_storyteller.wav"),
        "text": "Have you ever wondered why some stories stay with you forever, while others fade away in minutes?",
        "desc": "English (US) • Nam tự nhiên lôi cuốn • Video Essay, YouTube Story",
        "lang_category": "en",
        "type": "default",
        "preset": True,
    },
    "Alex — movie recap and shorts": {
        "audio": os.path.join(PRESET_DIR, "alex_recap.wav"),
        "text": "He thought he could escape the police, but within forty seconds, his entire plan completely unraveled.",
        "desc": "English (US) • Nam nhịp nhanh sắc nét • Movie Recap, Shorts Hook",
        "lang_category": "en",
        "type": "default",
        "preset": True,
    },
    "Emma — explainer and podcast": {
        "audio": os.path.join(PRESET_DIR, "emma_explainer.wav"),
        "text": "Science is not just about memorizing facts; it is about looking at the world with curiosity and wonder.",
        "desc": "English (UK) • Nữ truyền cảm hứng • Science Explainer, Podcast",
        "lang_category": "en",
        "type": "default",
        "preset": True,
    },
}

# Tự động nạp toàn bộ 16 giọng ElevenLabs Originals trải dài mọi thể loại
CATALOG_PATH = os.path.join(BASE, "elevenlabs_catalog.json")
if os.path.exists(CATALOG_PATH):
    try:
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            PRESETS.update(json.load(f))
    except Exception as e:
        print("Lỗi đọc catalog ElevenLabs:", e)

# Thêm giọng Tiếng Việt
PRESETS.update({
    "Minh Anh — Nam ấm áp, rõ ràng (Tiếng Việt)": {
        "audio": os.path.join(PRESET_DIR, "voice_vi_male.mp3"),
        "text": "Xin chào, đây là giọng đọc nam truyền cảm chuẩn phòng thu studio.",
        "desc": "Tiếng Việt • Nam • Tự sự, Thuyết minh",
        "gender": "male",
        "accent": "Vietnamese",
        "lang_category": "vi",
        "type": "default",
        "preset": True,
    },
    "Bảo Ngọc — Nữ nhẹ nhàng, tươi sáng (Tiếng Việt)": {
        "audio": os.path.join(PRESET_DIR, "voice_vi_female.mp3"),
        "text": "Chào bạn, đây là giọng đọc nữ nhẹ nhàng, tự nhiên và tràn đầy cảm xúc.",
        "desc": "Tiếng Việt • Nữ • Kể chuyện, Sách nói",
        "gender": "female",
        "accent": "Vietnamese",
        "lang_category": "vi",
        "type": "default",
        "preset": True,
    },
    "Gia Huy — Nam tự nhiên, gần gũi (Tiếng Việt)": {
        "audio": os.path.join(PRESET_DIR, "voice_vi_male.mp3"),
        "text": "Khám phá trải nghiệm mới mỗi ngày. Lắng nghe, cảm nhận và để câu chuyện của bạn cất lời.",
        "desc": "Tiếng Việt • Nam • Quảng cáo, Review",
        "gender": "male",
        "accent": "Vietnamese",
        "lang_category": "vi",
        "type": "default",
        "preset": True,
    },
})


def load_custom():
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_custom(d):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def all_voices():
    v = dict(PRESETS)
    v.update(load_custom())
    return v


def voice_choices():
    return list(all_voices().keys())


LANG_MAP = {"English": "English", "Tiếng Việt": "Vietnamese", "Tự động": None}

MODEL_STEPS = {
    "OmniVoice Siêu Tốc (12 bước)": {"steps": 12, "cfg": 1.9, "pos": 5.0},
    "OmniVoice Cân Bằng (Chuẩn 20 bước)": {"steps": 20, "cfg": 2.0, "pos": 5.0},
    "OmniVoice Tốc Độ Cao (Nhanh 14 bước)": {"steps": 14, "cfg": 1.9, "pos": 5.0},
    "OmniVoice Chi Tiết Cao (Kỹ 28 bước)": {"steps": 28, "cfg": 2.05, "pos": 5.0},
}


def render_model_info(m_name):
    if "v4" in m_name:
        return """
        <div class="el-model-meta-box">
          <div class="m-head-row">
            <span class="m-badge-active">● Đang kích hoạt</span>
            <span class="m-speed">⚡ Tốc độ cao nhất</span>
          </div>
          <div class="m-desc"><b>Eleven v4</b>: Mô hình siêu tốc & biểu cảm tự nhiên nhất (8 bước Flow-matching). Tối ưu hóa độ trễ thấp, sinh nhanh trong ~10-14s, thích hợp cho YouTube Shorts, Movie Recap, đối thoại tương tác.</div>
          <div class="m-tags">
            <span class="m-tag">Fastest</span>
            <span class="m-tag">Most Emotive</span>
            <span class="m-tag">~12s latency</span>
            <span class="m-tag">Shorts/Recap</span>
          </div>
        </div>"""
    elif "v3" in m_name:
        return """
        <div class="el-model-meta-box">
          <div class="m-head-row">
            <span class="m-badge-active">● Đang kích hoạt</span>
            <span class="m-speed">🎭 Diễn cảm chuyên sâu</span>
          </div>
          <div class="m-desc"><b>Eleven v3</b>: Mô hình giàu kịch tính (12 bước, CFG 3.2). Nhấn nhá ngữ điệu mạnh mẽ, thích hợp cho Video Essay, Phim tài liệu True Crime, kịch bản đòi hỏi nhiều cao trào.</div>
          <div class="m-tags">
            <span class="m-tag">Highly Expressive</span>
            <span class="m-tag">High Dynamic Range</span>
            <span class="m-tag">Video Essay</span>
            <span class="m-tag">True Crime</span>
          </div>
        </div>"""
    else:
        return """
        <div class="el-model-meta-box">
          <div class="m-head-row">
            <span class="m-badge-active">● Đang kích hoạt</span>
            <span class="m-speed">🎯 Bám mẫu chuẩn nhất</span>
          </div>
          <div class="m-desc"><b>Eleven Multilingual v2</b>: Mô hình có độ giống giọng mẫu (Speaker Similarity) cao nhất & ổn định nhất (14 bước). Tối ưu cho Voice Over, Sao chép giọng người thật và Sách nói dài.</div>
          <div class="m-tags">
            <span class="m-tag">Highest Similarity</span>
            <span class="m-tag">Voice Clone</span>
            <span class="m-tag">Voice Over</span>
            <span class="m-tag">Audiobooks</span>
          </div>
        </div>"""


def render_voice_preview_quote(v_name):
    v = all_voices().get(v_name, {})
    text = v.get("text", "")
    desc = v.get("desc", "")
    audio_path = v.get("audio", "").replace(os.sep, "/")
    audio_url = f"/gradio_api/file={audio_path}"
    sname = v_name.split("—")[0].strip()
    return f"""
    <div class="el-sample-quote-card">
      <div class="s-head-row">
        <button class="voice-circle-play-btn" onclick="playVoicePreview('{audio_url}', this)" title="Bấm nghe thử giọng {sname}">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 3 20 12 6 21 6 3"/></svg>
        </button>
        <div class="s-avatar-orb" title="{sname}"></div>
        <div class="s-meta-col">
          <div class="s-desc"><b>{sname}</b> • {desc}</div>
          <div class="s-quote">“{text}”</div>
        </div>
      </div>
    </div>"""



# ------------------------------------------------------------------
# Kịch bản mẫu YouTube English & Tiếng Việt chuẩn
# ------------------------------------------------------------------
PROMPTS = {
    "🕵️ True Crime": "The year was 1994. Deep inside the Black Forest, investigators discovered an abandoned radio tower broadcasting an unbroken 7-digit code. Every night at precisely 3:15 AM, the transmission repeated the exact same pattern.",
    "📈 Video Essay": "How did a small team of engineers quietly outsmart Silicon Valley's biggest tech giants? The answer lies in one forgotten decision made late at night in a modest garage.",
    "🎬 Movie Recap": "In a world where artificial intelligence controls every frequency, one man discovers a hidden signal that changes everything. Now, he only has twenty-four hours to uncover the truth.",
    "⚡ Shorts Hook": "Stop scrolling! What if I told you that the voice you're listening to right now isn't human, but running completely free on a 4GB graphics card?",
    "🌌 Science Explainer": "To understand quantum gravity, we first have to unlearn everything we know about empty space. Because in reality, nothing is ever truly empty.",
    "📖 Kể chuyện (Việt)": "Ngày nọ, trong một khu rừng nhỏ, có một chú chim luôn mơ được bay đến đại dương xa xôi.",
    "🎙 Quảng cáo (Việt)": "Khám phá trải nghiệm mới mỗi ngày. Lắng nghe, cảm nhận và để câu chuyện của bạn cất lời.",
}


# ------------------------------------------------------------------
# Chuẩn hóa kịch bản (Text Normalization) loại bỏ vấp số/giờ/viết tắt
# ------------------------------------------------------------------
def num_to_words(n):
    units = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
             'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen',
             'seventeen', 'eighteen', 'nineteen']
    tens = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
    if n < 0:
        return 'minus ' + num_to_words(-n)
    if n < 20:
        return units[n]
    if n < 100:
        return tens[n // 10] + ('' if n % 10 == 0 else '-' + units[n % 10])
    if n < 1000:
        rem = n % 100
        return units[n // 100] + ' hundred' + ('' if rem == 0 else ' ' + num_to_words(rem))
    if 1000 <= n < 2000:
        century = n // 100
        rem = n % 100
        if rem == 0:
            return units[century] + ' hundred'
        elif rem < 10:
            return units[century] + ' oh-' + units[rem]
        else:
            return units[century] + ' ' + num_to_words(rem)
    if 2000 <= n < 2100:
        rem = n % 100
        if rem == 0:
            return 'two thousand'
        elif rem < 10:
            return 'two thousand and ' + units[rem]
        else:
            return 'twenty ' + num_to_words(rem)
    if n < 1000000:
        thousands = n // 1000
        rem = n % 1000
        return num_to_words(thousands) + ' thousand' + ('' if rem == 0 else ' ' + num_to_words(rem))
    return str(n)


def normalize_script(text, lang="English"):
    if not text:
        return ""
    is_vi = lang == "Tiếng Việt" or any(c in "àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ" for c in text.lower())
    if is_vi:
        t = text.strip()
        vi_abbrs = [
            (r'\bđc\b', 'được'),
            (r'\bko\b', 'không'),
            (r'\bk\b', 'không'),
            (r'\bvs\b', 'với'),
            (r'\bj\b', 'gì'),
            (r'\bsp\b', 'sản phẩm'),
            (r'\bnv\b', 'nhân viên'),
            (r'\bmk\b', 'mình'),
            (r'\btks\b', 'cảm ơn'),
            (r'\btk\b', 'cảm ơn'),
            (r'\ba/c\b', 'anh chị'),
            (r'\bac\b', 'anh chị'),
            (r'\bkh\b', 'khách hàng'),
            (r'\bib\b', 'nhắn tin'),
            (r'\bPET\b', 'P-E-T'),
            (r'\bpet\b', 'P-E-T'),
            (r'\bpp\b', 'P-P'),
            (r'\bPP\b', 'P-P'),
            (r'\bkg\b', 'ki-lô-gam'),
            (r'\bml\b', 'mi-li-lít'),
            (r'\bcm\b', 'xen-ti-mét'),
            (r'\bmm\b', 'mi-li-mét'),
            (r'\bvnđ\b', 'đồng'),
            (r'\bvnd\b', 'đồng'),
            (r'\bđ\b', 'đồng'),
            (r'(\d+)k\b', r'\1 nghìn'),
            (r'(\d+)%', r'\1 phần trăm'),
        ]
        for pat, rep in vi_abbrs:
            t = re.sub(pat, rep, t, flags=re.IGNORECASE)
        t = re.sub(r'[ \t]+', ' ', t)
        return t

    def _rep_time(m):
        h = int(m.group(1))
        mins = int(m.group(2))
        ampm = (m.group(3) or '').lower()
        h_str = num_to_words(h)
        if mins == 0:
            m_str = "o'clock"
        elif mins < 10:
            m_str = f"oh-{num_to_words(mins)}"
        else:
            m_str = num_to_words(mins)
        ampm_str = " a.m." if "a" in ampm else (" p.m." if "p" in ampm else "")
        return f"{h_str} {m_str}{ampm_str}".strip()

    t = re.sub(r'\b(\d{1,2})[:.](\d{2})\s*(AM|PM|am|pm)?\b', _rep_time, text)
    t = re.sub(r'\b(\d+)-([a-zA-Z]+)\b', lambda m: f"{num_to_words(int(m.group(1)))}-{m.group(2)}", t)
    t = re.sub(r'\$(\d+)', lambda m: f"{num_to_words(int(m.group(1)))} dollars", t)
    t = re.sub(r'(\d+)%', lambda m: f"{num_to_words(int(m.group(1)))} percent", t)
    t = re.sub(r'\b(\d+)\b', lambda m: num_to_words(int(m.group(1))), t)
    return t


def split_smart_sentences(text, max_len=260):
    text = text.strip()
    paras = [p.strip() for p in text.split('\n') if p.strip()]
    chunks = []
    for p in paras:
        raw_sents = re.split(r'(?<=[.!?])\s+', p)
        buf = ""
        for s in raw_sents:
            s = s.strip()
            if not s:
                continue
            if not buf:
                buf = s
            elif len(buf) + len(s) + 1 <= max_len:
                buf = f"{buf} {s}"
            else:
                chunks.append(buf)
                buf = s
        if buf:
            chunks.append(buf)
    return chunks if chunks else [text]


def natural_pause(sr, duration_sec=0.42, with_breath=True):
    n_samples = int(duration_sec * sr)
    room_air = np.random.normal(0, 7e-5, n_samples).astype(np.float32)
    if not with_breath or duration_sec < 0.35:
        return room_air

    # Mô phỏng tiếng lấy hơi nhẹ tự nhiên của con người (Palatal Inhalation Breath ~ -56 dBFS)
    # 85ms nghỉ sau câu -> 200ms lấy hơi êm qua vòm họng (500-2600Hz) -> 135ms đóng thanh môn trước câu mới
    b_start = int(0.085 * sr)
    b_len = min(int(0.200 * sr), n_samples - b_start - int(0.080 * sr))
    if b_len > 200:
        raw_breath = np.random.normal(0, 1.0, b_len).astype(np.float32)
        try:
            sos_bp = signal.butter(2, [500.0, 2600.0], btype="bandpass", fs=sr, output="sos")
            shaped = signal.sosfilt(sos_bp, raw_breath)
            win = 0.5 * (1.0 - np.cos(np.linspace(0, 2.0 * np.pi, b_len, dtype=np.float32)))
            breath_wave = shaped * win * 0.0014
            room_air[b_start:b_start + b_len] += breath_wave
        except Exception:
            pass
    return room_air


def apply_taper(audio, sr, fade_ms=20):
    fade_len = int(sr * fade_ms / 1000.0)
    if len(audio) < 2 * fade_len:
        return audio
    fade_in = 0.5 * (1.0 - np.cos(np.linspace(0, np.pi, fade_len)))
    fade_out = 0.5 * (1.0 + np.cos(np.linspace(0, np.pi, fade_len)))
    audio = audio.copy()
    audio[:fade_len] *= fade_in
    audio[-fade_len:] *= fade_out
    return audio



# ------------------------------------------------------------------
# Hệ thống Emotion Hierarchy & Multi-Tier Emotion Parsing (ElevenLabs Standard)
# ------------------------------------------------------------------
EMOTION_TAGS = {
    "thì thầm": "whisper",
    "whisper": "whisper",
    "kịch tính": "dramatic",
    "dramatic": "dramatic",
    "hào hứng": "excited",
    "excited": "excited",
    "buồn": "sad",
    "sad": "sad",
    "buồn bã": "sad",
    "tức giận": "angry",
    "angry": "angry",
    "thở dài": "sigh",
    "sigh": "sigh",
    "điềm tĩnh": "calm",
    "calm": "calm",
}

TAG_REGEX = re.compile(r'\[(.*?)\]', re.IGNORECASE)

EMOTION_PROFILES = {
    "calm": {
        "speed_mult": 1.0,
        "cfg_mult": 1.0,
        "pos_mult": 1.0,
        "pause_sec": 0.35,
        "breath": True,
        "desc": "Điềm tĩnh, tự nhiên"
    },
    "whisper": {
        "speed_mult": 0.92,
        "cfg_mult": 0.88,
        "pos_mult": 0.72,
        "pause_sec": 0.38,
        "breath": True,
        "desc": "Thì thầm, bí ẩn, hơi thở sâu"
    },
    "dramatic": {
        "speed_mult": 0.90,
        "cfg_mult": 1.10,
        "pos_mult": 1.25,
        "pause_sec": 0.50,
        "breath": True,
        "desc": "Kịch tính, cao trào, ngưng nghỉ dài"
    },
    "excited": {
        "speed_mult": 1.08,
        "cfg_mult": 1.05,
        "pos_mult": 1.18,
        "pause_sec": 0.22,
        "breath": False,
        "desc": "Hào hứng, nhiệt huyết, nhịp nhanh"
    },
    "sad": {
        "speed_mult": 0.86,
        "cfg_mult": 0.92,
        "pos_mult": 0.75,
        "pause_sec": 0.52,
        "breath": True,
        "desc": "Buồn bã, trầm lắng, hụt hơi"
    },
    "angry": {
        "speed_mult": 1.10,
        "cfg_mult": 1.15,
        "pos_mult": 1.30,
        "pause_sec": 0.25,
        "breath": False,
        "desc": "Tức giận, dồn dập, gãy gọn"
    },
    "sigh": {
        "speed_mult": 0.88,
        "cfg_mult": 0.90,
        "pos_mult": 0.80,
        "pause_sec": 0.45,
        "breath": True,
        "desc": "Thở dài, mệt mỏi, buông lơi"
    },
}

def parse_emotion_script(raw_text):
    lines = raw_text.split('\n')
    current_emotion = "calm"
    segments = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        tokens = re.split(r'(\[.*?\])', line)
        for tok in tokens:
            tok = tok.strip()
            if not tok:
                continue
            m = TAG_REGEX.match(tok)
            if m:
                tag_content = m.group(1).strip().lower()
                if tag_content in EMOTION_TAGS:
                    current_emotion = EMOTION_TAGS[tag_content]
            else:
                segments.append({
                    "text": tok,
                    "emotion": current_emotion
                })
    return segments

def parse_and_chunk_script(raw_text, lang="English"):
    raw_segments = parse_emotion_script(raw_text)
    if not raw_segments:
        raw_text_clean = re.sub(r'\[.*?\]', '', raw_text).strip()
        if raw_text_clean:
            return [{"text": s, "emotion": "calm"} for s in split_smart_sentences(raw_text_clean, max_len=180)]
        return []
    final_chunks = []
    for seg in raw_segments:
        text = seg["text"].strip()
        if not text:
            continue
        sub_sents = split_smart_sentences(text, max_len=180)
        for s in sub_sents:
            final_chunks.append({
                "text": s,
                "emotion": seg["emotion"]
            })
    return final_chunks

def apply_emotion_dsp(audio, sr=24000, emotion="calm"):
    if len(audio) == 0 or emotion == "calm":
        return audio
    data = np.asarray(audio, dtype=np.float32).copy()
    try:
        if emotion == "whisper":
            sos_hp = signal.butter(2, 140.0, btype="highpass", fs=sr, output="sos")
            data = signal.sosfilt(sos_hp, data)
            data = biquad_peaking(data, sr, 3200.0, +2.5, Q=1.0)
            data = biquad_peaking(data, sr, 7000.0, +2.0, Q=0.8)
            data = np.tanh(data * 0.85) / 0.85

        elif emotion == "dramatic":
            data = biquad_peaking(data, sr, 160.0, +2.2, Q=0.9)
            data = biquad_peaking(data, sr, 500.0, -1.2, Q=1.2)
            data = biquad_peaking(data, sr, 2800.0, +1.6, Q=0.9)
            data = np.tanh(data * 1.15) / 1.15

        elif emotion == "excited":
            data = biquad_peaking(data, sr, 2600.0, +2.6, Q=1.0)
            data = biquad_peaking(data, sr, 8000.0, +1.8, Q=0.8)
            data = np.tanh(data * 1.20) / 1.20

        elif emotion == "sad":
            data = biquad_peaking(data, sr, 2200.0, -2.2, Q=1.0)
            sos_lp = signal.butter(2, 6500.0, btype="lowpass", fs=sr, output="sos")
            data = 0.70 * data + 0.30 * signal.sosfilt(sos_lp, data)

        elif emotion == "angry":
            data = biquad_peaking(data, sr, 220.0, +2.0, Q=1.1)
            data = biquad_peaking(data, sr, 3400.0, +3.2, Q=1.2)
            data = np.tanh(data * 1.35) / 1.35

        elif emotion == "sigh":
            sos_hp = signal.butter(2, 120.0, btype="highpass", fs=sr, output="sos")
            data = signal.sosfilt(sos_hp, data)
            data = biquad_peaking(data, sr, 4000.0, +1.5, Q=0.9)
    except Exception:
        pass

    p = np.max(np.abs(data))
    if p > 0.95:
        data = data * (0.92 / p)
    return data.astype(np.float32)


def biquad_peaking(data, sr, f0, gain_db, Q=1.0):
    A = 10.0 ** (gain_db / 40.0)
    w0 = 2.0 * np.pi * f0 / sr
    alpha = np.sin(w0) / (2.0 * Q)
    b0 = 1.0 + alpha * A
    b1 = -2.0 * np.cos(w0)
    b2 = 1.0 - alpha * A
    a0 = 1.0 + alpha / A
    a1 = -2.0 * np.cos(w0)
    a2 = 1.0 - alpha / A
    b = np.array([b0 / a0, b1 / a0, b2 / a0], dtype=np.float32)
    a = np.array([1.0, a1 / a0, a2 / a0], dtype=np.float32)
    return signal.lfilter(b, a, data)


# ------------------------------------------------------------------
# Bộ lọc âm thanh 5-Stage ElevenLabs Vocal Sweetness & Clarity DSP
# ------------------------------------------------------------------
def master_audio(audio, sr=24000, enable_eq=True, enable_compress=True):
    if len(audio) == 0:
        return audio
    data = np.asarray(audio, dtype=np.float32)

    # Stage 1: Highpass 65Hz (cắt rumble & gió mic)
    try:
        sos_hp = signal.butter(2, 65.0, btype="highpass", fs=sr, output="sos")
        data = signal.sosfilt(sos_hp, data)
    except Exception:
        pass

    if enable_eq:
        try:
            # Stage 2: Tube 2nd-Order Even-Harmonic Warmth (tạo độ ngọt analog, lấp đầy pha vocoder)
            sq = data * data
            data = data + 0.028 * (sq - np.mean(sq))

            # Stage 3: ElevenLabs 5-Band Spectral Curve Matching EQ
            data = biquad_peaking(data, sr, 185.0, +0.5, Q=0.9)   # Ấm ngực tự nhiên (Chest Warmth)
            data = biquad_peaking(data, sr, 480.0, -0.4, Q=1.1)   # Khử âm mũi đục (De-boxiness)
            data = biquad_peaking(data, sr, 1750.0, +1.3, Q=0.8)  # Độ trong trẻo & tiến trước (Forward Presence)
            data = biquad_peaking(data, sr, 3400.0, +0.9, Q=1.0)  # Độ rõ từng chữ (Articulation Clarity)
            data = biquad_peaking(data, sr, 7800.0, -1.2, Q=0.9)  # Khử xè kim loại Vocoder (Silk De-Fizz)

            # Silk High Roll-off @ 10.2kHz (làm mượt dải siêu cao như ElevenLabs gốc)
            sos_lp = signal.butter(2, 10200.0, btype="lowpass", fs=sr, output="sos")
            data = 0.75 * data + 0.25 * signal.sosfilt(sos_lp, data)

            # Stage 4: Dynamic De-Esser (làm dịu âm xuýt s/sh ở 4.5-7.5kHz)
            sos_sib = signal.butter(2, [4500.0, 7500.0], btype="bandpass", fs=sr, output="sos")
            sib = signal.sosfilt(sos_sib, data)
            sib_env = np.abs(sib)
            win = int(0.005 * sr)
            if win > 1:
                sib_env = np.convolve(sib_env, np.ones(win, dtype=np.float32) / win, mode="same")
            deess_gain = np.where(sib_env > 0.085, 0.085 / (sib_env + 1e-9), 1.0)
            data = data - sib * (1.0 - deess_gain) * 0.5
        except Exception:
            pass

    # Stage 5: Transparent TruePeak Limiting (-1.0 dBFS, bảo toàn Crest Factor ~ 8.4)
    peak = np.max(np.abs(data))
    if peak > 1e-4:
        data = data * (0.891 / peak)

    return data.astype(np.float32)


# ------------------------------------------------------------------
# Hệ thống ElevenLabs Audio Effects: Distance (Near/Medium/Far) & Space
# ------------------------------------------------------------------
def apply_audio_effects(audio, sr=24000, distance="Medium", env_filter="Studio (Dry)"):
    if len(audio) == 0:
        return audio
    data = np.asarray(audio, dtype=np.float32).copy()

    # 1. DISTANCE EFFECT (Near / Medium / Far)
    dist = (distance or "Medium").strip()
    try:
        if dist == "Near":
            # Proximity Effect (Sát micro 5-12cm: ấm trầm sâu, chi tiết hơi thở rõ rệt, khô 100%)
            data = biquad_peaking(data, sr, 135.0, +3.5, Q=0.8)
            data = biquad_peaking(data, sr, 1600.0, +1.0, Q=0.9)
            data = biquad_peaking(data, sr, 8500.0, +2.0, Q=0.8)
            data = np.tanh(data * 1.12) / np.tanh(1.12)

        elif dist == "Far":
            # Distant Perspective (Cách micro 2.5 - 3.5 mét: suy hao trầm & treble, phản xạ phòng)
            sos_hp_far = signal.butter(2, 240.0, btype="highpass", fs=sr, output="sos")
            direct = 0.35 * data + 0.65 * signal.sosfilt(sos_hp_far, data)
            sos_lp_far = signal.butter(2, 4200.0, btype="lowpass", fs=sr, output="sos")
            direct = signal.sosfilt(sos_lp_far, direct)
            direct = biquad_peaking(direct, sr, 1800.0, -1.5, Q=0.8)

            taps_ms = [17.0, 29.0, 43.0, 61.0, 83.0, 109.0]
            gains = [0.26, 0.21, 0.16, 0.12, 0.08, 0.05]
            refl = np.zeros_like(direct)
            for t_ms, g in zip(taps_ms, gains):
                d_samp = int((t_ms / 1000.0) * sr)
                if len(direct) > d_samp:
                    refl[d_samp:] += direct[:-d_samp] * g
            sos_damp = signal.butter(1, 3200.0, btype="lowpass", fs=sr, output="sos")
            refl = signal.sosfilt(sos_damp, refl)
            data = (0.62 * direct + 0.38 * refl) * 0.72
    except Exception:
        pass

    # 2. ENVIRONMENT & FILTER EFFECT
    ef = (env_filter or "Studio (Dry)").strip()
    try:
        if ef == "Small Room":
            taps_ms = [11.0, 23.0, 37.0, 53.0]
            gains = [0.18, 0.13, 0.09, 0.05]
            refl = np.zeros_like(data)
            for t_ms, g in zip(taps_ms, gains):
                d_samp = int((t_ms / 1000.0) * sr)
                if len(data) > d_samp:
                    refl[d_samp:] += data[:-d_samp] * g
            sos_damp = signal.butter(1, 4000.0, btype="lowpass", fs=sr, output="sos")
            refl = signal.sosfilt(sos_damp, refl)
            data = 0.82 * data + 0.18 * refl

        elif ef == "Large Hall":
            taps_ms = [29.0, 59.0, 97.0, 149.0, 211.0, 283.0, 367.0]
            gains = [0.24, 0.20, 0.16, 0.13, 0.10, 0.07, 0.05]
            refl = np.zeros_like(data)
            for t_ms, g in zip(taps_ms, gains):
                d_samp = int((t_ms / 1000.0) * sr)
                if len(data) > d_samp:
                    refl[d_samp:] += data[:-d_samp] * g
            sos_damp = signal.butter(1, 2800.0, btype="lowpass", fs=sr, output="sos")
            refl = signal.sosfilt(sos_damp, refl)
            data = 0.70 * data + 0.30 * refl

        elif ef == "Phone Line":
            sos_bp = signal.butter(4, [340.0, 3400.0], btype="bandpass", fs=sr, output="sos")
            data = signal.sosfilt(sos_bp, data)
            data = biquad_peaking(data, sr, 1200.0, +3.0, Q=1.2)
            data = np.tanh(data * 1.8) * 0.75

        elif ef == "Vintage Radio":
            sos_bp = signal.butter(3, [450.0, 2600.0], btype="bandpass", fs=sr, output="sos")
            data = signal.sosfilt(sos_bp, data)
            data = biquad_peaking(data, sr, 1050.0, +4.0, Q=1.5)
            data = np.tanh(data * 2.2) * 0.70

        elif ef == "Megaphone":
            sos_bp = signal.butter(4, [600.0, 4200.0], btype="bandpass", fs=sr, output="sos")
            data = signal.sosfilt(sos_bp, data)
            data = biquad_peaking(data, sr, 2100.0, +5.5, Q=1.4)
            data = np.tanh(data * 2.5) * 0.72
    except Exception:
        pass

    peak = np.max(np.abs(data))
    if peak > 0.95:
        data = data * (0.92 / peak)
    return data.astype(np.float32)


# ------------------------------------------------------------------
# Phân đoạn kịch bản thông minh (Anti-OOM Chunking)
# ------------------------------------------------------------------
def chunk_text(text, max_len=180):
    return split_smart_sentences(text, max_len=max_len)


# ------------------------------------------------------------------
# Xử lý sinh âm thanh (Core Inference Pipeline)
# ------------------------------------------------------------------
VOICE_PROMPT_CACHE = {}

def get_cached_voice_prompt(ref_audio, ref_text):
    if not ref_audio:
        return None
    key = (ref_audio, ref_text or "")
    if key not in VOICE_PROMPT_CACHE:
        try:
            VOICE_PROMPT_CACHE[key] = model.create_voice_clone_prompt(
                ref_audio=ref_audio,
                ref_text=ref_text,
                preprocess_prompt=True,
            )
        except Exception as e:
            print("Warning creating VoiceClonePrompt:", e)
            return None
    return VOICE_PROMPT_CACHE.get(key)


def _run_single(text, lang, speed, stability, similarity, style_exag, model_choice, denoise, emotion="calm", **voice):
    m = MODEL_STEPS.get(model_choice, list(MODEL_STEPS.values())[0])
    steps = m.get("steps", 20)
    base_cfg = m.get("cfg", 2.0)
    base_pos = m.get("pos", 5.0)

    emo = (emotion or "calm").lower()
    emo_prof = EMOTION_PROFILES.get(emo, EMOTION_PROFILES["calm"])

    # Tính toán Guidance Scale & Position Temperature chuẩn OmniVoice
    cfg = float(base_cfg * (0.85 + 0.30 * float(similarity))) * emo_prof["cfg_mult"]
    cfg = float(np.clip(cfg, 1.5, 2.5))

    pos_temp = float(base_pos * (0.80 + 0.40 * float(stability))) * emo_prof["pos_mult"]
    pos_temp = float(np.clip(pos_temp, 3.0, 7.0))

    eff_speed = float(speed) * emo_prof["speed_mult"]
    eff_speed = float(np.clip(eff_speed, 0.70, 1.40))

    kw = dict(
        text=text,
        language=LANG_MAP.get(lang),
        num_step=steps,
        speed=eff_speed,
        denoise=bool(denoise),
        postprocess_output=True,
        guidance_scale=cfg,
        position_temperature=pos_temp,
    )

    # Sử dụng Voice Clone Prompt đã được tiền xử lý & cache
    ref_audio = voice.get("ref_audio")
    ref_text = voice.get("ref_text")
    if ref_audio:
        v_prompt = get_cached_voice_prompt(ref_audio, ref_text)
        if v_prompt is not None:
            kw["voice_clone_prompt"] = v_prompt
        else:
            kw["ref_audio"] = ref_audio
            if ref_text:
                kw["ref_text"] = ref_text

    with torch.inference_mode():
        audio = model.generate(**kw)[0]
    if isinstance(audio, torch.Tensor):
        audio = audio.detach().cpu().numpy()
    audio = np.asarray(audio, dtype=np.float32).squeeze()

    # Áp dụng Emotion DSP
    audio = apply_emotion_dsp(audio, sr=model.sampling_rate, emotion=emo)
    return audio, steps


def save_output(audio, prefix):
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(OUT_DIR, f"{prefix}_{stamp}.wav")
    sf.write(path, audio, model.sampling_rate)
    return path


def history_files():
    files = sorted(glob.glob(os.path.join(OUT_DIR, "*.wav")), key=os.path.getmtime, reverse=True)
    return files[:30]


def status_html(elapsed, dur, steps, chunks=1, label="Đã tạo giọng nói thành công", fx_info="", emotions_used=None):
    chunk_str = f" • {chunks} phân đoạn" if chunks > 1 else ""
    fx_str = f" • 🎛 {fx_info}" if fx_info else ""
    emo_str = ""
    if emotions_used and len(emotions_used) > 0:
        emo_names = sorted(list(set(emotions_used)))
        icons = {"whisper": "🤫", "dramatic": "🎭", "excited": "🔥", "sad": "🌧", "angry": "⚡", "sigh": "💨", "calm": "🌿"}
        emo_badges = " ".join([f'<span class="el-emo-badge-pill">{icons.get(e, "✨")} {e}</span>' for e in emo_names])
        emo_str = f" • {emo_badges}"

    unique_id = f"status_{int(time.time() * 1000)}"
    return f"""
    <div class="el-status-pill auto-dismiss" id="{unique_id}" data-time="10" onmouseenter="pauseDismiss('{unique_id}')" onmouseleave="resumeDismiss('{unique_id}')">
      <div class="el-status-body">
        <span class="dot live-pulse"></span>
        <span class="title">{label}</span>
        <span class="sub">⏱ {elapsed:.1f}s • {dur:.1f}s âm thanh{chunk_str} • {steps} bước{fx_str}{emo_str} • 24 kHz</span>
      </div>
      <div class="el-status-actions">
        <span class="el-countdown-badge" id="{unique_id}_cd" title="Tự động ẩn sau 10 giây">10s</span>
        <button type="button" class="el-status-close-btn" onclick="dismissStatus('{unique_id}')" title="Ẩn ngay">✕</button>
      </div>
      <div class="el-status-progress-track">
        <div class="el-status-progress-bar" id="{unique_id}_bar"></div>
      </div>
    </div>"""


def tts(voice, text, lang, speed, stability, similarity, style_exag, model_choice, denoise, speaker_boost, fx_distance="Medium", fx_env="Studio (Dry)", progress=gr.Progress()):
    if not text or not text.strip():
        raise gr.Error("Vui lòng nhập văn bản cần chuyển thành giọng nói.")
    v = all_voices().get(voice)
    if not v or not os.path.exists(v["audio"]):
        raise gr.Error("Không tìm thấy tệp giọng mẫu đã chọn.")

    # 1. Phân tích kịch bản theo thẻ cảm xúc (Multi-tier Emotion Parsing)
    chunks = parse_and_chunk_script(text.strip(), lang=lang)
    if not chunks:
        chunks = [{"text": text.strip(), "emotion": "calm"}]
    total_chunks = len(chunks)

    t0 = time.time()
    sr = model.sampling_rate
    audio_segments = []
    total_steps = MODEL_STEPS.get(model_choice, {}).get("steps", 14)
    emotions_used = []

    for i, c in enumerate(chunks):
        chunk_text = c["text"]
        chunk_emo = c["emotion"]
        emotions_used.append(chunk_emo)
        prof = EMOTION_PROFILES.get(chunk_emo, EMOTION_PROFILES["calm"])

        # Chuẩn hóa kịch bản (mở rộng số/thời gian/viết tắt để loại bỏ vấp âm)
        norm_chunk = normalize_script(chunk_text, lang=lang)

        # Real-time progress update
        preview = norm_chunk[:30] + ("..." if len(norm_chunk) > 30 else "")
        progress(i / total_chunks, desc=f"Đoạn {i+1}/{total_chunks} • [{chunk_emo.upper()}] • {preview}")

        seg, steps = _run_single(
            norm_chunk, lang, speed, stability, similarity, style_exag,
            model_choice, denoise, emotion=chunk_emo,
            ref_audio=v["audio"], ref_text=v["text"]
        )
        seg = apply_taper(seg, sr, fade_ms=20)
        audio_segments.append(seg)

        # Chèn nhịp thở tự nhiên theo cảm xúc giữa các câu (Palatal Breath Room)
        if i < total_chunks - 1:
            pause_sec = prof["pause_sec"]
            with_breath = prof["breath"]
            c_stripped = norm_chunk.strip()
            if c_stripped.endswith((".", "!", "?")):
                audio_segments.append(natural_pause(sr, duration_sec=pause_sec, with_breath=with_breath))
            elif c_stripped.endswith((",", ";", ":")):
                audio_segments.append(natural_pause(sr, duration_sec=max(0.18, pause_sec * 0.6), with_breath=False))
            else:
                audio_segments.append(natural_pause(sr, duration_sec=max(0.24, pause_sec * 0.8), with_breath=False))

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    progress(0.98, desc="Đang hoàn thiện âm thanh & mastering...")
    full_audio = np.concatenate(audio_segments)
    if speaker_boost:
        full_audio = master_audio(full_audio, sr=sr)

    # 3. Áp dụng ElevenLabs Audio Effects (Distance & Space/Filter)
    full_audio = apply_audio_effects(full_audio, sr=sr, distance=fx_distance, env_filter=fx_env)

    fx_tags = []
    if fx_distance and fx_distance != "Medium":
        fx_tags.append(f"Distance: {fx_distance}")
    if fx_env and fx_env != "Studio (Dry)":
        fx_tags.append(fx_env)
    fx_info = ", ".join(fx_tags)

    path = save_output(full_audio, "tts")
    dur = len(full_audio) / sr
    elapsed = time.time() - t0
    progress(1.0, desc="Đã tạo giọng nói hoàn tất!")
    return path, status_html(elapsed, dur, total_steps, total_chunks, fx_info=fx_info, emotions_used=emotions_used), gr.update(visible=True), history_files()


def voice_change_run(target_voice, audio_file, script_hint, lang, speed, stability, similarity, model_choice, fx_distance="Medium", fx_env="Studio (Dry)", progress=gr.Progress()):
    if not audio_file:
        raise gr.Error("Vui lòng tải lên tệp âm thanh hoặc video cần đổi giọng.")
    v = all_voices().get(target_voice)
    if not v or not os.path.exists(v["audio"]):
        raise gr.Error("Không tìm thấy giọng đích đã chọn.")

    text_to_speak = (script_hint or "").strip()
    if not text_to_speak:
        text_to_speak = v.get("text", "Xin chào, đây là âm thanh đã được chuyển đổi giọng đọc.")

    progress(0.3, desc="Đang đổi giọng...")
    t0 = time.time()
    audio, steps = _run_single(
        text_to_speak, lang, speed, stability, similarity, 0.0,
        model_choice, True,
        ref_audio=v["audio"], ref_text=v["text"]
    )
    audio = master_audio(audio, sr=model.sampling_rate)
    audio = apply_audio_effects(audio, sr=model.sampling_rate, distance=fx_distance, env_filter=fx_env)
    path = save_output(audio, "vc_changer")
    dur = len(audio) / model.sampling_rate
    return path, status_html(time.time() - t0, dur, steps, 1, "Đã đổi giọng thành công"), gr.update(visible=True), history_files()


def char_count(text):
    n = len(text or "")
    return f'<div class="el-count">{n:,} / 5.000 ký tự</div>'


def _slug(name):
    return re.sub(r"[^\w\-]+", "_", name.strip(), flags=re.UNICODE)[:60] or "voice"


def _refresh(value):
    ch = voice_choices()
    return gr.update(choices=ch, value=value), gr.update(choices=ch, value=value)


def clone_create(name, audio, transcript):
    if not name or not name.strip():
        raise gr.Error("Vui lòng đặt tên cho giọng đọc.")
    if not audio:
        raise gr.Error("Vui lòng tải lên hoặc thu âm đoạn mẫu (5–15 giây).")
    if not transcript or not transcript.strip():
        raise gr.Error("Vui lòng nhập đúng nội dung câu thoại trong tệp mẫu.")
    name = name.strip()
    ext = os.path.splitext(audio)[1] or ".wav"
    dst = os.path.join(VOICES_DIR, _slug(name) + ext)
    shutil.copy(audio, dst)
    d = load_custom()
    d[name] = {"audio": dst, "text": transcript.strip(), "desc": "Bản sao giọng nói (Sao chép nhanh)", "type": "cloned", "preset": False, "lang_category": "custom"}
    save_custom(d)
    a, b = _refresh(name)
    msg = f'<div class="el-status-pill"><span class="dot"></span><span class="title">Đã tạo giọng “{name}”</span><span class="sub">Đã kích hoạt trong Đọc văn bản thành tiếng.</span></div>'
    return a, b, msg, gr.update(visible=False), "tts"


def design_generate(gender, age, pitch, accent, script, lang, model_choice, progress=gr.Progress()):
    if not script or not script.strip():
        raise gr.Error("Vui lòng nhập văn bản đọc thử.")
    instruct_tags = f"{gender}, {age}, {pitch}, {accent}"
    progress(0.3, desc=f"Thiết kế giọng đọc...")
    t0 = time.time()
    steps = MODEL_STEPS.get(model_choice, {}).get("steps", 12)
    with torch.inference_mode():
        audio = model.generate(
            text=script.strip(),
            language=LANG_MAP.get(lang),
            num_step=steps,
            instruct=instruct_tags,
            postprocess_output=True,
        )[0]
    if isinstance(audio, torch.Tensor):
        audio = audio.detach().cpu().numpy()
    audio = np.asarray(audio, dtype=np.float32).squeeze()
    audio = master_audio(audio, sr=model.sampling_rate)
    path = save_output(audio, "design")
    dur = len(audio) / model.sampling_rate
    return path, status_html(time.time() - t0, dur, steps, 1, "Đã thiết kế mẫu giọng"), path, script.strip(), history_files()


def design_save(name, path, script):
    if not path:
        raise gr.Error("Vui lòng bấm 'Nghe thử' trước khi lưu.")
    if not name or not name.strip():
        raise gr.Error("Vui lòng đặt tên cho giọng vừa thiết kế.")
    name = name.strip()
    dst = os.path.join(VOICES_DIR, _slug(name) + ".wav")
    shutil.copy(path, dst)
    d = load_custom()
    d[name] = {"audio": dst, "text": script, "desc": "Giọng nhân vật (Thiết kế giọng đọc)", "type": "designed", "preset": False, "lang_category": "custom"}
    save_custom(d)
    a, b = _refresh(name)
    msg = f'<div class="el-status-pill"><span class="dot"></span><span class="title">Đã lưu “{name}”</span><span class="sub">Có thể chọn ngay trong phần Cài đặt.</span></div>'
    return a, b, msg, gr.update(visible=False)


def lib_preview(voice):
    v = all_voices().get(voice)
    if not v:
        return None, ""
    kind = "Mặc định hệ thống" if v.get("preset") else "Giọng của bạn"
    info = f"""
    <div class="el-voice-badge">
      <div class="orb-thumb"></div>
      <div>
        <div class="name">{voice}</div>
        <div class="meta">{v.get("desc", "")} • <b>{kind}</b></div>
        <div class="quote">“{v["text"]}”</div>
      </div>
    </div>"""
    return v["audio"], info


def lib_delete(voice):
    d = load_custom()
    if voice not in d:
        raise gr.Error("Không thể xóa các giọng đọc mặc định của hệ thống.")
    try:
        os.remove(d[voice]["audio"])
    except Exception:
        pass
    del d[voice]
    save_custom(d)
    first = voice_choices()[0]
    a, b = _refresh(first)
    return a, b


def render_voice_library_html(filter_type="Tất cả", search_q=""):
    voices = all_voices()
    html_cards = []
    sq = (search_q or "").strip().lower()

    for name, data in voices.items():
        vtype = data.get("type", "default")
        lcat = data.get("lang_category", "en")

        accent = data.get("accent", "")
        gender = data.get("gender", "")
        if not accent:
            if "US" in name or "Mỹ" in name or "American" in name:
                accent = "American"
            elif "UK" in name or "Anh" in name or "British" in name:
                accent = "British"
        if not gender:
            if "Nam" in name or "Male" in name:
                gender = "male"
            elif "Nữ" in name or "Female" in name:
                gender = "female"

        if filter_type == "US English (Mỹ)" and accent != "American":
            continue
        if filter_type == "UK English (Anh)" and accent != "British":
            continue
        if filter_type == "Nam (Male)" and gender != "male":
            continue
        if filter_type == "Nữ (Female)" and gender != "female":
            continue
        if filter_type == "Tiếng Việt" and lcat != "vi":
            continue
        if filter_type == "Giọng tự tạo" and vtype in ["default", "elevenlabs"]:
            continue

        desc = data.get("desc", "")
        text = data.get("text", "")
        if sq and (sq not in name.lower() and sq not in desc.lower() and sq not in text.lower()):
            continue

        is_default = data.get("preset", False)
        type_badge = "ElevenLabs Original" if vtype == "elevenlabs" else ("Hệ thống" if is_default else ("Đã sao chép" if vtype == "cloned" else "Đã thiết kế"))
        audio_path = data.get("audio", "").replace("\\", "/")
        audio_url = f"/gradio_api/file={audio_path}"

        html_cards.append(f"""
        <div class="vlib-card" data-voice="{name}">
          <div class="vlib-left">
            <div class="vlib-orb"></div>
            <div class="vlib-meta">
              <div class="vlib-name-row">
                <span class="vlib-name">{name}</span>
                <span class="vlib-tag">{type_badge}</span>
              </div>
              <div class="vlib-tags-sub">{desc}</div>
              <div class="vlib-quote">“{text}”</div>
            </div>
          </div>
          <div class="vlib-actions">
            <button class="vlib-play-circle-btn" onclick="playVoicePreview('{audio_url}', this)" title="Bấm nghe thử giọng {name}">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 3 20 12 6 21 6 3"/></svg>
            </button>
            <button class="vlib-use-btn" onclick="selectVoiceLib('{name}')">Dùng cho Đọc kịch bản</button>
          </div>
        </div>
        """)

    if not html_cards:
        return '<div class="vlib-empty">Không tìm thấy giọng đọc nào phù hợp.</div>'
    return "".join(html_cards)


TOOL_LABELS = {
    "tts": "Đọc kịch bản (Text to Speech)",
    "vc": "Tạo giọng mới (Clone & Design)",
    "changer": "Đổi giọng (Voice Changer)",
    "lib": "Kho giọng đọc (Voice Library)",
}


def topbar(page):
    return f"""
    <div class="el-topbar">
      <div class="crumb">
        <span class="brand-square">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m16 6 4 14"/><path d="M12 6v14"/><path d="M8 8v12"/><path d="M4 4v16"/></svg>
        </span>
        <span class="brand-text">Thành Âm</span>
        <span class="divider">/</span>
        <span class="crumb-title">{TOOL_LABELS.get(page, '')}</span>
      </div>

      <div class="topbar-center">
        <div class="topbar-search" title="Tìm kiếm (⌘K)">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#888" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
          <span class="search-placeholder">Tìm kiếm...</span>
          <span class="search-kbd">⌘K</span>
        </div>
      </div>

      <div class="actions">
        <span class="top-status-badge"><span class="live-dot"></span> GTX 1650 FP16</span>
        <a href="https://elevenlabs.io/docs" target="_blank" class="header-text-btn" title="Xem tài liệu ElevenLabs">Tài liệu</a>
        <button class="header-text-btn" onclick="alert('Thành Âm Studio v2.0 • Local RTX/GTX AI Voice')" title="Trợ giúp & Phản hồi">Hỗ trợ</button>
        <button class="header-icon-btn" title="Thư mục dự án" onclick="alert('Thư mục xuất âm thanh: E:\\VoiceAI\\outputs')">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#171717" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/></svg>
        </button>
        <button class="header-icon-btn" title="Thông báo hệ thống" onclick="alert('Hệ thống hoạt động bình thường • CUDA FP16 sẵn sàng')">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#171717" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>
        </button>
      </div>
    </div>"""


# ------------------------------------------------------------------
# Thiết kế UI/UX Tiếng Việt "Thành Âm" (100% Gọn Gàng - Không Lớp Vỏ Rác)
# ------------------------------------------------------------------
CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root, body, gradio-app, .gradio-container, .gradio-container.dark {
  --bg: #ffffff;
  --surface: #f7f7f8;
  --surface-clean: #fafafa;
  --border: #e7e7e7;
  --border-strong: #d9d9d9;
  --text: #171717;
  --text-muted: #666666;
  --text-faint: #999999;
  --radius-card: 20px;
  --radius-control: 10px;
  --radius-pill: 999px;
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, system-ui, sans-serif;
  color-scheme: light !important;
}

html, body, gradio-app, .gradio-container {
  margin: 0 !important;
  padding: 0 !important;
  max-width: 100% !important;
  width: 100% !important;
  min-height: 100vh !important;
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: var(--font-sans) !important;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}
footer { display: none !important; }

#shell {
  margin: 0 !important;
  padding: 0 !important;
  gap: 0 !important;
  width: 100% !important;
  max-width: 100% !important;
  min-height: 100vh !important;
  display: flex !important;
  flex-direction: row !important;
  flex-wrap: nowrap !important;
  background: #ffffff !important;
}

/* 1. TOP STATUS / PROMO BANNER (Dính sát mép trên full-width) */
#thanham-top-banner.el-banner {
  background: #18181b;
  color: #ffffff !important;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 500;
  padding: 7px 16px;
  width: 100% !important;
  max-width: 100% !important;
  position: relative;
  box-sizing: border-box;
  margin: 0 !important;
  border-radius: 0 !important;
  z-index: 1000;
}
.el-banner-content { display: flex; align-items: center; justify-content: center; gap: 8px; }
.el-banner-content .banner-btn {
  background: #ffffff;
  color: #2e66ca !important;
  padding: 2px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
}
.el-banner-close {
  position: absolute;
  right: 14px;
  background: transparent;
  border: none;
  color: #ffffff;
  font-size: 14px;
  cursor: pointer;
  padding: 4px 8px;
  line-height: 1;
}

/* 2. SIDEBAR GỌN GÀNG (Cao full viewport dính mép trái, border-right 1px #e7e7e7) */
#sidebar {
  background: #fafafa !important;
  border-right: 1px solid var(--border) !important;
  border-left: none !important;
  border-top: none !important;
  border-bottom: none !important;
  border-radius: 0 !important;
  padding: 16px 12px 14px 12px !important;
  min-height: 100vh !important;
  height: 100vh !important;
  position: sticky !important;
  top: 0 !important;
  box-sizing: border-box !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: flex-start !important;
  gap: 12px !important;
  flex-shrink: 0 !important;
}
.el-logo-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 6px 14px;
  font-size: 15px;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: #18181b !important;
  border-bottom: 1px solid #e4e4e7;
  margin-bottom: 6px;
}
.el-logo-brand span {
  color: #18181b !important;
  font-weight: 700 !important;
}
.brand-square {
  width: 28px;
  height: 28px;
  background: #171717;
  color: #ffffff !important;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 800;
}
.sidebar-group-title {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--text-faint) !important;
  padding: 8px 8px 6px;
  letter-spacing: 0.05em;
}

/* Nav Radio: Item cao ~36px, font 14px/500, radius 8px, gap 4px. Active = nền #efefef, Hover = #f5f5f5 */
#nav {
  display: flex !important;
  flex-direction: column !important;
  gap: 4px !important;
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
}
#nav .wrap {
  display: flex !important;
  flex-direction: column !important;
  gap: 4px !important;
}
#nav label {
  display: flex !important;
  align-items: center !important;
  gap: 10px !important;
  height: 36px !important;
  min-height: 36px !important;
  padding: 0 10px !important;
  border-radius: 8px !important;
  font-size: 14px !important;
  font-weight: 500 !important;
  color: var(--text) !important;
  cursor: pointer !important;
  background: transparent !important;
  border: none !important;
  margin: 0 !important;
  transition: background 0.15s ease, color 0.15s ease !important;
}
#nav label:hover {
  background: #f5f5f5 !important;
}
#nav label.selected, #nav label:has(input:checked) {
  background: #efefef !important;
  color: #171717 !important;
  font-weight: 600 !important;
}
#nav input[type="radio"] { display: none !important; }

/* SVG Line Icons đơn sắc thống nhất cho 4 Workspace (18px, stroke 1.5, #171717) */
#nav label::before {
  content: "";
  display: inline-block;
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
}
/* 1. Đọc kịch bản: Sound wave */
#nav label:has(input[value="tts"])::before,
#nav .wrap > label:nth-child(1)::before {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%23171717' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M2 10v3'/%3E%3Cpath d='M6 6v11'/%3E%3Cpath d='M10 3v18'/%3E%3Cpath d='M14 8v7'/%3E%3Cpath d='M18 5v13'/%3E%3Cpath d='M22 10v3'/%3E%3C/svg%3E");
}
/* 2. Tạo giọng mới: Sparkles */
#nav label:has(input[value="vc"])::before,
#nav .wrap > label:nth-child(2)::before {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%23171717' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3L12 3Z'/%3E%3Cpath d='M5 3v4'/%3E%3Cpath d='M19 17v4'/%3E%3C/svg%3E");
}
/* 3. Đổi giọng: Refresh cycle */
#nav label:has(input[value="changer"])::before,
#nav .wrap > label:nth-child(3)::before {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%23171717' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8'/%3E%3Cpath d='M3 3v5h5'/%3E%3Cpath d='M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16'/%3E%3Cpath d='M16 21h5v-5'/%3E%3C/svg%3E");
}
/* 4. Kho giọng đọc: Layout grid */
#nav label:has(input[value="lib"])::before,
#nav .wrap > label:nth-child(4)::before {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%23171717' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect width='7' height='7' x='3' y='3' rx='1'/%3E%3Crect width='7' height='7' x='14' y='3' rx='1'/%3E%3Crect width='7' height='7' x='14' y='14' rx='1'/%3E%3Crect width='7' height='7' x='3' y='14' rx='1'/%3E%3C/svg%3E");
}

/* 3. USER-SELECT: NONE (Chống bôi xanh vô ý cho sidebar, nút, tab, nhãn) */
#sidebar,
#sidebar *,
button,
.btn-black,
.btn-ghost,
.btn-reset,
.el-banner,
.el-topbar,
.el-topbar *,
.tab-nav,
.tab-nav button,
#nav label,
.sidebar-group-title,
.el-slider-head,
.el-row-label,
.el-format-pill {
  user-select: none !important;
  -webkit-user-select: none !important;
}

/* 4. THẺ GPU + LAN_URL Ở ĐÁY SIDEBAR (radius 12px, border #e7e7e7, chữ nhỏ) */
.sidebar-bottom {
  margin-top: auto !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 8px !important;
  padding-top: 14px !important;
  border-top: 1px solid var(--border) !important;
}
.el-side-card {
  background: #ffffff !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  padding: 8px 10px !important;
  font-size: 11px !important;
  color: var(--text-muted) !important;
}
.el-side-card b {
  display: block;
  color: var(--text) !important;
  font-size: 11.5px;
  font-weight: 600;
  margin-bottom: 2px;
}
.el-side-card .live {
  color: #16a34a;
  font-weight: 600;
}
.el-side-card code {
  background: #f4f4f5;
  color: #18181b;
  font-family: monospace;
  font-size: 10.5px;
  padding: 1px 5px;
  border-radius: 4px;
  margin-top: 2px;
  display: inline-block;
  user-select: text !important;
  -webkit-user-select: text !important;
}

/* 5. WORKSPACE TOPBAR & HEADER */
.el-topbar {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 16px !important;
  padding: 0 20px !important;
  border-bottom: 1px solid var(--border) !important;
  background: #ffffff !important;
  height: 52px !important;
  min-height: 52px !important;
  box-sizing: border-box !important;
}
.el-topbar .crumb {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}
.el-topbar .crumb .brand-text { font-weight: 700; font-size: 14px; color: #171717; }
.el-topbar .crumb .divider { color: #cccccc; margin: 0 4px; }
.el-topbar .crumb .crumb-title { font-weight: 500; font-size: 13.5px; color: #444444; }

.topbar-center {
  flex: 1;
  max-width: 340px;
  display: flex;
  justify-content: center;
}
.topbar-search {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f4f4f5;
  border: 1px solid var(--border);
  border-radius: var(--radius-pill);
  padding: 5px 12px;
  font-size: 12.5px;
  color: var(--text-faint);
  cursor: pointer;
  width: 100%;
  max-width: 260px;
  transition: all 0.15s ease;
}
.topbar-search:hover {
  background: #ebebed;
  border-color: #d1d1d6;
}
.topbar-search .search-placeholder {
  flex: 1;
  color: #71717a;
}
.topbar-search .search-kbd {
  background: #ffffff;
  border: 1px solid #d4d4d8;
  border-radius: 4px;
  font-size: 10.5px;
  font-weight: 600;
  padding: 1px 5px;
  color: #71717a;
  line-height: 1.2;
}

.el-topbar .actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.header-text-btn {
  background: transparent;
  border: none;
  font-size: 12.5px;
  font-weight: 500;
  color: #52525b;
  padding: 6px 10px;
  border-radius: 6px;
  text-decoration: none;
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease;
}
.header-text-btn:hover {
  background: #f4f4f5;
  color: #18181b;
}

.header-icon-btn {
  width: 36px !important;
  height: 36px !important;
  min-width: 36px !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  background: #ffffff !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  color: #171717 !important;
  cursor: pointer !important;
  padding: 0 !important;
  transition: all 0.15s ease !important;
  box-shadow: none !important;
}
.header-icon-btn:hover {
  background: #f4f4f5 !important;
  border-color: #d4d4d8 !important;
}

.top-status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: var(--radius-pill);
  padding: 4px 10px;
  font-size: 11.5px;
  font-weight: 500;
  color: #166534;
}
.live-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #22c55e;
}
  font-weight: 500;
  color: #166534;
}
.live-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #22c55e;
}

#main { gap: 0 !important; padding: 0 !important; }
#workspace { gap: 0 !important; flex-wrap: nowrap; }

/* Center Canvas */
#center {
  padding: 24px 44px !important;
  max-width: 1080px;
  margin: 0 auto;
  width: 100%;
  min-height: calc(100vh - 90px);
  background: #ffffff !important;
}
#script, #script > * { border: none !important; background: transparent !important; box-shadow: none !important; }
#script textarea {
  border: none !important;
  box-shadow: none !important;
  font-size: 16px !important;
  line-height: 1.7 !important;
  color: var(--text) !important;
  padding: 0 !important;
  resize: vertical !important;
  background: transparent !important;
  font-family: var(--font-sans) !important;
}
#script textarea::placeholder { color: #8a8a8a !important; font-weight: 400 !important; }

.el-gs {
  font-size: 12px;
  font-weight: 500;
  color: #777777;
  margin-top: 20px;
  margin-bottom: 10px;
}
.chips {
  display: flex !important;
  flex-wrap: wrap !important;
  gap: 8px !important;
}
.chips button {
  background: #ffffff !important;
  border: 1px solid #e3e3e3 !important;
  border-radius: 8px !important;
  padding: 6px 12px !important;
  font-size: 12px !important;
  color: #222222 !important;
  font-weight: 400 !important;
  transition: all 0.15s ease !important;
  cursor: pointer !important;
  box-shadow: none !important;
}
.chips button:hover {
  background: #f7f7f7 !important;
  border-color: #d1d1d1 !important;
  color: #000000 !important;
}

.el-bottom {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  margin-top: 24px !important;
  padding-top: 14px !important;
  border-top: 1px solid var(--border) !important;
}
.el-count { font-size: 11.5px; color: #888888; }

.btn-black, .btn-black:hover {
  background: #171717 !important;
  color: #ffffff !important;
  border: none !important;
  border-radius: 8px !important;
  font-weight: 500 !important;
  font-size: 13px !important;
  padding: 8px 18px !important;
  transition: all 0.15s ease !important;
}
.btn-black * { color: #ffffff !important; }
.btn-black:hover { background: #2a2a2a !important; }

.btn-ghost {
  background: #ffffff !important;
  color: #171717 !important;
  border: 1px solid #d9d9d9 !important;
  border-radius: 8px !important;
  font-weight: 500 !important;
  font-size: 12.5px !important;
  padding: 8px 16px !important;
  transition: all 0.15s ease !important;
}
.btn-ghost * { color: #171717 !important; }
.btn-ghost:hover { background: #fafafa !important; }

/* Output Dock */
.el-output-card {
  margin-top: 18px !important;
  background: #ffffff !important;
  border: 1.5px solid #e4e4e7 !important;
  border-radius: 14px !important;
  padding: 16px 20px !important;
  box-shadow: 0 2px 8px rgba(0,0,0,0.03) !important;
  transition: all 0.2s ease !important;
}
.el-output-card:hover {
  border-color: #cbd5e1 !important;
}
.el-status-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #f5f7fb;
  border: 1px solid #e2e8f0;
  border-radius: var(--radius-pill);
  padding: 5px 14px;
  font-size: 12px;
  margin-bottom: 10px;
}
.el-status-pill .dot { width: 8px; height: 8px; border-radius: 50%; background: #22c55e; }
.el-status-pill .title { font-weight: 600; color: #0f172a; }
.el-status-pill .sub { color: #64748b; font-size: 11.5px; margin-left: 4px; }

/* Model Cards Selector & Meta */
#model_cards_radio .wrap {
  display: flex !important;
  flex-direction: column !important;
  gap: 6px !important;
}
#model_cards_radio label {
  display: flex !important;
  align-items: center !important;
  padding: 8px 12px !important;
  border: 1px solid #e4e4e7 !important;
  border-radius: 8px !important;
  background: #ffffff !important;
  cursor: pointer !important;
  transition: all 0.15s ease !important;
  font-size: 12px !important;
  font-weight: 500 !important;
  color: #18181b !important;
  margin: 0 !important;
}
#model_cards_radio label span,
#model_cards_radio span,
#model_cards_radio .wrap label {
  color: #18181b !important;
  font-weight: 500 !important;
}
#model_cards_radio label:hover {
  background: #f8fafc !important;
  border-color: #cbd5e1 !important;
}
#model_cards_radio label.selected, #model_cards_radio label:has(input:checked) {
  border-color: #0f172a !important;
  background: #f8fafc !important;
  font-weight: 600 !important;
}
.el-model-meta-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 10px 12px;
  margin-top: 8px;
  margin-bottom: 12px;
}
.m-head-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}
.m-badge-active {
  font-size: 10.5px;
  font-weight: 600;
  color: #166534;
  background: #dcfce7;
  border-radius: 4px;
  padding: 1px 6px;
}
.m-speed {
  font-size: 11px;
  font-weight: 500;
  color: #0f172a;
}
.m-desc {
  font-size: 11.5px;
  color: #334155;
  line-height: 1.45;
  margin-bottom: 8px;
}
.m-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}
.m-tag {
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 4px;
  font-size: 10px;
  font-weight: 500;
  color: #475569;
  padding: 1px 6px;
}

/* Voice Preview Card & Lib Dock */
.el-sample-quote-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 10px 12px;
  margin: 6px 0 10px;
}
.s-head-row {
  display: flex !important;
  align-items: center !important;
  gap: 12px !important;
}
.s-meta-col {
  display: flex !important;
  flex-direction: column !important;
  gap: 3px !important;
  flex: 1 !important;
}
.el-sample-quote-card .s-desc {
  font-weight: 600;
  font-size: 12px;
  color: #0f172a;
}
.el-sample-quote-card .s-quote {
  font-style: italic;
  color: #64748b;
  font-size: 11.5px;
  line-height: 1.35;
}

/* Circular Black Play Button (ElevenLabs Style) */
.voice-circle-play-btn,
.vlib-play-circle-btn {
  width: 36px !important;
  height: 36px !important;
  min-width: 36px !important;
  border-radius: 50% !important;
  background: #171717 !important;
  color: #ffffff !important;
  border: none !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  cursor: pointer !important;
  flex-shrink: 0 !important;
  transition: transform 0.15s ease, background 0.15s ease, box-shadow 0.15s ease !important;
  box-shadow: 0 2px 6px rgba(0,0,0,0.12) !important;
  padding: 0 !important;
  user-select: none !important;
}
.voice-circle-play-btn:hover,
.vlib-play-circle-btn:hover {
  background: #000000 !important;
  transform: scale(1.08) !important;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2) !important;
}
.voice-circle-play-btn:active,
.vlib-play-circle-btn:active {
  transform: scale(0.96) !important;
}
.voice-circle-play-btn.playing,
.vlib-play-circle-btn.playing {
  background: #2563eb !important;
  box-shadow: 0 0 0 3px rgba(37,99,235,0.25) !important;
}

.el-lib-preview-dock {
  background: #fcfcfd !important;
  border: 1.5px solid #e2e8f0 !important;
  border-radius: 14px !important;
  padding: 16px 18px !important;
  margin-bottom: 20px !important;
  box-shadow: 0 1px 4px rgba(0,0,0,0.02) !important;
}



/* 4. WORKSPACE TẠO GIỌNG ĐỌC */
.el-h1 {
  font-size: 22px;
  font-weight: 600;
  letter-spacing: -0.02em;
  margin: 0 0 6px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #171717 !important;
}
.el-sub { font-size: 13px; color: #6f6f6f; margin-bottom: 18px; }

.vc-card-clean {
  background: var(--surface) !important;
  border: 1px solid #e5e5e7 !important;
  border-radius: var(--radius-card) !important;
  padding: 22px !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: space-between !important;
  height: 380px !important;
  box-sizing: border-box !important;
}
.vc-title { font-size: 16px; font-weight: 600; color: #191919 !important; margin-bottom: 4px; }
.vc-desc { font-size: 13px; color: #6f6f6f !important; line-height: 1.45; min-height: 40px; }

.orb-container {
  position: relative;
  width: 140px;
  height: 140px;
  margin: 12px auto;
  display: flex;
  align-items: center;
  justify-content: center;
}
.orb {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: inset 0 0 25px rgba(255,255,255,0.7), 0 8px 24px rgba(0,0,0,0.06);
}
.orb.sky {
  background: radial-gradient(circle at 35% 25%, #ffffff 0%, #b8e1fc 30%, #50a7f2 70%, #1a6cb8 100%);
}
.orb.navy {
  background: radial-gradient(circle at 35% 25%, #7ea2d4 0%, #304c78 40%, #0d1e3a 80%, #050b17 100%);
}

.play-center {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: rgba(255,255,255,0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #171717;
  font-size: 11px;
}

.orb-range {
  display: flex;
  justify-content: space-between;
  border-top: 1px solid #e5e5e5;
  padding-top: 10px;
  margin-top: 4px;
}
.sub-lbl { font-size: 11px; color: #858585; display: block; }
.val-lbl { font-size: 12px; font-weight: 600; color: #1f1f1f; display: block; }

/* 5. WORKSPACE ĐỔI GIỌNG */
.dropzone-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 1px dashed #bdbdbd;
  background: #fcfcfc;
  border-radius: 16px;
  padding: 32px 24px;
  text-align: center;
  transition: all 0.15s ease;
  max-width: 560px;
  margin: 20px auto 0;
}
.dropzone-box:hover { border-color: #4381f5; background: #f4f8ff; }

/* 6. WORKSPACE KHO GIỌNG ĐỌC */
.vlib-top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 16px;
}
.vlib-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 12px 18px;
  transition: all 0.12s ease;
  margin-bottom: 8px;
}
.vlib-card:hover {
  background: #f5f5f5 !important;
  border-color: var(--border-strong);
}
.vlib-left { display: flex; align-items: center; gap: 14px; flex: 1; min-width: 0; }
.vlib-orb {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  flex-shrink: 0;
  background: radial-gradient(circle at 30% 25%, #e6ffff 0%, #75e8fa 22%, #23a8f4 52%, #526ef7 78%, #d1fbf1 100%);
}
.vlib-meta { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
.vlib-name-row { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.vlib-name { font-size: 14px; font-weight: 600; color: #171717; }
.vlib-tag {
  background: #f4f4f5;
  border: 1px solid var(--border);
  border-radius: var(--radius-pill);
  padding: 2px 8px;
  font-size: 10px;
  color: #666666;
}
.vlib-tags-sub { font-size: 12px; color: #71717a; }
.vlib-quote { font-size: 12px; color: #a1a1aa; font-style: italic; max-width: 480px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.vlib-actions {
  display: flex !important;
  align-items: center !important;
  gap: 10px !important;
  flex-shrink: 0 !important;
}
.vlib-use-btn {
  background: #ffffff;
  border: 1px solid #d4d4d8;
  border-radius: 8px;
  padding: 7px 14px;
  font-size: 12.5px;
  font-weight: 500;
  color: #18181b;
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}
.vlib-use-btn:hover { background: #18181b; color: #ffffff; border-color: #18181b; }

/* 7. INSPECTOR */
#inspector {
  background: #ffffff !important;
  border-left: 1px solid var(--border) !important;
  padding: 18px 18px !important;
  height: calc(100vh - 50px);
  overflow-y: auto;
  box-sizing: border-box;
}
#inspector .tab-nav {
  border-bottom: 1px solid var(--border) !important;
  gap: 16px !important;
  margin-bottom: 12px !important;
}
#inspector button[role="tab"] {
  background: transparent !important;
  border: none !important;
  border-bottom: 2px solid transparent !important;
  color: #777777 !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  padding: 6px 2px !important;
  border-radius: 0 !important;
}
#inspector button[role="tab"][aria-selected="true"] {
  color: #171717 !important;
  border-bottom: 2px solid #171717 !important;
  font-weight: 600 !important;
}

.el-sec-title {
  font-size: 12px;
  font-weight: 500;
  color: #252525 !important;
  margin: 14px 0 6px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.el-pill-dd {
  border: 1px solid #e1e1e1 !important;
  border-radius: 11px !important;
  background: #ffffff !important;
  padding: 2px 6px !important;
}

/* ==================== 18. ELEVENLABS SLIDERS (INSPECTOR) ==================== */
.el-slider-head {
  margin-top: 14px;
  margin-bottom: 2px;
}
.el-slider-head .title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12.5px;
  font-weight: 500;
  color: #171717 !important;
  margin-bottom: 2px;
}
.el-slider-val {
  font-size: 11px;
  font-weight: 600;
  color: #171717 !important;
  background: #f0f0f2;
  padding: 1px 6px;
  border-radius: 6px;
  font-variant-numeric: tabular-nums;
  border: 1px solid #e4e4e7;
}
.el-slider-head .sub-row {
  display: flex;
  justify-content: space-between;
  font-size: 10px;
  color: #8e8e93 !important;
}

.el-clean-slider {
  --slider-color: #171717 !important;
  margin: 0 0 6px !important;
  padding: 0 !important;
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}

.el-clean-slider .head,
.el-clean-slider label,
.el-clean-slider button,
.el-clean-slider .min_value,
.el-clean-slider .max_value,
.el-clean-slider .tab-like-container,
.el-clean-slider input[type="number"] {
  display: none !important;
}

/* Đảm bảo ô input có chiều cao 22px để thumb tròn 15px không bị browser cắt cụt */
.el-clean-slider input[type="range"] {
  -webkit-appearance: none !important;
  appearance: none !important;
  width: 100% !important;
  height: 22px !important;
  background: transparent !important;
  cursor: pointer !important;
  outline: none !important;
  border: none !important;
  padding: 0 !important;
  margin: 0 !important;
  display: block !important;
}

/* Track mảnh thanh lịch ElevenLabs (4px) */
.el-clean-slider input[type="range"]::-webkit-slider-runnable-track {
  height: 4px !important;
  border-radius: 999px !important;
  background: linear-gradient(to right, #171717 var(--range_progress, 0%), #e5e5e7 var(--range_progress, 0%)) !important;
  border: none !important;
}

/* Thumb tròn đen ElevenLabs nổi bật (15px), viền trắng 2.5px */
.el-clean-slider input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none !important;
  appearance: none !important;
  width: 15px !important;
  height: 15px !important;
  border-radius: 50% !important;
  background-color: #171717 !important;
  border: 2.5px solid #ffffff !important;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3) !important;
  margin-top: -5.5px !important;
  cursor: grab !important;
  transition: transform 0.12s ease, box-shadow 0.12s ease !important;
}

.el-clean-slider input[type="range"]::-webkit-slider-thumb:hover {
  transform: scale(1.18);
  box-shadow: 0 2px 7px rgba(0, 0, 0, 0.45) !important;
}

.el-clean-slider input[type="range"]::-webkit-slider-thumb:active {
  cursor: grabbing !important;
  transform: scale(1.25);
}

/* Firefox Support */
.el-clean-slider input[type="range"]::-moz-range-track {
  height: 4px !important;
  border-radius: 999px !important;
  background: #e5e5e7 !important;
  border: none !important;
}

.el-clean-slider input[type="range"]::-moz-range-progress {
  height: 4px !important;
  border-radius: 999px !important;
  background-color: #171717 !important;
}

.el-clean-slider input[type="range"]::-moz-range-thumb {
  width: 15px !important;
  height: 15px !important;
  border-radius: 50% !important;
  background-color: #171717 !important;
  border: 2.5px solid #ffffff !important;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3) !important;
  cursor: grab !important;
}

/* Toggle Switches */
.el-row-item {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  margin-top: 10px !important;
  padding: 2px 0 !important;
}
.el-row-label {
  font-size: 12px;
  font-weight: 500;
  color: #252525 !important;
}
.el-format-pill {
  background: #f4f4f5;
  border-radius: var(--radius-pill);
  padding: 3px 10px;
  font-size: 11px;
  font-weight: 500;
  color: #18181b !important;
}

.el-switch label {
  display: flex !important;
  align-items: center !important;
  justify-content: flex-end !important;
  margin: 0 !important;
  cursor: pointer;
}
.el-switch label span { display: none !important; }
.el-switch input[type="checkbox"] {
  appearance: none !important;
  -webkit-appearance: none !important;
  width: 36px !important;
  height: 20px !important;
  background: #dedede !important;
  border-radius: var(--radius-pill) !important;
  position: relative !important;
  cursor: pointer !important;
  border: none !important;
  transition: background 0.2s ease !important;
}
.el-switch input[type="checkbox"]::after {
  content: "";
  position: absolute;
  top: 2px;
  left: 2px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #ffffff;
  box-shadow: 0 1px 2px rgba(0,0,0,0.2);
  transition: transform 0.2s ease;
}
.el-switch input[type="checkbox"]:checked { background: #191919 !important; }
.el-switch input[type="checkbox"]:checked::after { transform: translateX(16px); }

.el-reset-row {
  display: flex !important;
  justify-content: flex-end !important;
  margin-top: 14px !important;
}
.btn-reset {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  color: #666666 !important;
  font-size: 11.5px !important;
  font-weight: 500 !important;
  padding: 4px 8px !important;
  cursor: pointer;
}
.btn-reset:hover { background: #f4f4f5 !important; border-radius: 6px !important; color: #171717 !important; }

/* ==================== 19. ELEVENLABS AUDIO EFFECTS (DISTANCE & SPACE) ==================== */
#fx_distance_input, #fx_env_input {
  display: none !important;
}
.el-fx-section {
  margin-top: 14px;
  margin-bottom: 10px;
  border-top: 1px solid #f0f0f2;
  padding-top: 12px;
  user-select: none;
}
.el-fx-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  margin-bottom: 8px;
}
.el-fx-title {
  font-size: 12.5px;
  font-weight: 500;
  color: #171717 !important;
}
.el-fx-chevron {
  color: #71717a;
  transition: transform 0.2s ease;
}
.el-fx-section.collapsed .el-fx-chevron {
  transform: rotate(-90deg);
}
.el-fx-section.collapsed .el-fx-body {
  display: none;
}
.el-fx-body {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.el-fx-row {
  position: relative;
  display: flex;
  align-items: center;
  height: 36px;
  background: #ffffff;
  border: 1px solid #e4e4e7;
  border-radius: 10px;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
.el-fx-row:hover {
  border-color: #d4d4d8;
}
.el-fx-label-cell {
  display: flex;
  align-items: center;
  gap: 7px;
  width: 104px;
  min-width: 104px;
  height: 100%;
  padding: 0 10px;
  border-right: 1px solid #e4e4e7;
  color: #71717a !important;
  font-size: 12.5px;
  font-weight: 400;
}
.el-fx-label-cell svg {
  color: #71717a;
  flex-shrink: 0;
}
.el-fx-select-cell {
  flex: 1;
  height: 100%;
  padding: 0 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12.5px;
  font-weight: 500;
  color: #18181b !important;
  cursor: pointer;
  transition: background 0.12s ease;
}
.el-fx-select-cell:hover,
.el-fx-select-cell.open {
  background: #ececee;
}
.el-fx-select-cell .fx-dd-arrow {
  color: #52525b;
  transition: transform 0.18s ease;
}
.el-fx-select-cell.open .fx-dd-arrow {
  transform: rotate(180deg);
}
.el-fx-remove-cell {
  width: 34px;
  min-width: 34px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-left: 1px solid #e4e4e7;
  color: #71717a;
  cursor: pointer;
  border-top-right-radius: 9px;
  border-bottom-right-radius: 9px;
  transition: background 0.12s ease, color 0.12s ease;
}
.el-fx-remove-cell:hover {
  background: #fef2f2;
  color: #dc2626;
}
.el-fx-popover {
  display: none;
  position: absolute;
  top: calc(100% + 5px);
  left: 103px;
  right: 33px;
  background: #ffffff;
  border: 1px solid #e4e4e7;
  border-radius: 12px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.14), 0 4px 10px -2px rgba(0, 0, 0, 0.06);
  padding: 4px;
  z-index: 1000;
}
.el-fx-popover.show {
  display: block;
}
.el-fx-opt {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 7px 10px;
  border-radius: 8px;
  font-size: 12.5px;
  font-weight: 400;
  color: #18181b !important;
  cursor: pointer;
  transition: background 0.1s ease;
}
.el-fx-opt:hover {
  background: #f4f4f5;
}
.el-fx-opt.active {
  background: #f4f4f5;
  font-weight: 500;
}
.el-fx-opt .fx-check {
  opacity: 0;
  color: #18181b;
}
.el-fx-opt.active .fx-check {
  opacity: 1;
}
.el-fx-add-btn {
  display: none;
  align-items: center;
  justify-content: center;
  gap: 6px;
  height: 32px;
  border: 1px dashed #d4d4d8;
  border-radius: 9px;
  background: #fafafa;
  color: #52525b !important;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
}
.el-fx-add-btn:hover {
  border-color: #18181b;
  color: #18181b !important;
  background: #f4f4f5;
}

/* Sliding creation panels */
.el-creation-panel {
  margin-top: 20px !important;
  background: #ffffff !important;
  border: 1px solid var(--border) !important;
  border-radius: 16px !important;
  padding: 20px 24px !important;
  box-shadow: 0 4px 16px rgba(0,0,0,0.03) !important;
}
.el-panel-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border);
  padding-bottom: 10px;
  margin-bottom: 14px;
}
.el-panel-head b { font-size: 15px; color: #171717 !important; }

@media (max-width: 1100px) {
  #shell, #workspace { flex-wrap: wrap !important; }
  #center { padding: 18px 20px !important; }
  #inspector { width: 100% !important; border-left: none; border-top: 1px solid var(--border); }
}

@media (max-width: 900px) {
  #sidebar {
    width: 58px !important;
    min-width: 58px !important;
    padding: 10px 4px !important;
  }
  .brand-text, .divider, .crumb-title, .sidebar-group-title, #nav label span, .sidebar-bottom {
    display: none !important;
  }
  .el-logo-brand { justify-content: center; padding: 6px 0 10px; }
  #nav label { justify-content: center !important; padding: 7px 0 !important; }
}


/* ==================== 20. ELEVENLABS EMOTION TOOLBAR & CHIPS ==================== */
.el-emo-toolbar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 10px;
  padding: 8px 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
}
.el-emo-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  color: #334155 !important;
}
.el-emo-chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 9999px;
  padding: 4px 11px;
  font-size: 12px;
  font-weight: 500;
  color: #0f172a !important;
  cursor: pointer;
  transition: all 0.15s ease;
  user-select: none;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.el-emo-chip:hover {
  background: #f1f5f9;
  border-color: #0f172a;
  transform: translateY(-1px);
}
.el-emo-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11.5px;
  font-weight: 600;
  color: #52525b;
}
.el-emo-chip-list {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
}
.el-emo-chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: #ffffff;
  border: 1px solid #e4e4e7;
  border-radius: 9999px;
  padding: 3px 9px;
  font-size: 11.5px;
  font-weight: 500;
  color: #18181b;
  cursor: pointer;
  transition: all 0.15s ease;
  user-select: none;
}
.el-emo-chip:hover {
  background: #f4f4f5;
  border-color: #18181b;
  transform: translateY(-1px);
}
.el-emo-chip .e-icon {
  font-size: 12px;
}
.el-emo-badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 1px 7px;
  background: #ede9fe;
  color: #6d28d9;
  border-radius: 9999px;
  font-size: 11px;
  font-weight: 600;
}

/* ==================== 21. STATUS PILL AUTO-DISMISS IN 10S ==================== */
.el-status-pill.auto-dismiss {
  position: relative;
  display: flex !important;
  align-items: center;
  justify-content: space-between;
  width: 100% !important;
  box-sizing: border-box;
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 12px !important;
  padding: 10px 14px 14px 14px !important;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04) !important;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
  overflow: hidden;
}
.el-status-pill.auto-dismiss.dismissed {
  opacity: 0 !important;
  transform: translateY(-8px) scale(0.98) !important;
  max-height: 0 !important;
  padding-top: 0 !important;
  padding-bottom: 0 !important;
  margin-top: 0 !important;
  margin-bottom: 0 !important;
  border-width: 0 !important;
  pointer-events: none !important;
}
.el-status-pill .el-status-body {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  min-width: 0;
  flex-wrap: wrap;
}
.el-status-pill .dot.live-pulse {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
  animation: el-pulse-ring 1.8s infinite cubic-bezier(0.66, 0, 0, 1);
}
@keyframes el-pulse-ring {
  0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
  70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
  100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}
.el-status-pill .el-status-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}
.el-countdown-badge {
  font-size: 11px;
  font-weight: 600;
  color: #71717a;
  background: #f4f4f5;
  padding: 2px 7px;
  border-radius: 6px;
  border: 1px solid #e4e4e7;
}
.el-status-close-btn {
  background: transparent;
  border: none;
  font-size: 13px;
  color: #a1a1aa;
  cursor: pointer;
  padding: 2px 6px;
  border-radius: 4px;
  transition: all 0.15s ease;
}
.el-status-close-btn:hover {
  background: #f4f4f5;
  color: #18181b;
}
.el-status-progress-track {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: #f1f5f9;
}
.el-status-progress-bar {
  height: 100%;
  width: 100%;
  background: linear-gradient(90deg, #10b981, #3b82f6);
  transition: width 0.1s linear;
}

/* ==================== 22. REAL-TIME GRADIO LOADING SHIMMER ==================== */
.progress-bar-wrap, .progress-bar, .progress-level-inner, div[data-testid="progress-bar"] {
  border-radius: 9999px !important;
  background: #f1f5f9 !important;
  overflow: hidden !important;
}
.progress-level-inner, div[data-testid="progress-bar"] > div {
  background: linear-gradient(90deg, #18181b 0%, #3b82f6 50%, #10b981 100%) !important;
  background-size: 200% 100% !important;
  animation: el-shimmer-progress 1.8s linear infinite !important;
  box-shadow: 0 0 12px rgba(59, 130, 246, 0.45) !important;
}
@keyframes el-shimmer-progress {
  0% { background-position: 100% 0; }
  100% { background-position: -100% 0; }
}

/* ==================== 23. SIGNATURE HOPE AVATAR ORB ==================== */
.s-avatar-orb {
  width: 30px;
  height: 30px;
  min-width: 30px;
  border-radius: 50%;
  background: conic-gradient(from 180deg at 50% 50%, #38bdf8 0deg, #818cf8 120deg, #ec4899 240deg, #38bdf8 360deg);
  box-shadow: 0 2px 8px rgba(56, 189, 248, 0.35);
  flex-shrink: 0;
  animation: el-orb-rotate 8s linear infinite;
}
@keyframes el-orb-rotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}


/* Fix voice dropdown styling */
#voice_dd_input,
#voice_dd_input .wrap,
#voice_dd_input .wrap-inner,
#voice_dd_input input,
#voice_dd_input .single-select,
.el-pill-dd,
.el-pill-dd .wrap,
.el-pill-dd .wrap-inner,
.el-pill-dd input,
.el-pill-dd .single-select {
  background: #ffffff !important;
  color: #18181b !important;
  border-color: #e4e4e7 !important;
  border-radius: 12px !important;
}
#voice_dd_input input::placeholder,
.el-pill-dd input::placeholder {
  color: #71717a !important;
}
#voice_dd_input .wrap-inner {
  padding: 6px 10px !important;
}
#voice_sample_audio_player {
  display: none !important;
}


/* Refined Studio Textarea */
#script {
  border: 1px solid #e2e8f0 !important;
  border-radius: 14px !important;
  background: #ffffff !important;
  padding: 8px !important;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
  transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
#script:focus-within {
  border-color: #18181b !important;
  box-shadow: 0 0 0 3px rgba(24, 24, 27, 0.06) !important;
}
#script textarea {
  font-size: 15px !important;
  line-height: 1.65 !important;
  color: #18181b !important;
  background: transparent !important;
  border: none !important;
  padding: 8px 10px !important;
}


/* High-Contrast Crisp Typography for Inspector Sliders & Labels */
.el-slider-head {
  margin-top: 16px !important;
  margin-bottom: 4px !important;
}
.title-row,
.el-slider-head .title-row {
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  color: #18181b !important;
  margin-bottom: 3px !important;
}
.title-row span,
.el-slider-head .title-row span {
  color: #18181b !important;
  font-size: 13px !important;
  font-weight: 600 !important;
}
.sub-row,
.el-slider-head .sub-row {
  display: flex !important;
  justify-content: space-between !important;
  font-size: 11px !important;
  color: #52525b !important;
}
.sub-row span,
.el-slider-head .sub-row span {
  color: #52525b !important;
  font-size: 11px !important;
  font-weight: 500 !important;
}
.el-slider-val {
  font-size: 11px !important;
  font-weight: 600 !important;
  color: #18181b !important;
  background: #f4f4f5 !important;
  padding: 2px 7px !important;
  border-radius: 6px !important;
  border: 1px solid #e4e4e7 !important;
}
.el-sec-title {
  font-size: 13px !important;
  font-weight: 600 !important;
  color: #18181b !important;
  margin: 14px 0 6px !important;
}
.el-row-label {
  font-size: 12.5px !important;
  font-weight: 500 !important;
  color: #18181b !important;
}
.el-sample-quote-card {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
  border-radius: 12px !important;
  padding: 10px 12px !important;
  margin: 8px 0 12px !important;
}
.el-sample-quote-card .s-desc,
.el-sample-quote-card .s-desc b {
  color: #0f172a !important;
  font-size: 12px !important;
  font-weight: 600 !important;
}
.el-sample-quote-card .s-quote {
  color: #475569 !important;
  font-size: 11.5px !important;
  font-style: italic !important;
  line-height: 1.4 !important;
  margin-top: 2px !important;
}

/* ===== POLISHED INSPECTOR MATCHING IMAGE 1 & 2 ===== */
.sub-r-wrap {
  display: flex !important;
  flex-direction: column !important;
  align-items: flex-end !important;
  text-align: right !important;
}
.sub-tick {
  font-size: 8px !important;
  color: #a1a1aa !important;
  line-height: 1 !important;
  margin-bottom: 1px !important;
  font-family: ui-monospace, monospace !important;
}
.el-clean-slider input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none !important;
  appearance: none !important;
  width: 3px !important;
  height: 14px !important;
  border-radius: 1px !important;
  background-color: #18181b !important;
  border: none !important;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.4) !important;
  margin-top: -5px !important;
  cursor: pointer !important;
}
.el-clean-slider input[type="range"]::-webkit-slider-runnable-track {
  height: 3px !important;
  border-radius: 2px !important;
  background: linear-gradient(to right, #52525b var(--range_progress, 50%), #e4e4e7 var(--range_progress, 50%)) !important;
  border: none !important;
}
.el-switch {
  border: 1px solid #e5e7eb !important;
  border-radius: 6px !important;
  padding: 3px 5px !important;
  background: #ffffff !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}
.el-switch input[type="checkbox"] {
  appearance: none !important;
  -webkit-appearance: none !important;
  width: 36px !important;
  height: 19px !important;
  background: #f4f4f5 !important;
  border: 1px solid #e4e4e7 !important;
  border-radius: 20px !important;
  position: relative !important;
  cursor: pointer !important;
  transition: background 0.2s ease, border-color 0.2s ease !important;
}
.el-switch input[type="checkbox"]::after {
  content: "" !important;
  position: absolute !important;
  top: 2px !important;
  left: 2px !important;
  width: 13px !important;
  height: 13px !important;
  border-radius: 50% !important;
  background: #d4d4d8 !important;
  transition: transform 0.2s ease, background-color 0.2s ease !important;
}
.el-switch input[type="checkbox"]:checked {
  background: #000000 !important;
  border-color: #000000 !important;
}
.el-switch input[type="checkbox"]:checked::after {
  background: #ffffff !important;
  transform: translateX(17px) !important;
  box-shadow: 0 1px 3px rgba(0,0,0,0.35) !important;
}
.el-format-pill {
  background: #f4f4f5 !important;
  border-radius: 9999px !important;
  padding: 5px 10px !important;
  font-size: 10px !important;
  font-weight: 500 !important;
  color: #27272a !important;
  white-space: nowrap !important;
  border: none !important;
  letter-spacing: -0.01em !important;
}

"""

JS_INJECT = """
() => {
  document.documentElement.classList.remove('dark');
  document.body.classList.remove('dark');
  const observer = new MutationObserver(() => {
    if (document.body.classList.contains('dark')) document.body.classList.remove('dark');
    if (document.documentElement.classList.contains('dark')) document.documentElement.classList.remove('dark');
  });
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
  observer.observe(document.body, { attributes: true, attributeFilter: ['class'] });

  if (localStorage.getItem('thanham_banner_closed') === 'true') {
    const b = document.getElementById('thanham-top-banner');
    if (b) b.style.display = 'none';
  }

  let currentVoiceAudio = null;
  let currentVoiceBtn = null;

  window.playVoicePreview = function(url, btn) {
    if (currentVoiceAudio && currentVoiceBtn === btn) {
      if (!currentVoiceAudio.paused) {
        currentVoiceAudio.pause();
        btn.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 3 20 12 6 21 6 3"/></svg>';
        btn.classList.remove('playing');
        return;
      } else {
        currentVoiceAudio.play();
        btn.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>';
        btn.classList.add('playing');
        return;
      }
    }

    if (currentVoiceAudio) {
      currentVoiceAudio.pause();
      if (currentVoiceBtn) {
        currentVoiceBtn.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 3 20 12 6 21 6 3"/></svg>';
        currentVoiceBtn.classList.remove('playing');
      }
    }

    const audio = new Audio(url);
    currentVoiceAudio = audio;
    currentVoiceBtn = btn;
    btn.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>';
    btn.classList.add('playing');

    audio.play().catch(e => console.error("Audio preview error:", e));

    audio.onended = function() {
      btn.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 3 20 12 6 21 6 3"/></svg>';
      btn.classList.remove('playing');
      currentVoiceAudio = null;
      currentVoiceBtn = null;
    };
  };

  window.selectVoiceLib = function(voiceName) {
    const dd = document.querySelector('#voice_dd_input input, #voice_dd_input .single-select');
    if (dd) {
      dd.value = voiceName;
      dd.dispatchEvent(new Event('input', { bubbles: true }));
    }
    const navInputs = document.querySelectorAll('#nav input[type="radio"]');
    if (navInputs && navInputs.length > 0) {
      navInputs[0].checked = true;
      navInputs[0].dispatchEvent(new Event('change', { bubbles: true }));
    }
  };

  // Đồng bộ giá trị hiển thị thời gian thực cho Slider Inspector
  function bindSlider(sliderId, badgeId, formatter) {
    const el = document.getElementById(sliderId);
    if (!el) return;
    const input = el.querySelector('input[type="range"]');
    const badge = document.getElementById(badgeId);
    if (!input || !badge) return;
    const update = () => {
      const val = parseFloat(input.value);
      badge.textContent = formatter(val);
      // Tự động cập nhật vạch màu đen bám theo vị trí con trượt
      const min = parseFloat(input.min) || 0;
      const max = parseFloat(input.max) || 1;
      const pct = Math.max(0, Math.min(100, ((val - min) / (max - min)) * 100));
      input.style.setProperty('--range_progress', pct + '%');
    };
    input.addEventListener('input', update);
    input.addEventListener('change', update);
    update();
  }

  function initSliders() {
    bindSlider('slider_speed', 'val-speed', v => (isNaN(v) ? '0.95x' : v.toFixed(2) + 'x'));
    bindSlider('slider_stability', 'val-stability', v => (isNaN(v) ? '45%' : Math.round(v * 100) + '%'));
    bindSlider('slider_similarity', 'val-similarity', v => (isNaN(v) ? '75%' : Math.round(v * 100) + '%'));
    bindSlider('slider_style', 'val-style', v => (isNaN(v) ? '5%' : Math.round(v * 100) + '%'));
  }

  setTimeout(initSliders, 300);
  setTimeout(initSliders, 1000);
  setTimeout(initSliders, 2500);

  // ==================== ELEVENLABS AUDIO EFFECTS CONTROLLER ====================
  window.setGradioFxInput = function(elemId, val) {
    const wrap = document.getElementById(elemId);
    if (!wrap) return;
    const inp = wrap.querySelector('textarea, input');
    if (inp) {
      const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set
        || Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value')?.set;
      if (setter) setter.call(inp, val);
      else inp.value = val;
      inp.dispatchEvent(new Event('input', { bubbles: true }));
      inp.dispatchEvent(new Event('change', { bubbles: true }));
    }
  };

  window.toggleFxSection = function(headerEl) {
    const sec = headerEl.closest('.el-fx-section');
    if (sec) sec.classList.toggle('collapsed');
  };

  window.toggleFxDropdown = function(kind, ev) {
    if (ev) ev.stopPropagation();
    const menuId = kind === 'distance' ? 'fx-menu-distance' : 'fx-menu-env';
    const cellId = kind === 'distance' ? 'fx-cell-distance' : 'fx-cell-env';
    const otherMenuId = kind === 'distance' ? 'fx-menu-env' : 'fx-menu-distance';
    const otherCellId = kind === 'distance' ? 'fx-cell-env' : 'fx-cell-distance';

    const otherMenu = document.getElementById(otherMenuId);
    const otherCell = document.getElementById(otherCellId);
    if (otherMenu) otherMenu.classList.remove('show');
    if (otherCell) otherCell.classList.remove('open');

    const menu = document.getElementById(menuId);
    const cell = document.getElementById(cellId);
    if (menu && cell) {
      const isOpen = menu.classList.contains('show');
      menu.classList.toggle('show', !isOpen);
      cell.classList.toggle('open', !isOpen);
    }
  };

  window.selectFxOption = function(kind, val, optEl, ev) {
    if (ev) ev.stopPropagation();
    const valSpan = document.getElementById(kind === 'distance' ? 'fx-val-distance' : 'fx-val-env');
    if (valSpan) valSpan.textContent = val;

    const menu = document.getElementById(kind === 'distance' ? 'fx-menu-distance' : 'fx-menu-env');
    const cell = document.getElementById(kind === 'distance' ? 'fx-cell-distance' : 'fx-cell-env');
    if (menu) {
      menu.querySelectorAll('.el-fx-opt').forEach(el => el.classList.remove('active'));
      if (optEl) optEl.classList.add('active');
      menu.classList.remove('show');
    }
    if (cell) cell.classList.remove('open');

    window.setGradioFxInput(kind === 'distance' ? 'fx_distance_input' : 'fx_env_input', val);
  };

  window.removeFxRow = function(kind, ev) {
    if (ev) ev.stopPropagation();
    const row = document.getElementById(kind === 'distance' ? 'fx-row-distance' : 'fx-row-env');
    if (row) row.style.display = 'none';

    if (kind === 'distance') {
      window.selectFxOption('distance', 'Medium', document.querySelector('#fx-menu-distance [data-val="Medium"]'));
    } else {
      window.selectFxOption('env', 'Studio (Dry)', document.querySelector('#fx-menu-env [data-val="Studio (Dry)"]'));
    }

    const addBtn = document.getElementById('fx-add-btn');
    if (addBtn) addBtn.style.display = 'flex';
  };

  window.restoreFxRows = function() {
    const r1 = document.getElementById('fx-row-distance');
    const r2 = document.getElementById('fx-row-env');
    if (r1 && r1.style.display === 'none') {
      r1.style.display = 'flex';
    } else if (r2 && r2.style.display === 'none') {
      r2.style.display = 'flex';
    }
    const stillHidden = (r1 && r1.style.display === 'none') || (r2 && r2.style.display === 'none');
    const addBtn = document.getElementById('fx-add-btn');
    if (addBtn) addBtn.style.display = stillHidden ? 'flex' : 'none';
  };

  
  // ==================== ELEVENLABS EMOTION TAGS & 10S AUTO-DISMISS ====================
  window.insertEmotionTag = function(tag) {
    const ta = document.querySelector('#script textarea');
    if (!ta) return;
    const start = ta.selectionStart;
    const end = ta.selectionEnd;
    const val = ta.value;
    const before = val.substring(0, start);
    const after = val.substring(end, val.length);
    const prefix = (start > 0 && val[start - 1] !== '\n' && val[start - 1] !== ' ') ? ' ' : '';
    const suffix = (after.length > 0 && after[0] !== ' ' && after[0] !== '\n') ? ' ' : ' ';
    const newText = before + prefix + tag + suffix + after;
    
    const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value')?.set;
    if (setter) setter.call(ta, newText);
    else ta.value = newText;
    
    const newPos = start + prefix.length + tag.length + suffix.length;
    ta.setSelectionRange(newPos, newPos);
    ta.focus();
    ta.dispatchEvent(new Event('input', { bubbles: true }));
    ta.dispatchEvent(new Event('change', { bubbles: true }));
  };

  window.activeDismissTimers = {};

  window.dismissStatus = function(id) {
    const el = document.getElementById(id);
    if (!el) return;
    el.classList.add('dismissed');
    setTimeout(() => {
      if (el && el.parentNode) el.remove();
    }, 450);
    if (window.activeDismissTimers[id]) {
      clearInterval(window.activeDismissTimers[id]);
      delete window.activeDismissTimers[id];
    }
  };

  window.pauseDismiss = function(id) {
    const el = document.getElementById(id);
    if (el) el.classList.add('paused');
  };

  window.resumeDismiss = function(id) {
    const el = document.getElementById(id);
    if (el) el.classList.remove('paused');
  };

  function initAutoDismissObservers() {
    const observer = new MutationObserver(() => {
      document.querySelectorAll('.el-status-pill.auto-dismiss:not([data-bound="true"])').forEach(pill => {
        pill.setAttribute('data-bound', 'true');
        const id = pill.id;
        let remaining = 100; // 10.0 seconds in tenths (0.1s)
        const cd = document.getElementById(id + '_cd');
        const bar = document.getElementById(id + '_bar');
        
        const interval = setInterval(() => {
          if (pill.classList.contains('paused')) return;
          remaining -= 1;
          if (cd) {
            const sec = Math.ceil(remaining / 10);
            cd.textContent = `${sec}s`;
          }
          if (bar) {
            bar.style.width = `${Math.max(0, (remaining / 100) * 100)}%`;
          }
          if (remaining <= 0) {
            clearInterval(interval);
            delete window.activeDismissTimers[id];
            window.dismissStatus(id);
          }
        }, 100);
        window.activeDismissTimers[id] = interval;
      });
    });
    observer.observe(document.body, { childList: true, subtree: true });
  }
  setTimeout(initAutoDismissObservers, 600);

  document.addEventListener('click', () => {
    ['fx-menu-distance', 'fx-menu-env'].forEach(id => {
      const m = document.getElementById(id);
      if (m) m.classList.remove('show');
    });
    ['fx-cell-distance', 'fx-cell-env'].forEach(id => {
      const c = document.getElementById(id);
      if (c) c.classList.remove('open');
    });
  });
}
"""

theme = gr.themes.Base(
    primary_hue="neutral",
    neutral_hue="neutral",
    font=[gr.themes.GoogleFont("Inter"), "Segoe UI", "sans-serif"],
)

with gr.Blocks(title="Thành Âm • Studio Giọng Nói AI") as demo:
    # 1. Top Banner
    gr.HTML("""
    <div id="thanham-top-banner" class="el-banner">
      <div class="el-banner-content">
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>
        <span>Studio sản xuất giọng đọc Vocal tiếng Anh & Tiếng Việt chuẩn phát thanh trên GTX 1650</span>
      </div>
      <button class="el-banner-close" onclick="
        document.getElementById('thanham-top-banner').style.display='none';
        localStorage.setItem('thanham_banner_closed', 'true');
      " aria-label="Ẩn thông báo">✕</button>
    </div>""")

    with gr.Row(elem_id="shell", equal_height=False):
        # ---------------- 2. Sidebar Tinh Gọn (Chỉ giữ công cụ thực) ----------------
        with gr.Column(scale=0, min_width=220, elem_id="sidebar"):
            gr.HTML("""
            <div class="el-logo-brand">
              <span class="brand-square">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m16 6 4 14"/><path d="M12 6v14"/><path d="M8 8v12"/><path d="M4 4v16"/></svg>
              </span>
              <span>Thành Âm</span>
            </div>
            <div class="sidebar-group-title">Không gian làm việc</div>
            """)

            # 4 công cụ chính HOÀN TOÀN CÓ TÍNH NĂNG
            nav = gr.Radio(
                choices=[
                    ("Đọc kịch bản", "tts"),
                    ("Tạo giọng mới", "vc"),
                    ("Đổi giọng", "changer"),
                    ("Kho giọng đọc", "lib"),
                ],
                value="tts", show_label=False, container=False, elem_id="nav",
            )

            gr.HTML(f"""
            <div class="sidebar-bottom">
              <div class="el-side-card">
                <b>NVIDIA GTX 1650 • 4 GB</b>
                <span class="live">● CUDA FP16 Trực tuyến</span>
              </div>
              <div class="el-side-card">
                <b>Mở trên điện thoại</b>
                Cùng mạng Wi-Fi:<br/><code>{LAN_URL}</code>
              </div>
            </div>""")

        # ---------------- Main Canvas ----------------
        with gr.Column(scale=1, elem_id="main"):
            bar = gr.HTML(topbar("tts"))
            with gr.Row(elem_id="workspace", equal_height=False):
                with gr.Column(scale=1, elem_id="center"):

                    # ==================== Workspace 1: Đọc kịch bản (Text to Speech) ====================
                    with gr.Column(visible=True) as page_tts:
                        gr.HTML("""
                        <div class="el-emo-toolbar">
                          <div class="el-emo-label">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8z"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><circle cx="9" cy="9" r="1.5"/><circle cx="15" cy="9" r="1.5"/></svg>
                            <span>Thẻ cảm xúc ElevenLabs:</span>
                          </div>
                          <div class="el-emo-chip-list">
                            <button type="button" class="el-emo-chip" onclick="insertEmotionTag('[kịch tính]')"><span class="e-icon">🎭</span> Kịch tính</button>
                            <button type="button" class="el-emo-chip" onclick="insertEmotionTag('[thì thầm]')"><span class="e-icon">🤫</span> Thì thầm</button>
                            <button type="button" class="el-emo-chip" onclick="insertEmotionTag('[hào hứng]')"><span class="e-icon">🔥</span> Hào hứng</button>
                            <button type="button" class="el-emo-chip" onclick="insertEmotionTag('[buồn]')"><span class="e-icon">🌧</span> Buồn bã</button>
                            <button type="button" class="el-emo-chip" onclick="insertEmotionTag('[tức giận]')"><span class="e-icon">⚡</span> Tức giận</button>
                            <button type="button" class="el-emo-chip" onclick="insertEmotionTag('[thở dài]')"><span class="e-icon">💨</span> Thở dài</button>
                            <button type="button" class="el-emo-chip" onclick="insertEmotionTag('[điềm tĩnh]')"><span class="e-icon">🌿</span> Điềm tĩnh</button>
                          </div>
                        </div>""")
                        script = gr.Textbox(
                            show_label=False, container=False, elem_id="script", lines=12, max_lines=30,
                            max_length=5000,
                            placeholder="Nhập hoặc dán kịch bản tiếng Anh hoặc tiếng Việt... Hệ thống tự động phân tách câu và ghép mượt mà trên GPU GTX 1650.",
                            value="The year was 1994. Deep inside the Black Forest, investigators discovered an abandoned radio tower broadcasting an unbroken 7-digit code. Every night at precisely 3:15 AM, the transmission repeated the exact same pattern.",
                        )
                        with gr.Row(elem_classes="el-bottom"):
                            count = gr.HTML(char_count(""))
                            clear_btn = gr.Button("Xóa", elem_classes="btn-ghost", scale=0, min_width=70)
                            sample_btn = gr.Button("Mẫu", elem_classes="btn-ghost", scale=0, min_width=70)
                            gen_btn = gr.Button("Tạo giọng nói", elem_classes="btn-black", scale=0, min_width=160)

                        # Hộp phát âm thanh thường trực & tự động phát
                        with gr.Column(visible=False, elem_classes="el-output-card") as output_dock:
                            tts_status = gr.HTML("""
                            <div class="el-status-pill">
                              <span class="dot"></span>
                              <span class="title">Sẵn sàng phát âm thanh</span>
                              <span class="sub">GTX 1650 FP16 • Bấm “Tạo giọng nói” để tạo & tự động phát trực tiếp</span>
                            </div>""")
                            tts_audio = gr.Audio(
                                label="Bản âm thanh phát trực tiếp & tải về (Tự động phát khi xong)",
                                type="filepath",
                                interactive=False,
                                autoplay=True,
                                elem_id="tts_player"
                            )

                    # ==================== Workspace 2: Tạo giọng mới (Clone & Design) ====================
                    with gr.Column(visible=False) as page_vc:
                        gr.HTML("""
                        <div class="el-h1">Tạo giọng đọc mới</div>
                        <div class="el-sub">Chọn phương thức: Sao chép nhanh từ mẫu ghi âm hoặc Thiết kế giọng mới theo thuộc tính âm sắc.</div>
                        """)

                        with gr.Tabs():
                            with gr.Tab("🎙 Sao chép giọng (Voice Clone)"):
                                gr.HTML('<div class="el-sub" style="margin-top:10px;">Tạo bản sao giọng nói chân thực từ một đoạn âm thanh ngắn (5–15 giây) kèm văn bản chính xác câu thoại.</div>')
                                ic_name = gr.Textbox(label="Tên giọng đọc mới", placeholder="Ví dụ: Giọng MC Minh Quân, English Narrator...")
                                ic_audio = gr.Audio(label="Đoạn âm thanh mẫu (5–15s)", type="filepath", sources=["upload", "microphone"])
                                ic_text = gr.Textbox(label="Văn bản chính xác được nói trong đoạn mẫu", placeholder="Nhập đúng câu nói trong audio để mô hình so khớp...", lines=2)
                                ic_btn = gr.Button("Tạo bản sao giọng nói", elem_classes="btn-black")
                                ic_status = gr.HTML("")

                            with gr.Tab("🎨 Thiết kế giọng đọc (Voice Design)"):
                                gr.HTML('<div class="el-sub" style="margin-top:10px;">Tự phối âm sắc giọng nói bằng việc kết hợp giới tính, độ tuổi, âm vực và ngữ điệu (Accent).</div>')
                                with gr.Row():
                                    vd_gender = gr.Dropdown(["male", "female"], value="male", label="Giới tính")
                                    vd_age = gr.Dropdown(["young adult", "middle-aged", "teenager", "elderly"], value="young adult", label="Độ tuổi")
                                    vd_pitch = gr.Dropdown(["very low pitch", "low pitch", "moderate pitch", "high pitch"], value="low pitch", label="Âm vực (Pitch)")
                                    vd_accent = gr.Dropdown(["american accent", "british accent", "australian accent", "canadian accent"], value="american accent", label="Ngữ điệu (Accent)")

                                vd_text = gr.Textbox(label="Câu đọc thử nghiệm", value="Welcome to this video essay, where we explore the hidden dynamics of human decision making.", lines=2)
                                with gr.Row():
                                    vd_btn = gr.Button("Nghe thử giọng thiết kế", elem_classes="btn-black", scale=1)
                                vd_status = gr.HTML("")
                                vd_audio = gr.Audio(label="Bản nghe thử (Tự động phát)", type="filepath", interactive=False, autoplay=True)

                                with gr.Row():
                                    vd_save_name = gr.Textbox(label="Đặt tên cho giọng này để lưu vào Kho", placeholder="Ví dụ: David Video Essayist...")
                                    vd_save_btn = gr.Button("Lưu vào Kho giọng đọc", elem_classes="btn-ghost", scale=0, min_width=180)
                                vd_save_status = gr.HTML("")

                    # ==================== Workspace 3: Đổi giọng (Voice Changer) ====================
                    with gr.Column(visible=False) as page_changer:
                        gr.HTML("""
                        <div class="el-h1">Đổi giọng (Voice Changer)</div>
                        <div class="el-sub">Tải lên tệp âm thanh hoặc video để chuyển đổi sang giọng đọc đích mong muốn.</div>
                        """)

                        changer_audio_in = gr.Audio(label="Tệp âm thanh / video đầu vào", type="filepath", sources=["upload", "microphone"])
                        changer_hint = gr.Textbox(label="Gợi ý văn bản (tùy chọn)", placeholder="Nhập câu thoại hoặc để trống để giữ nội dung gốc...", lines=2)
                        with gr.Row():
                            changer_btn = gr.Button("Tiến hành đổi giọng", elem_classes="btn-black", scale=0, min_width=180)

                        with gr.Column(visible=True, elem_classes="el-output-card") as changer_output_dock:
                            changer_status = gr.HTML("")
                            changer_audio_out = gr.Audio(label="Âm thanh sau khi đổi giọng (Tự động phát)", type="filepath", interactive=False, autoplay=True)

                    # ==================== Workspace 4: Kho giọng đọc (Voices Library) ====================
                    with gr.Column(visible=False) as page_lib:
                        gr.HTML("""
                        <div class="el-h1">Kho giọng đọc (Voices Library)</div>
                        <div class="el-sub">Dễ dàng nghe thử và chọn giọng vocal tiếng Anh hoặc tiếng Việt cho kịch bản của bạn.</div>
                        """)

                        # Bảng nghe thử trực tiếp giọng mẫu
                        with gr.Column(elem_classes="el-lib-preview-dock"):
                            with gr.Row():
                                lib_dd = gr.Dropdown(
                                    choices=voice_choices(),
                                    value=voice_choices()[0],
                                    label="Chọn giọng muốn nghe thử (21 giọng English & 3 giọng Việt)",
                                    scale=1,
                                    elem_classes="el-pill-dd",
                                )
                                lib_use = gr.Button("Sử dụng giọng này cho Đọc kịch bản", elem_classes="btn-black", scale=0, min_width=240)
                            lib_info = gr.HTML(render_voice_preview_quote(voice_choices()[0]))
                            lib_audio = gr.Audio(
                                value=all_voices()[voice_choices()[0]]["audio"],
                                label="▶ Bản thu âm mẫu gốc (Bấm Play để nghe trực tiếp)",
                                type="filepath",
                                interactive=False,
                                autoplay=False,
                            )
                            with gr.Row():
                                lib_del = gr.Button("Xóa giọng này (chỉ áp dụng cho giọng tự tạo)", elem_classes="btn-ghost", size="sm", scale=0, min_width=150)

                        gr.HTML('<div class="el-sec-title" style="margin-top:20px;">Duyệt danh mục theo nhóm</div>')
                        with gr.Row(elem_classes="vlib-top-bar"):
                            lib_search = gr.Textbox(
                                show_label=False, container=False, placeholder="Tìm kiếm theo tên nhân vật hoặc phong cách...",
                                scale=1, elem_classes="el-pill-dd",
                            )
                            lib_filter = gr.Radio(
                                choices=["Tất cả", "US English (Mỹ)", "UK English (Anh)", "Nam (Male)", "Nữ (Female)", "Tiếng Việt", "Giọng tự tạo"],
                                value="Tất cả", show_label=False, container=False,
                            )

                        # Danh sách card giọng đọc trực quan
                        lib_cards_container = gr.HTML(render_voice_library_html("Tất cả"))

                # ==================== Cột Cài đặt bên phải (Inspector) ====================
                with gr.Column(scale=0, min_width=330, elem_id="inspector", visible=True) as inspector:
                    with gr.Tabs():
                        with gr.Tab("Cài đặt"):
                            gr.HTML('<div class="el-sec-title">Giọng đọc</div>')
                            with gr.Row(elem_classes="el-voice-pill-row"):
                                voice_dd = gr.Dropdown(
                                    choices=voice_choices(),
                                    value=voice_choices()[0],
                                    show_label=False,
                                    container=False,
                                    elem_classes="el-pill-dd",
                                    elem_id="voice_dd_input",
                                )
                            voice_sample_quote = gr.HTML(render_voice_preview_quote(voice_choices()[0]))
                            voice_sample_player = gr.Audio(
                                value=all_voices()[voice_choices()[0]]["audio"],
                                label="▶ Nghe thử mẫu giọng đang chọn",
                                interactive=False,
                                autoplay=False,
                                elem_id="voice_sample_audio_player",
                                visible=False,
                            )

                            # Tốc độ
                            gr.HTML("""
                            <div class="el-slider-head">
                              <div class="title-row"><span>Tốc độ đọc</span></div>
                              <div class="sub-row"><span>Chậm hơn</span><span class="sub-r-wrap"><span class="sub-tick">v</span><span>Nhanh hơn</span></span></div>
                            </div>""")
                            speed = gr.Slider(0.7, 1.4, value=0.95, step=0.05, show_label=False, container=False, elem_id="slider_speed", elem_classes="el-clean-slider")

                            # Độ ổn định
                            gr.HTML("""
                            <div class="el-slider-head">
                              <div class="title-row"><span>Độ ổn định</span></div>
                              <div class="sub-row"><span>Linh hoạt, cảm xúc</span><span class="sub-r-wrap"><span class="sub-tick">v</span><span>Ổn định, đều đặn</span></span></div>
                            </div>""")
                            stability = gr.Slider(0.0, 1.0, value=0.45, step=0.05, show_label=False, container=False, elem_id="slider_stability", elem_classes="el-clean-slider")

                            # Độ tương đồng
                            gr.HTML("""
                            <div class="el-slider-head">
                              <div class="title-row"><span>Độ bám giọng mẫu</span></div>
                              <div class="sub-row"><span>Linh hoạt</span><span class="sub-r-wrap"><span class="sub-tick">v</span><span>Rất giống mẫu</span></span></div>
                            </div>""")
                            similarity = gr.Slider(0.0, 1.0, value=0.75, step=0.05, show_label=False, container=False, elem_id="slider_similarity", elem_classes="el-clean-slider")

                            # Cường điệu phong cách
                            gr.HTML("""
                            <div class="el-slider-head">
                              <div class="title-row"><span>Nhấn nhá cảm xúc</span></div>
                              <div class="sub-row"><span>Tự nhiên</span><span class="sub-r-wrap"><span class="sub-tick">v</span><span>Kịch tính</span></span></div>
                            </div>""")
                            style_exag = gr.Slider(0.0, 1.0, value=0.05, step=0.05, show_label=False, container=False, elem_id="slider_style", elem_classes="el-clean-slider")

                            # ==================== ElevenLabs Audio effects ====================
                            gr.HTML("""
                            <div class="el-fx-section">
                              <div class="el-fx-header" onclick="toggleFxSection(this)">
                                <span class="el-fx-title">Audio effects</span>
                                <svg class="el-fx-chevron" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
                              </div>
                              <div class="el-fx-body">
                                <!-- Row 1: Distance (Near / Medium / Far) -->
                                <div class="el-fx-row" id="fx-row-distance">
                                  <div class="el-fx-label-cell">
                                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
                                      <circle cx="12" cy="11" r="2.5"/>
                                      <path d="M12 13.5v4.5"/>
                                      <path d="M9.5 18h5"/>
                                      <path d="M6.5 7.5a7.5 7.5 0 0 0 0 7" stroke-dasharray="2 2"/>
                                      <path d="M17.5 7.5a7.5 7.5 0 0 1 0 7" stroke-dasharray="2 2"/>
                                    </svg>
                                    <span>Distance</span>
                                  </div>
                                  <div class="el-fx-select-cell" id="fx-cell-distance" onclick="toggleFxDropdown('distance', event)">
                                    <span id="fx-val-distance">Medium</span>
                                    <svg class="fx-dd-arrow" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
                                  </div>
                                  <div class="el-fx-remove-cell" onclick="removeFxRow('distance', event)" title="Gỡ hiệu ứng Distance">
                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
                                  </div>
                                  <!-- Popover menu -->
                                  <div class="el-fx-popover" id="fx-menu-distance">
                                    <div class="el-fx-opt" data-val="Near" onclick="selectFxOption('distance', 'Near', this, event)">
                                      <span>Near</span>
                                      <svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                                    </div>
                                    <div class="el-fx-opt active" data-val="Medium" onclick="selectFxOption('distance', 'Medium', this, event)">
                                      <span>Medium</span>
                                      <svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                                    </div>
                                    <div class="el-fx-opt" data-val="Far" onclick="selectFxOption('distance', 'Far', this, event)">
                                      <span>Far</span>
                                      <svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                                    </div>
                                  </div>
                                </div>

                                <!-- Row 2: Space & Filter -->
                                <div class="el-fx-row" id="fx-row-env">
                                  <div class="el-fx-label-cell">
                                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
                                      <path d="M2 10v3"/>
                                      <path d="M6 6v11"/>
                                      <path d="M10 3v18"/>
                                      <path d="M14 8v7"/>
                                      <path d="M18 5v13"/>
                                      <path d="M22 10v3"/>
                                    </svg>
                                    <span>Space</span>
                                  </div>
                                  <div class="el-fx-select-cell" id="fx-cell-env" onclick="toggleFxDropdown('env', event)">
                                    <span id="fx-val-env">Studio (Dry)</span>
                                    <svg class="fx-dd-arrow" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
                                  </div>
                                  <div class="el-fx-remove-cell" onclick="removeFxRow('env', event)" title="Gỡ hiệu ứng Space">
                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
                                  </div>
                                  <!-- Popover menu -->
                                  <div class="el-fx-popover" id="fx-menu-env">
                                    <div class="el-fx-opt active" data-val="Studio (Dry)" onclick="selectFxOption('env', 'Studio (Dry)', this, event)">
                                      <span>Studio (Dry)</span>
                                      <svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                                    </div>
                                    <div class="el-fx-opt" data-val="Small Room" onclick="selectFxOption('env', 'Small Room', this, event)">
                                      <span>Small Room</span>
                                      <svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                                    </div>
                                    <div class="el-fx-opt" data-val="Large Hall" onclick="selectFxOption('env', 'Large Hall', this, event)">
                                      <span>Large Hall</span>
                                      <svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                                    </div>
                                    <div class="el-fx-opt" data-val="Phone Line" onclick="selectFxOption('env', 'Phone Line', this, event)">
                                      <span>Phone Line</span>
                                      <svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                                    </div>
                                    <div class="el-fx-opt" data-val="Vintage Radio" onclick="selectFxOption('env', 'Vintage Radio', this, event)">
                                      <span>Vintage Radio</span>
                                      <svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                                    </div>
                                    <div class="el-fx-opt" data-val="Megaphone" onclick="selectFxOption('env', 'Megaphone', this, event)">
                                      <span>Megaphone</span>
                                      <svg class="fx-check" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                                    </div>
                                  </div>
                                </div>

                                <div class="el-fx-add-btn" id="fx-add-btn" onclick="restoreFxRows()">
                                  <span>+ Add effect</span>
                                </div>
                              </div>
                            </div>""")
                            fx_distance = gr.Textbox(value="Medium", show_label=False, container=False, elem_id="fx_distance_input")
                            fx_env = gr.Textbox(value="Studio (Dry)", show_label=False, container=False, elem_id="fx_env_input")

                            # Ngôn ngữ
                            with gr.Row(elem_classes="el-row-item"):
                                gr.HTML('<div class="el-row-label">Ngôn ngữ</div>')
                                lang = gr.Dropdown(
                                    list(LANG_MAP.keys()),
                                    value="English",
                                    show_label=False,
                                    container=False,
                                    scale=0,
                                    min_width=130,
                                    elem_classes="el-pill-dd",
                                )

                            # Master âm thanh phòng thu (-14 LUFS)
                            with gr.Row(elem_classes="el-row-item"):
                                gr.HTML('<div class="el-row-label">Master chuẩn phòng thu (-14 LUFS)</div>')
                                speaker_boost = gr.Checkbox(value=True, show_label=False, container=False, scale=0, min_width=44, elem_classes="el-switch")

                            # Loại bỏ tiếng ồn nền
                            with gr.Row(elem_classes="el-row-item"):
                                gr.HTML('<div class="el-row-label">Loại bỏ tiếng ồn nền</div>')
                                denoise = gr.Checkbox(value=False, show_label=False, container=False, scale=0, min_width=44, elem_classes="el-switch")

                            # Định dạng đầu ra
                            with gr.Row(elem_classes="el-row-item"):
                                gr.HTML('<div class="el-row-label">Định dạng đầu ra</div>')
                                gr.HTML('<div class="el-format-pill">WAV · 24 kHz · TruePeak -1.0dB</div>')

                            # Nút đặt lại giá trị
                            with gr.Row(elem_classes="el-reset-row"):
                                reset = gr.Button("↺  Đặt lại giá trị", size="sm", elem_classes="btn-reset", scale=0, min_width=110)

                            # Accordion chọn mô hình (Đặt gọn gàng bên dưới các slider chính)
                            with gr.Accordion("⚙️ Cấu hình mô hình tạo sinh (AI Model)", open=False):
                                model_choice_dd = gr.Radio(
                                    choices=[
                                        ("Eleven v4 (Turbo)", "Eleven v4 (Turbo)"),
                                        ("Eleven v3 (Biểu cảm)", "Eleven v3 (Biểu cảm)"),
                                        ("Eleven Multilingual v2 (Chuẩn)", "Eleven Multilingual v2 (Chuẩn)"),
                                    ],
                                    value="Eleven v4 (Turbo)",
                                    show_label=False,
                                    container=False,
                                    elem_id="model_cards_radio",
                                )
                                model_info_card = gr.HTML(render_model_info("Eleven v4 (Turbo)"))
                        with gr.Tab("Lịch sử"):
                            history = gr.Files(label="Bản âm thanh đã tạo gần đây", value=history_files(), interactive=False)

    # ---------------- Bộ điều hướng sự kiện ----------------
    def on_nav(page):
        return (
            gr.update(visible=page == "tts"),
            gr.update(visible=page == "vc"),
            gr.update(visible=page == "changer"),
            gr.update(visible=page == "lib"),
            gr.update(visible=page in ["tts", "changer"]),
            topbar(page),
        )

    nav.change(on_nav, nav, [page_tts, page_vc, page_changer, page_lib, inspector, bar])

    clear_btn.click(lambda: "", None, script)
    sample_text_tpl = (
        "[kịch tính] Năm 1994, sâu trong Rừng Đen, các điều tra viên phát hiện một tháp phát thanh bỏ hoang đang liên tục phát đi một mã số gồm bảy chữ số.\n"
        "[thì thầm] Mỗi đêm, đúng 3 giờ 15 phút, tín hiệu lại lặp lại cùng một chuỗi âm thanh.\n"
        "[hào hứng] Hãy tưởng tượng, giọng đọc này được tạo hoàn toàn bằng công nghệ số trên GPU GTX 1650.\n"
        "[điềm tĩnh] Cảm ơn bạn đã lắng nghe."
    )
    sample_btn.click(lambda: sample_text_tpl, None, script)
    script.change(char_count, script, count)

    # Sinh âm thanh Đọc kịch bản
    gen_btn.click(
        tts,
        [voice_dd, script, lang, speed, stability, similarity, style_exag, model_choice_dd, denoise, speaker_boost, fx_distance, fx_env],
        [tts_audio, tts_status, output_dock, history],
    )

    # Đổi giọng
    changer_btn.click(
        voice_change_run,
        [voice_dd, changer_audio_in, changer_hint, lang, speed, stability, similarity, model_choice_dd, fx_distance, fx_env],
        [changer_audio_out, changer_status, changer_output_dock, history],
    )

    # Cập nhật mô tả mô hình động
    model_choice_dd.change(render_model_info, model_choice_dd, model_info_card)

    reset.click(
        lambda: (0.95, 0.45, 0.75, 0.05, "Eleven v4 (Turbo)", False, True, "English", render_model_info("Eleven v4 (Turbo)"), "Medium", "Studio (Dry)"),
        None,
        [speed, stability, similarity, style_exag, model_choice_dd, denoise, speaker_boost, lang, model_info_card, fx_distance, fx_env],
    )

    def on_clone_success(name, audio, transcript):
        v1, v2, msg, _, p_tab = clone_create(name, audio, transcript)
        cards_html = render_voice_library_html()
        return v1, v2, msg, p_tab, cards_html

    ic_btn.click(on_clone_success, [ic_name, ic_audio, ic_text], [voice_dd, lib_dd, ic_status, nav, lib_cards_container])

    vd_path, vd_script = gr.State(""), gr.State("")
    vd_btn.click(design_generate, [vd_gender, vd_age, vd_pitch, vd_accent, vd_text, lang, model_choice_dd],
                 [vd_audio, vd_status, vd_path, vd_script, history])

    def on_design_save_success(name, path, script_text):
        v1, v2, msg, _ = design_save(name, path, script_text)
        cards_html = render_voice_library_html()
        return v1, v2, msg, cards_html

    vd_save_btn.click(on_design_save_success, [vd_save_name, vd_path, vd_script],
                      [voice_dd, lib_dd, vd_save_status, lib_cards_container])

    # Kho giọng đọc & Đồng bộ nghe thử mẫu giọng
    def on_voice_select(v):
        v_data = all_voices().get(v, {})
        return v_data.get("audio"), render_voice_preview_quote(v)

    voice_dd.change(on_voice_select, voice_dd, [voice_sample_player, voice_sample_quote])
    lib_dd.change(on_voice_select, lib_dd, [lib_audio, lib_info])

    def on_lib_filter(flt, sq):
        return render_voice_library_html(flt, sq)

    lib_filter.change(on_lib_filter, [lib_filter, lib_search], lib_cards_container)
    lib_search.change(on_lib_filter, [lib_filter, lib_search], lib_cards_container)

    def on_use_voice(v):
        v_data = all_voices().get(v, {})
        return v, "tts", v_data.get("audio"), render_voice_preview_quote(v)

    lib_use.click(on_use_voice, lib_dd, [voice_dd, nav, voice_sample_player, voice_sample_quote])

    def on_delete_voice(v):
        v1, v2 = lib_delete(v)
        cards_html = render_voice_library_html()
        first = voice_choices()[0]
        audio, info = on_voice_select(first)
        return v1, v2, cards_html, audio, info, audio, info

    lib_del.click(on_delete_voice, lib_dd, [voice_dd, lib_dd, lib_cards_container, lib_audio, lib_info, voice_sample_player, voice_sample_quote])


if __name__ == "__main__":
    print(f"🚀 Thành Âm Studio đang khởi chạy trên: http://127.0.0.1:7860 & {LAN_URL}")
    demo.queue().launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True,
        theme=theme,
        css=CSS,
        js=JS_INJECT,
        allowed_paths=[BASE, OUT_DIR, PRESET_DIR, VOICES_DIR],
    )
