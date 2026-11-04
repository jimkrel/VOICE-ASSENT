import re

APP_PATH = r"E:\VoiceAI\studio_app.py"

with open(APP_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# 1. ADD EMOTION DEFINITIONS AFTER apply_taper
EMOTION_BLOCK = '''
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

TAG_REGEX = re.compile(r'\\[(.*?)\\]', re.IGNORECASE)

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
    lines = raw_text.split('\\n')
    current_emotion = "calm"
    segments = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        tokens = re.split(r'(\\[.*?\\])', line)
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
        raw_text_clean = re.sub(r'\\[.*?\\]', '', raw_text).strip()
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
'''

# Find insertion point before def biquad_peaking
target_biquad = "def biquad_peaking(data, sr, f0, gain_db, Q=1.0):"
if target_biquad in text:
    text = text.replace(target_biquad, EMOTION_BLOCK + "\n\n" + target_biquad)
    print("Added EMOTION_BLOCK")
else:
    print("Could not find biquad_peaking target")

# 2. UPDATE render_voice_preview_quote with avatar orb matching Image 1
old_quote = '''def render_voice_preview_quote(v_name):
    v = all_voices().get(v_name, {})
    text = v.get("text", "")
    desc = v.get("desc", "")
    audio_path = v.get("audio", "").replace("\\\\", "/")
    audio_url = f"/gradio_api/file={audio_path}"
    sname = v_name.split("—")[0].strip()
    return f"""
    <div class="el-sample-quote-card">
      <div class="s-head-row">
        <button class="voice-circle-play-btn" onclick="playVoicePreview('{audio_url}', this)" title="Bấm nghe thử giọng {sname}">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 3 20 12 6 21 6 3"/></svg>
        </button>
        <div class="s-meta-col">
          <div class="s-desc"><b>{sname}</b> • {desc}</div>
          <div class="s-quote">“{text}”</div>
        </div>
      </div>
    </div>"""'''

new_quote = '''def render_voice_preview_quote(v_name):
    v = all_voices().get(v_name, {})
    text = v.get("text", "")
    desc = v.get("desc", "")
    audio_path = v.get("audio", "").replace("\\\\", "/")
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
    </div>"""'''

if "def render_voice_preview_quote" in text:
    text = re.sub(
        r'def render_voice_preview_quote\(v_name\):[\s\S]*?</div>"""',
        new_quote,
        text,
        count=1
    )
    print("Updated render_voice_preview_quote")

# 3. UPDATE _run_single to accept emotion and apply EMOTION_PROFILES & DSP
old_run_single_pattern = r'def _run_single\(text, lang, speed, stability, similarity, style_exag, model_choice, denoise, \*\*voice\):[\s\S]*?return audio, steps'

new_run_single = '''def _run_single(text, lang, speed, stability, similarity, style_exag, model_choice, denoise, emotion="calm", **voice):
    m = MODEL_STEPS.get(model_choice, list(MODEL_STEPS.values())[0])
    steps = m.get("steps", 14)
    base_cfg = m.get("cfg", 1.95)
    base_pos = m.get("pos", 0.85)

    emo = (emotion or "calm").lower()
    emo_prof = EMOTION_PROFILES.get(emo, EMOTION_PROFILES["calm"])

    # Hiệu chỉnh CFG & Position Temperature kết hợp Slider + Thẻ cảm xúc ElevenLabs
    cfg = (base_cfg * (0.82 + 0.25 * float(similarity)) + float(style_exag) * 0.35) * emo_prof["cfg_mult"]
    cfg = float(np.clip(cfg, 1.55, 2.35))

    pos_temp = (base_pos * (1.25 - 0.55 * float(stability)) + float(style_exag) * 0.45) * emo_prof["pos_mult"]
    pos_temp = float(np.clip(pos_temp, 0.50, 1.45))

    eff_speed = float(speed) * emo_prof["speed_mult"]
    eff_speed = float(np.clip(eff_speed, 0.65, 1.50))

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
    kw.update({k: v for k, v in voice.items() if v})
    with torch.inference_mode():
        audio = model.generate(**kw)[0]
    if isinstance(audio, torch.Tensor):
        audio = audio.detach().cpu().numpy()
    audio = np.asarray(audio, dtype=np.float32).squeeze()

    # Áp dụng Emotion DSP (định hình âm vực, lụa/thì thầm/kịch tính)
    audio = apply_emotion_dsp(audio, sr=model.sampling_rate, emotion=emo)
    return audio, steps'''

text = re.sub(old_run_single_pattern, new_run_single, text, count=1)
print("Updated _run_single")

# 4. UPDATE status_html with 10s auto-dismiss and countdown
old_status_pattern = r'def status_html\(elapsed, dur, steps, chunks=1, label="[^"]*", fx_info=""\):[\s\S]*?</div>"""'

new_status_html = '''def status_html(elapsed, dur, steps, chunks=1, label="Đã tạo giọng nói thành công", fx_info="", emotions_used=None):
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
    </div>"""'''

text = re.sub(old_status_pattern, new_status_html, text, count=1)
print("Updated status_html")

# 5. UPDATE tts() to use parse_and_chunk_script and real-time progress
old_tts_pattern = r'def tts\(voice, text, lang, speed, stability, similarity, style_exag, model_choice, denoise, speaker_boost, fx_distance="Medium", fx_env="Studio \(Dry\)", progress=gr\.Progress\(\)\):[\s\S]*?return path, status_html\(elapsed, dur, total_steps, total_chunks, fx_info=fx_info\), gr\.update\(visible=True\), history_files\(\)'

new_tts = '''def tts(voice, text, lang, speed, stability, similarity, style_exag, model_choice, denoise, speaker_boost, fx_distance="Medium", fx_env="Studio (Dry)", progress=gr.Progress()):
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
    return path, status_html(elapsed, dur, total_steps, total_chunks, fx_info=fx_info, emotions_used=emotions_used), gr.update(visible=True), history_files()'''

text = re.sub(old_tts_pattern, new_tts, text, count=1)
print("Updated tts()")

# 6. INSERT EMOTION TOOLBAR IN UI ABOVE script = gr.Textbox
target_script = "script = gr.Textbox(\n                            show_label=False, container=False, elem_id=\"script\""
replacement_script = """gr.HTML(\"\"\"
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
                        </div>\"\"\")
                        script = gr.Textbox(
                            show_label=False, container=False, elem_id="script\""""

if target_script in text:
    text = text.replace(target_script, replacement_script)
    print("Added Emotion Toolbar above script")
else:
    print("Could not find target_script")

# 7. ADD JS LOGIC TO JS_INJECT
js_additions = """
  // ==================== ELEVENLABS EMOTION TAGS & 10S AUTO-DISMISS ====================
  window.insertEmotionTag = function(tag) {
    const ta = document.querySelector('#script textarea');
    if (!ta) return;
    const start = ta.selectionStart;
    const end = ta.selectionEnd;
    const val = ta.value;
    const before = val.substring(0, start);
    const after = val.substring(end, val.length);
    const prefix = (start > 0 && val[start - 1] !== '\\n' && val[start - 1] !== ' ') ? ' ' : '';
    const suffix = (after.length > 0 && after[0] !== ' ' && after[0] !== '\\n') ? ' ' : ' ';
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
"""

# Inject into JS_INJECT before document.addEventListener('click'
target_js = "document.addEventListener('click', () => {"
if target_js in text:
    text = text.replace(target_js, js_additions + "\n  " + target_js)
    print("Added JS Logic")
else:
    print("Could not find target_js")

# 8. ADD CSS STYLES FOR EMOTIONS, AUTO-DISMISS, LOADING SHIMMER & HOPE AVATAR
css_additions = """
/* ==================== 20. ELEVENLABS EMOTION TOOLBAR & CHIPS ==================== */
.el-emo-toolbar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 8px;
  padding: 6px 12px;
  background: #fafafa;
  border: 1px solid #e4e4e7;
  border-radius: 10px;
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
"""

# Append CSS before JS_INJECT
target_css_end = 'JS_INJECT = """'
if target_css_end in text:
    text = text.replace(target_css_end, css_additions + '\n\n' + target_css_end)
    print("Added CSS Additions")
else:
    print("Could not find target_css_end")

with open(APP_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print(f"Successfully wrote updated studio_app.py ({len(text)} characters)")
