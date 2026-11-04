import urllib.request

html = urllib.request.urlopen("http://127.0.0.1:7860").read().decode("utf-8")
print(f"HTML length: {len(html)}")
with open(r"E:\VoiceAI\page.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Saved page.html")
