with open('E:/VoiceAI/studio_mockup.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'inspector' in line.lower() and ('id=' in line or 'class=' in line):
        print(f"Line {i+1}: {line.strip()[:100]}")
