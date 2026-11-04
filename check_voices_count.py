import sys
sys.path.append(r'E:\VoiceAI')
from studio_app import all_voices
v = all_voices()
print("TOTAL VOICES AVAILABLE IN STUDIO:", len(v))
for i, name in enumerate(v.keys(), 1):
    info = v[name]
    print(f"{i:2d}. {name} | {info.get('desc')}")
