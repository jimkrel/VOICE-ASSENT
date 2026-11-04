import re

with open(r"E:\VoiceAI\studio_app.py", "r", encoding="utf-8") as f:
    text = f.read()

vars_used = set(re.findall(r'var\(--([a-zA-Z0-9_-]+)\)', text))
print("Variables used:", vars_used)
