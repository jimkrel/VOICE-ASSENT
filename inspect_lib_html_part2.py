with open('E:/VoiceAI/studio_app.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'def render_voice_library_html[\s\S]*?(?=\ndef )', text)
if m:
    print(m.group(0)[1400:3000])
