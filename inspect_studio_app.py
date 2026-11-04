with open('E:/VoiceAI/studio_app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'with gr.Column(elem_id="sidebar"' in line or 'with gr.Column(elem_id="inspector"' in line:
        print(f"Line {i+1}: {line.strip()}")
    if 'elem_id="inspector"' in line:
        print("Found inspector at line:", i+1)
        for j in range(i, min(i+100, len(lines))):
            print(f"{j+1}: {lines[j].rstrip()}")
