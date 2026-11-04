import subprocess
import time
import json
import urllib.request
import os

ART_DIR = r"C:\Users\jinnr\.gemini\antigravity\brain\8d36b352-add6-40e0-84f2-30ff15335bbb"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Launch Chrome with remote debugging to inspect console errors
proc = subprocess.Popen([
    CHROME,
    "--headless=new",
    "--remote-debugging-port=9223",
    "--disable-gpu",
    "http://127.0.0.1:7860/"
])

time.sleep(3)
try:
    tabs = json.loads(urllib.request.urlopen("http://127.0.0.1:9223/json").read().decode())
    print("Open tabs in Chrome:", len(tabs))
    for t in tabs:
        print("Tab:", t.get("url"), t.get("title"))
except Exception as e:
    print("Error:", e)
finally:
    proc.terminate()
