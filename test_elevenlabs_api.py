import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    req = urllib.request.Request(
        'https://api.elevenlabs.io/v1/voices',
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        voices = data.get('voices', [])
        print(f"Total voices returned: {len(voices)}")
        for v in voices:
            name = v.get('name')
            purl = v.get('preview_url')
            labels = v.get('labels', {})
            print(f"- {name}: {purl} | {labels}")
except Exception as e:
    print("API Error:", e)
