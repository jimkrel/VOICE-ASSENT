with open('E:/VoiceAI/studio_mockup.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '.slider-card' in line or '.toggle-switch' in line or '.el-range-input' in line:
        print(f"Line {i+1}: {line.strip()}")
