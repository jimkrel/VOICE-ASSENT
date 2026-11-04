with open('E:/VoiceAI/studio_mockup.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'<div class=\"textarea-actions\">([\s\S]*?)</div>', text)
if m:
    print("Found textarea-actions:")
    print(m.group(1))
else:
    print("Could not find textarea-actions")
