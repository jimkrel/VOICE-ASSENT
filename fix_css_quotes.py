with open(r"E:\VoiceAI\studio_app.py", "r", encoding="utf-8") as f:
    text = f.read()

# Fix the early quote closure
bad_part = """  #nav label { justify-content: center !important; padding: 7px 0 !important; }
}
\"\"\""""

good_part = """  #nav label { justify-content: center !important; padding: 7px 0 !important; }
}"""

if bad_part in text:
    text = text.replace(bad_part, good_part, 1)
    print("Replaced bad_part")
else:
    # Try with \r\n
    bad_part_crlf = bad_part.replace("\n", "\r\n")
    if bad_part_crlf in text:
        text = text.replace(bad_part_crlf, good_part.replace("\n", "\r\n"), 1)
        print("Replaced bad_part_crlf")
    else:
        print("bad_part not found")

# Now ensure the CSS string is closed before JS_INJECT = """
if '100% { transform: rotate(360deg); }\n}\n\n\nJS_INJECT = """' in text:
    text = text.replace('100% { transform: rotate(360deg); }\n}\n\n\nJS_INJECT = """', '100% { transform: rotate(360deg); }\n}\n"""\n\nJS_INJECT = """')
    print("Added closing quote before JS_INJECT")
elif '100% { transform: rotate(360deg); }\r\n}\r\n\r\n\r\nJS_INJECT = """' in text:
    text = text.replace('100% { transform: rotate(360deg); }\r\n}\r\n\r\n\r\nJS_INJECT = """', '100% { transform: rotate(360deg); }\r\n}\r\n"""\r\n\r\nJS_INJECT = """')
    print("Added closing quote before JS_INJECT (crlf)")
else:
    print("orb transform not found")

with open(r"E:\VoiceAI\studio_app.py", "w", encoding="utf-8") as f:
    f.write(text)
