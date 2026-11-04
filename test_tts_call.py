from gradio_client import Client

client = Client('http://127.0.0.1:7860')
print("Testing /tts endpoint...")
res = client.predict(
    voice='Marcus — Documentary & Crime (US Deep Male)',
    text='Hello from automated verification.',
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
print("TTS Success! Result:", res)
