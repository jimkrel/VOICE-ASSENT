import subprocess
import os

browser = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out_png = r"E:\VoiceAI\screenshot.png"
if os.path.exists(out_png):
    os.remove(out_png)

cmd = [
    browser,
    "--headless",
    "--disable-gpu",
    "--window-size=1600,1000",
    "--virtual-time-budget=6000",
    f"--screenshot={out_png}",
    "http://127.0.0.1:7860"
]
res = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
print(f"Screenshot saved, size={os.path.getsize(out_png) if os.path.exists(out_png) else 0} bytes")
