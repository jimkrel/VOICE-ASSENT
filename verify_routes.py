import subprocess
import urllib.request
import json
import os

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ART_DIR = r"C:\Users\jinnr\.gemini\antigravity\brain\8d36b352-add6-40e0-84f2-30ff15335bbb"

# 1. Verify direct route URLs and redirects
routes = [
    ("/text-to-speech", "route_tts.png"),
    ("/voice-creation", "route_create.png"),
    ("/voice-changer", "route_changer.png"),
    ("/voice-library", "route_library.png"),
]

for route, fname in routes:
    out_path = os.path.join(ART_DIR, fname)
    url = f"http://127.0.0.1:7860{route}"
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=1600,900",
        "--force-dark-mode",
        "--virtual-time-budget=3500",
        f"--screenshot={out_path}",
        url,
    ]
    subprocess.run(cmd, check=True)
    print(f"Captured {route} -> {out_path} ({os.path.getsize(out_path)} bytes)")

# 2. Check redirect from /
req = urllib.request.urlopen("http://127.0.0.1:7860/")
print("Redirect / ->", req.geturl())

# 3. Check redirect from ?tab=voice-creation
req2 = urllib.request.urlopen("http://127.0.0.1:7860/?tab=voice-creation")
print("Redirect /?tab=voice-creation ->", req2.geturl())
