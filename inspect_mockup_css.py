with open('E:/VoiceAI/studio_mockup.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'(\.slider-card[^{]*\{[^}]+\}|\.el-range-input[^{]*\{[^}]+\}|\.el-fx-[^{]*\{[^}]+\}|\.toggle-switch[^{]*\{[^}]+\})', text)
for m in matches[:15]:
    print(m)
    print('-'*40)
