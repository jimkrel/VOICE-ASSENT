with open(r"E:\VoiceAI\studio_app.py", "r", encoding="utf-8") as f:
    text = f.read()

import re
m = re.findall(r'\.el-sample-quote-card[^{]*\{[^}]*\}', text)
for x in m:
    print(x)
