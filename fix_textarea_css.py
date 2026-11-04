with open(r"E:\VoiceAI\studio_app.py", "r", encoding="utf-8") as f:
    text = f.read()

target = """#voice_sample_audio_player {
  display: none !important;
}
\"\"\""""

replacement = """#voice_sample_audio_player {
  display: none !important;
}"""

if target in text:
    text = text.replace(target, replacement, 1)
    print("Removed premature quote")

target_crlf = target.replace("\n", "\r\n")
if target_crlf in text:
    text = text.replace(target_crlf, replacement.replace("\n", "\r\n"), 1)
    print("Removed premature quote (crlf)")

# Now place """ right before JS_INJECT
if 'padding: 8px 10px !important;\n}\n\n\nJS_INJECT = """' in text:
    text = text.replace('padding: 8px 10px !important;\n}\n\n\nJS_INJECT = """', 'padding: 8px 10px !important;\n}\n"""\n\nJS_INJECT = """')
    print("Added quote before JS_INJECT")
elif 'padding: 8px 10px !important;\r\n}\r\n\r\n\r\nJS_INJECT = """' in text:
    text = text.replace('padding: 8px 10px !important;\r\n}\r\n\r\n\r\nJS_INJECT = """', 'padding: 8px 10px !important;\r\n}\r\n"""\r\n\r\nJS_INJECT = """')
    print("Added quote before JS_INJECT (crlf)")

with open(r"E:\VoiceAI\studio_app.py", "w", encoding="utf-8") as f:
    f.write(text)
