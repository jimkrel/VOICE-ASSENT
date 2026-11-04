import os
os.environ['HF_HOME'] = r'E:\VoiceAI\cache'
import json
import urllib.request
import ssl
import subprocess
import soundfile as sf
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    'https://api.elevenlabs.io/v1/voices',
    headers={'User-Agent': 'Mozilla/5.0'}
)

print("Fetching voices from ElevenLabs API...")
with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    voices = data.get('voices', [])

print(f"Total premade voices found: {len(voices)}")

# Let's pick 5 iconic ElevenLabs voices
selected_names = [
    'Adam - Dominant, Firm',
    'George - Warm, Captivating Storyteller',
    'Sarah - Mature, Reassuring, Confident',
    'Alice - Clear, Engaging Educator',
    'Brian - Deep, Resonant and Comforting'
]

processor = WhisperProcessor.from_pretrained("openai/whisper-tiny.en")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny.en")

PRESET_DIR = r"E:\VoiceAI\presets"
os.makedirs(PRESET_DIR, exist_ok=True)

results = {}
for v in voices:
    name = v.get('name')
    if name in selected_names or any(s.split(' - ')[0] == name.split(' - ')[0] for s in selected_names):
        short_name = name.split(' - ')[0].lower()
        purl = v.get('preview_url')
        if not purl:
            continue
        
        raw_path = os.path.join(PRESET_DIR, f"eleven_{short_name}_raw.mp3")
        wav_path = os.path.join(PRESET_DIR, f"eleven_{short_name}.wav")
        
        print(f"\nProcessing {name}...")
        urllib.request.urlretrieve(purl, raw_path)
        
        # Convert to 24000Hz mono wav
        cmd = ["ffmpeg", "-y", "-i", raw_path, "-ar", "24000", "-ac", "1", wav_path]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Transcribe
        audio, sr = sf.read(wav_path)
        # Resample to 16000 for whisper
        import scipy.signal as signal
        num_samples = int(len(audio) * 16000 / sr)
        audio_16k = signal.resample(audio, num_samples)
        
        feat = processor(audio_16k, sampling_rate=16000, return_tensors="pt").input_features
        pred = model.generate(feat)
        transcript = processor.batch_decode(pred, skip_special_tokens=True)[0].strip()
        
        results[name] = {
            "wav": wav_path,
            "transcript": transcript,
            "desc": v.get("description", ""),
            "labels": v.get("labels", {})
        }
        print(f"-> {short_name}: '{transcript}' ({os.path.getsize(wav_path)} bytes)")

print("\nDone! Results:")
print(json.dumps(results, indent=2))
