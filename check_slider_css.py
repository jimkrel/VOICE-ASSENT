with open(r"E:\VoiceAI\studio_app.py", "r", encoding="utf-8") as f:
    text = f.read()

import re
m = re.findall(r'\.el-slider-head[^{]*\{[^}]*\}', text)
for x in m:
    print(x)

m2 = re.findall(r'\.sub-row[^{]*\{[^}]*\}', text)
for x in m2:
    print(x)
