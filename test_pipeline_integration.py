from studio_app import parse_and_chunk_script, status_html, EMOTION_PROFILES, EMOTION_TAGS

test_script = """
[kịch tính] The year was 1994. Deep inside the Black Forest, investigators discovered an abandoned radio tower.
[thì thầm] Every night at precisely 3:15 AM, the transmission repeated the exact same pattern.
[hào hứng] Stop scrolling! What if I told you this voice is fully generated locally?
[điềm tĩnh] Thank you for listening.
"""

chunks = parse_and_chunk_script(test_script)
print(f"Chunks generated: {len(chunks)}")
emotions_used = []
for i, c in enumerate(chunks):
    print(f"  Chunk {i+1} [{c['emotion']}]: {c['text']}")
    emotions_used.append(c['emotion'])

html = status_html(12.4, 18.2, 14, chunks=len(chunks), emotions_used=emotions_used)
assert "auto-dismiss" in html
assert "data-time=\"10\"" in html
assert "el-countdown-badge" in html
assert "el-status-progress-bar" in html
assert "dramatic" in html
assert "whisper" in html
assert "excited" in html

print("SUCCESS: Full pipeline integration verified!")
