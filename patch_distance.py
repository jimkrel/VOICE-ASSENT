p = r'E:\VoiceAI\ui_v2\lib\voice-catalog.ts'
with open(p, 'r', encoding='utf-8') as f:
    text = f.read()
text = text.replace('distance: "Xa"', 'distance: "Vừa"')
with open(p, 'w', encoding='utf-8') as f:
    f.write(text)
print('Done!')
