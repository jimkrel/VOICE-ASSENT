import subprocess
import time
import json
import urllib.request
import os

ART_DIR = r"C:\Users\jinnr\.gemini\antigravity\brain\8d36b352-add6-40e0-84f2-30ff15335bbb"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Launch chrome with remote debugging
proc = subprocess.Popen([
    CHROME,
    "--headless=new",
    "--remote-debugging-port=9222",
    "--disable-gpu",
    "--window-size=1600,900",
    "--force-dark-mode",
    "http://127.0.0.1:7860/voice-creation"
])

time.sleep(3)
try:
    # Get webSocketDebuggerUrl
    res = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(res.read().decode())
    target = tabs[0]
    ws_url = target["webSocketDebuggerUrl"]
    print("Attached to target:", target["url"])

    # Connect via standard simple socket
    import socket
    import base64
    import hashlib

    # Use websocket client if installed or simple js evaluation via CDP HTTP endpoint
    # CDP HTTP doesn't evaluate directly, but let's test if python has websocket-client
except Exception as e:
    print("Error:", e)
finally:
    proc.terminate()
