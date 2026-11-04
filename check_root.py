import re

with open(r"E:\VoiceAI\studio_app.py", "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r':root\s*\{[^}]*\}', text)
if m:
    print(m.group(0))
else:
    print("No :root found")
