with open('E:/VoiceAI/studio_app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'DEFAULT_SCRIPT' in line or 'DEFAULT_SAMPLE' in line or 'Năm 1994' in line:
        print(f"Line {i+1}: {line.strip()[:100]}")
