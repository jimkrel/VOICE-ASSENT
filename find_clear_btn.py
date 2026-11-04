with open('E:/VoiceAI/studio_app.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# check clear_btn in studio_app.py
matches = [line for line in text.splitlines() if 'clear_btn' in line]
print("clear_btn occurrences:")
for m in matches:
    print(m)
