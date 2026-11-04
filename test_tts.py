from gradio_client import Client
import time

client = Client("http://127.0.0.1:7860/")
print("Calling /tts...")
t0 = time.time()
res = client.predict(
    "Marcus — Documentary & Crime (US Deep Male)",
    "The year was 1994. Deep inside the Black Forest, investigators discovered an abandoned radio tower.",
    "English",
    1.05,
    0.45,
    0.80,
    0.10,
    "Eleven v4 (Turbo)",
    False,
    True,
    api_name="/tts"
)
print(f"SUCCESS in {time.time() - t0:.2f}s! Output:", res)
