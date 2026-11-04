import subprocess
import time
import os

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ART_DIR = r"C:\Users\jinnr\.gemini\antigravity\brain\8d36b352-add6-40e0-84f2-30ff15335bbb"

# Take screenshot of /voice-creation
out_before = os.path.join(ART_DIR, "demo_test_ready.png")
cmd = [
    CHROME,
    "--headless=new",
    "--disable-gpu",
    "--hide-scrollbars",
    "--window-size=1600,900",
    "--force-dark-mode",
    "--virtual-time-budget=3000",
    f"--screenshot={out_before}",
    "http://127.0.0.1:7860/voice-creation",
]
subprocess.run(cmd, check=True)
print("Captured demo ready screenshot ->", out_before, f"({os.path.getsize(out_before)} bytes)")
