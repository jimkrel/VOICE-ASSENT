import re

with open(r"E:\VoiceAI\studio_app.py", "r", encoding="utf-8") as f:
    text = f.read()

for m in re.finditer(r'([^{}]*audio[^{}]*)\{([^}]*)\}', text, re.IGNORECASE):
    print("Selector:", m.group(1).strip())
    print("Body:", m.group(2).strip()[:80])
    print("-" * 30)
