with open(r"E:\VoiceAI\studio_app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if ".el-pill-dd" in l or "input" in l and "background" in l:
        print(f"{i+1}: {l.strip()[:100]}")
