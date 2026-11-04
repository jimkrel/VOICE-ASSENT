with open(r"E:\VoiceAI\studio_app.py", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = [m.group(0) for m in re.finditer(r'title-row[^{]*\{[^}]*\}', text)]
for m in matches:
    print(m)
    print("-" * 20)

matches2 = [m.group(0) for m in re.finditer(r'#inspector[^{]*\{[^}]*\}', text)]
for m in matches2:
    print(m)
    print("-" * 20)
