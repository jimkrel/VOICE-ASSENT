with open(r"E:\VoiceAI\studio_app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "el-status-pill" in l:
        print(f"{i+1}: {l.strip()[:80]}")
