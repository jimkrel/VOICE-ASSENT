import os, sys

# Redirect all HuggingFace and PyTorch model caches to drive E: to preserve drive C:!
os.environ['HF_HOME'] = r'E:\VoiceAI\hf_cache'
os.environ['TORCH_HOME'] = r'E:\VoiceAI\torch_cache'
os.environ['TEMP'] = r'E:\VoiceAI\temp'
os.environ['TMP'] = r'E:\VoiceAI\temp'

from f5_tts.infer.infer_gradio import app

if __name__ == "__main__":
    print("Launching F5-TTS Voice Studio on http://127.0.0.1:7860 ...")
    app.launch(server_name="127.0.0.1", server_port=7860, share=False)
