with open('E:/VoiceAI/studio_app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'script =' in line:
        print(f"Line {i+1}: {line.strip()[:120]}")
        for j in range(i, min(i+15, len(lines))):
            print(f"  {j+1}: {lines[j].rstrip()}")
