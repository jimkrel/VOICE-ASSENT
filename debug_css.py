import re

with open(r"E:\VoiceAI\studio_app.py", "r", encoding="utf-8") as f:
    text = f.read()

patterns = [
    r'#sidebar\s*\{[^}]*\}',
    r'#nav\s*\{[^}]*\}',
    r'\.sidebar-bottom\s*\{[^}]*\}',
    r'#model_cards_radio[^{]*\{[^}]*\}',
    r'#voice_dd_input[^{]*\{[^}]*\}',
    r'\.el-logo-brand[^{]*\{[^}]*\}',
    r'\.brand-square[^{]*\{[^}]*\}',
    r'audio\s*\{[^}]*\}',
]

for p in patterns:
    print(f"=== Pattern: {p} ===")
    matches = re.findall(p, text, re.IGNORECASE)
    for m in matches[:3]:
        print(m)
        print("-" * 20)
