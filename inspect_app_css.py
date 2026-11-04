with open('E:/VoiceAI/studio_app.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'(\.el-clean-slider[^{]*\{[^}]+\}|\.el-slider-head[^{]*\{[^}]+\}|\.el-switch[^{]*\{[^}]+\}|\.el-format-pill[^{]*\{[^}]+\})', text)
for m in matches:
    print(m)
    print('-'*30)
