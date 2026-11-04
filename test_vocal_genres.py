from gradio_client import Client

client = Client('http://127.0.0.1:7860')
print("Testing TTS with Sarah (American Female • News & TV)...")
res1 = client.predict(
    voice='Sarah — ElevenLabs (American Female • 📺 News & Television)',
    text='Good evening. Here are the top technological developments breaking across the world right now.',
    lang='English',
    speed=1.05,
    stability=0.45,
    similarity=0.8,
    style_exag=0.1,
    model_choice='Eleven v4 (Turbo)',
    denoise=False,
    speaker_boost=True,
    api_name='/tts'
)
print("Sarah Success:", res1[0])

print("\nTesting TTS with Daniel (British Male • News Anchor)...")
res2 = client.predict(
    voice='Daniel — ElevenLabs (British Male • 🎙 Formal News Anchor)',
    text='Welcome to this global report, analyzing the subtle forces reshaping the modern digital economy.',
    lang='English',
    speed=1.05,
    stability=0.45,
    similarity=0.8,
    style_exag=0.1,
    model_choice='Eleven v4 (Turbo)',
    denoise=False,
    speaker_boost=True,
    api_name='/tts'
)
print("Daniel Success:", res2[0])
