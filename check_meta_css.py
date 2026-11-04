with open(r"E:\VoiceAI\studio_app.py", "r", encoding="utf-8") as f:
    text = f.read()

import re
patterns = [
    r'\.s-desc[^{]*\{[^}]*\}',
    r'\.s-quote[^{]*\{[^}]*\}',
    r'\.el-model-meta-box[^{]*\{[^}]*\}',
    r'\.m-desc[^{]*\{[^}]*\}',
]

for p in patterns:
    matches = re.findall(p, text)
    print(f"Pattern {p}:")
    for m in matches:
        print(m)
        print("-" * 20)
