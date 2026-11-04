import os, sys, time
os.environ['HF_HOME'] = r'E:\VoiceAI\hf_cache'
os.environ['TORCH_HOME'] = r'E:\VoiceAI\torch_cache'
os.environ['TEMP'] = r'E:\VoiceAI\temp'

from huggingface_hub import hf_hub_download

repo_id = 'k2-fsa/OmniVoice'
files_to_download = [
    'config.json',
    'tokenizer.json',
    'tokenizer_config.json',
    'chat_template.jinja',
    'audio_tokenizer/config.json',
    'audio_tokenizer/preprocessor_config.json',
    'audio_tokenizer/model.safetensors',
    'model.safetensors',
]

print(f"🚀 Bắt đầu tải {len(files_to_download)} files của OmniVoice về E:\\VoiceAI\\hf_cache...")

for i, f in enumerate(files_to_download, 1):
    print(f"\n[{i}/{len(files_to_download)}] Đang tải {f}...")
    t0 = time.time()
    path = hf_hub_download(repo_id=repo_id, filename=f)
    sz = os.path.getsize(path) / (1024**2)
    print(f"✅ Hoàn thành {f} ({sz:.2f} MB) trong {time.time()-t0:.1f}s")

print("\n🎉 Toàn bộ model OmniVoice đã được tải hoàn tất!")
