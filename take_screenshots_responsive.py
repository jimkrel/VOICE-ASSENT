import subprocess
import os
import sys

browser = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def capture(url, out_path, width=1600, height=817, dark=False):
    if os.path.exists(out_path):
        os.remove(out_path)
    
    cmd = [
        browser,
        "--headless",
        "--disable-gpu",
        f"--window-size={width},{height}",
        "--virtual-time-budget=6000",
    ]
    if dark:
        cmd.append("--force-dark-mode")
    cmd.extend([
        f"--screenshot={out_path}",
        url
    ])
    subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    print(f"Captured {out_path}, size={os.path.getsize(out_path) if os.path.exists(out_path) else 0}")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "desktop"
    if mode == "desktop_dark":
        capture("http://127.0.0.1:7860", r"E:\VoiceAI\screenshot_dark_1600x817.png", 1600, 817, dark=True)
    elif mode == "mobile":
        capture("http://127.0.0.1:7860", r"E:\VoiceAI\screenshot_mobile_375x812.png", 375, 812, dark=False)
