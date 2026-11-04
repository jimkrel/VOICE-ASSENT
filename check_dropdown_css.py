import re

with open(r"E:\VoiceAI\studio_app.py", "r", encoding="utf-8") as f:
    text = f.read()

patterns = [
    r'\.el-pill-dd[^{]*\{[^}]*\}',
    r'#voice_dd[^{]*\{[^}]*\}',
    r'select\s*\{[^}]*\}',
    r'\.single-select[^{]*\{[^}]*\}',
    r'gradio-dropdown[^{]*\{[^}]*\}',
]

for p in patterns:
    print(f"=== Pattern: {p} ===")
    matches = re.findall(p, text, re.IGNORECASE)
    for m in matches[:5]:
        print(m)
        print("-" * 20)
