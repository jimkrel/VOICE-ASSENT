import torchaudio

path = r'E:\VoiceAI\presets\eleven_adam.mp3'
info = torchaudio.info(path)
print(f"Sample rate: {info.sample_rate}, Channels: {info.num_channels}, Duration: {info.num_frames / info.sample_rate:.2f}s")
