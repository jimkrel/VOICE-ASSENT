with open('E:/VoiceAI/studio_mockup.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'Tạo giọng nói' in line or 'btn-generate' in line or 'Xóa' in line:
        print(f"Line {i+1}: {line.strip()[:100]}")
