import subprocess
import os

browser = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out_png = r"E:\VoiceAI\mockup_screenshot.png"
if os.path.exists(out_png):
    os.remove(out_png)

cmd = [
    browser,
    "--headless",
    "--disable-gpu",
    "--window-size=1600,1000",
    "--virtual-time-budget=3000",
    f"--screenshot={out_png}",
    "file:///E:/VoiceAI/studio_mockup.html"
]
res = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
print(f"Screenshot saved, size={os.path.getsize(out_png) if os.path.exists(out_png) else 0} bytes")
