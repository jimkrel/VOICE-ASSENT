import subprocess
import os

browser = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out_png = r"E:\VoiceAI\vlib_screenshot.png"
if os.path.exists(out_png):
    os.remove(out_png)

# We can capture mockup with JS injected or after switching to lib
script_js = "switchTool('lib');"

# Or we can create a temporary file that starts on lib
with open('E:/VoiceAI/studio_mockup.html', 'r', encoding='utf-8') as f:
    text = f.read()

text_lib = text.replace("switchTool('tts')", "switchTool('lib')")
text_lib = text_lib.replace('id="ws-tts" style="display: flex;', 'id="ws-tts" style="display: none;')
text_lib = text_lib.replace('id="ws-lib" style="display: none;', 'id="ws-lib" style="display: flex;')
text_lib = text_lib.replace('id="inspector"', 'id="inspector" style="display: none;"')
text_lib = text_lib.replace('id="crumb-tool">/ Đọc kịch bản (Text to Speech)', 'id="crumb-tool">/ Kho giọng đọc (Voice Library)')
text_lib = text_lib.replace('id="nav-tts" class="nav-item active"', 'id="nav-tts" class="nav-item"')
text_lib = text_lib.replace('id="nav-lib" class="nav-item"', 'id="nav-lib" class="nav-item active"')

with open('E:/VoiceAI/studio_mockup_lib.html', 'w', encoding='utf-8') as f:
    f.write(text_lib)

cmd = [
    browser,
    "--headless",
    "--disable-gpu",
    "--window-size=1600,1000",
    "--virtual-time-budget=3000",
    f"--screenshot={out_png}",
    "file:///E:/VoiceAI/studio_mockup_lib.html"
]
res = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
print(f"Voice library screenshot saved, size={os.path.getsize(out_png) if os.path.exists(out_png) else 0} bytes")
