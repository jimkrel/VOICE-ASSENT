from gradio_client import Client
import time

try:
    client = Client("http://127.0.0.1:7860/")
    print("Connected to Gradio server!")
    # Test text
    test_text = "The year was 1994. Deep inside the Black Forest, investigators discovered an abandoned radio tower broadcasting an unbroken 7-digit code."
    
    t0 = time.time()
    result = client.predict(
        voice="🎙️ Marcus — Phóng sự & Bí ẩn (US Deep Male)",
        text=test_text,
        lang="English",
        speed=1.05,
        stability=0.45,
        similarity=0.80,
        style_exag=0.15,
        model_mode_name="⚡ Eleven v4 Style (Turbo & Siêu cảm xúc • Shorts / Viral)",
        yt_master=True,
        api_name="/tts"
    )
    print(f"Inference test SUCCESS in {time.time() - t0:.2f}s! Output:", result)
except Exception as e:
    print("API test info:", e)
