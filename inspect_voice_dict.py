import json
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    'https://api.elevenlabs.io/v1/voices',
    headers={'User-Agent': 'Mozilla/5.0'}
)
with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    voices = data.get('voices', [])
    for v in voices:
        if v.get('name') == 'Adam':
            print(json.dumps(v, indent=2))
            break
