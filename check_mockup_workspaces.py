with open('E:/VoiceAI/studio_mockup.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<div class=\"workspace-[^\"]*\"[^>]*>|<section id=\"[^\"]*\"[^>]*>', text)
print("Workspace sections found in studio_mockup.html:")
for m in matches[:10]:
    print(m)
