import os, torch, soundfile as sf
import numpy as np

# Protect SSD Drive C: -> force all caches and temps to Drive E:
os.environ['HF_HOME'] = r'E:\VoiceAI\hf_cache'
os.environ['TORCH_HOME'] = r'E:\VoiceAI\torch_cache'
os.environ['TEMP'] = r'E:\VoiceAI\temp'
os.environ['TMP'] = r'E:\VoiceAI\temp'

from omnivoice.models.omnivoice import OmniVoice

PRESET_DIR = r"E:\VoiceAI\presets"
os.makedirs(PRESET_DIR, exist_ok=True)

# OmniVoice valid tags:
# Gender: male, female
# Age: child, teenager, young adult, middle-aged, elderly
# Pitch: very low pitch, low pitch, moderate pitch, high pitch, very high pitch
# Accent: american accent, british accent, australian accent, canadian accent
targets = {
    "marcus_documentary.wav": (
        "male, middle-aged, very low pitch, american accent",
        "The year was 1994. Deep inside the mountain, investigators discovered something that defies all rational explanation."
    ),
    "liam_storyteller.wav": (
        "male, young adult, moderate pitch, american accent",
        "Have you ever wondered why some stories stay with you forever, while others fade away in minutes?"
    ),
    "alex_recap.wav": (
        "male, young adult, low pitch, american accent",
        "He thought he could escape the police, but within forty seconds, his entire plan completely unraveled."
    ),
    "emma_explainer.wav": (
        "female, young adult, moderate pitch, british accent",
        "Science is not just about memorizing facts; it is about looking at the world with curiosity and wonder."
    )
}

print("🔄 Đang nạp mô hình OmniVoice để tạo kho giọng anchor YouTube...")
model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cuda:0", dtype=torch.float16)
print("✅ OmniVoice đã nạp xong!")

for fname, (instruct_p, text_p) in targets.items():
    fpath = os.path.join(PRESET_DIR, fname)
    if os.path.exists(fpath) and os.path.getsize(fpath) > 10000:
        print(f"⏩ Đã có sẵn: {fname}")
        continue
    print(f"🎙 Đang sinh mẫu {fname} với cấu hình [{instruct_p}]...")
    with torch.inference_mode():
        audio = model.generate(
            text=text_p,
            language="English",
            num_step=14,
            instruct=instruct_p,
            postprocess_output=True,
        )[0]
    if isinstance(audio, torch.Tensor):
        audio = audio.detach().cpu().numpy()
    audio = np.asarray(audio, dtype=np.float32).squeeze()
    peak = np.max(np.abs(audio))
    if peak > 1e-4:
        audio = audio / peak * 0.92
    sf.write(fpath, audio, model.sampling_rate)
    print(f"💾 Đã lưu thành công {fname} ({len(audio)/model.sampling_rate:.1f}s)")

print("🎉 Hoàn tất nạp kho mẫu giọng YouTube tiếng Anh!")
