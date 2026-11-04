with open(r"E:\VoiceAI\studio_app.py", "r", encoding="utf-8") as f:
    text = f.read()

import re
patterns = [r'\.s-head-row[^{]*\{[^}]*\}', r'\.voice-circle-play-btn[^{]*\{[^}]*\}']
for p in patterns:
    for m in re.findall(p, text):
        print(m)
