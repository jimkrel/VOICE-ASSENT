with open(r"E:\VoiceAI\studio_app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "theme =" in l or "gr.Blocks(" in l or "css =" in l or "CSS =" in l or "custom_css" in l.lower():
        print(f"{i+1}: {l.strip()[:100]}")
