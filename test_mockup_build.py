# Script to build full 4-workspace SPA in studio_mockup.html
import re

with open('E:/VoiceAI/studio_mockup.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's inspect CSS to see where we can add the workspace styles
print("Current studio_mockup.html length:", len(html))
