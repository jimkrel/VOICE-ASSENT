import time
import subprocess
import os

browser = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def take_shot(path, delay=2):
    cmd = [
        browser,
        "--headless",
        "--disable-gpu",
        "--force-dark-mode",
        "--window-size=1600,817",
        f"--virtual-time-budget={delay * 1000}",
        f"--screenshot={path}",
        "http://127.0.0.1:7860"
    ]
    subprocess.run(cmd, capture_output=True, text=True, timeout=20)
    print("Saved:", path, "size:", os.path.getsize(path) if os.path.exists(path) else 0)

if __name__ == "__main__":
    take_shot(r"E:\VoiceAI\final_desktop_dark.png", delay=3)
