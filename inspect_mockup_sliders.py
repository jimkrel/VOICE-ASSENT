with open('E:/VoiceAI/studio_mockup.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect CSS for range input and switches
import re
css_matches = re.findall(r'(\.slider-card[\s\S]*?)(?=\n\s*\.[a-z]|\n\s*</style>)', text)
for c in css_matches[:8]:
    print(c[:400])
    print('='*50)
