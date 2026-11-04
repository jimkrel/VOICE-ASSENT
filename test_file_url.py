import urllib.request
try:
    url = 'http://127.0.0.1:7860/file=E:/VoiceAI/presets/eleven_adam.wav'
    req = urllib.request.urlopen(url)
    print("Status:", req.status, "Content-Length:", req.headers.get('Content-Length'))
except Exception as e:
    print("Error:", e)
