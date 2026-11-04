import re

with open(r"E:\VoiceAI\studio_app.py", "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()
print(f"Total lines: {len(lines)}")

patterns = ["def tts", "def apply_audio_effects", "EMOTION", "Audio effects", "status_html", "Hope - upbeat", "JS_INJECT", "CUSTOM_CSS"]
for p in patterns:
    matches = [i+1 for i, l in enumerate(lines) if p.lower() in l.lower()]
    print(f"Pattern '{p}': found at lines {matches[:10]}")
