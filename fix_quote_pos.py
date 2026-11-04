with open(r"E:\VoiceAI\studio_app.py", "r", encoding="utf-8") as f:
    text = f.read()

# Fix the placement of """
target = """100% { transform: rotate(360deg); }
}
\"\"\""""

replacement = """100% { transform: rotate(360deg); }
}"""

if target in text:
    text = text.replace(target, replacement, 1)
    print("Removed premature quote")

target_crlf = target.replace("\n", "\r\n")
if target_crlf in text:
    text = text.replace(target_crlf, replacement.replace("\n", "\r\n"), 1)
    print("Removed premature quote (crlf)")

# Now place """ before JS_INJECT
if 'display: none !important;\n}\n\n\nJS_INJECT = """' in text:
    text = text.replace('display: none !important;\n}\n\n\nJS_INJECT = """', 'display: none !important;\n}\n"""\n\nJS_INJECT = """')
    print("Added quote before JS_INJECT")
elif 'display: none !important;\r\n}\r\n\r\n\r\nJS_INJECT = """' in text:
    text = text.replace('display: none !important;\r\n}\r\n\r\n\r\nJS_INJECT = """', 'display: none !important;\r\n}\r\n"""\r\n\r\nJS_INJECT = """')
    print("Added quote before JS_INJECT (crlf)")

with open(r"E:\VoiceAI\studio_app.py", "w", encoding="utf-8") as f:
    f.write(text)
