with open(r"E:\VoiceAI\studio_app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "def biquad" in l or "def master_audio" in l or "def sweet_tube" in l or "def apply_deesser" in l:
        print(f"{i+1}: {l.strip()}")
