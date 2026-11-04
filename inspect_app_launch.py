with open('E:/VoiceAI/studio_app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for j in range(max(0, len(lines)-30), len(lines)):
    print(f"{j+1}: {lines[j].rstrip()}")
