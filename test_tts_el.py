import os
os.environ['HF_HOME'] = r'E:\VoiceAI\cache'
from gradio_client import Client

client = Client('http://127.0.0.1:7860')
print("Testing TTS with Adam (ElevenLabs Original)...")
res = client.predict(
    voice='Adam — ElevenLabs (US Dominant & Firm Male)',
    text='Stop scrolling! The vocal timbre you are hearing is cloned directly from ElevenLabs running locally on our GPU.',
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
print("TTS Success! Output audio:", res[0])
print("Status:", res[1].strip())
