import subprocess
import urllib.request
import json
import os

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ART_DIR = r"C:\Users\jinnr\.gemini\antigravity\brain\8d36b352-add6-40e0-84f2-30ff15335bbb"

# 1. Verify backend metrics
req = urllib.request.urlopen("http://127.0.0.1:7860/api/system/metrics", timeout=10)
metrics = json.loads(req.read().decode("utf-8"))
print("System Metrics via Next.js proxy:", json.dumps(metrics["hardware"], ensure_ascii=False))

# 2. Capture all 4 tabs on desktop 1600x900
tabs = [
    ("text-to-speech", "tab1_tts.png"),
    ("voice-creation", "tab2_create.png"),
    ("voice-changer", "tab3_changer.png"),
    ("voice-library", "tab4_library.png"),
]

for tab, fname in tabs:
    out_path = os.path.join(ART_DIR, fname)
    url = f"http://127.0.0.1:7860/?tab={tab}"
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=1600,900",
        "--force-dark-mode",
        "--virtual-time-budget=4000",
        f"--screenshot={out_path}",
        url,
    ]
    subprocess.run(cmd, check=True)
    print(f"Captured {tab} -> {out_path} ({os.path.getsize(out_path)} bytes)")
