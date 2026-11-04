import os
os.environ['HF_HOME'] = r'E:\VoiceAI\cache'
import soundfile as sf
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration

audio, sr = sf.read(r"E:\VoiceAI\presets\eleven_adam.wav")
processor = WhisperProcessor.from_pretrained("openai/whisper-tiny.en")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny.en")

input_features = processor(audio, sampling_rate=16000, return_tensors="pt").input_features
predicted_ids = model.generate(input_features)
transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
print("Transcript:", transcription[0].strip())
