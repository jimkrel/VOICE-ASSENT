import re

EMOTION_TAGS = {
    "thì thầm": "whisper",
    "whisper": "whisper",
    "kịch tính": "dramatic",
    "dramatic": "dramatic",
    "hào hứng": "excited",
    "excited": "excited",
    "buồn": "sad",
    "sad": "sad",
    "buồn bã": "sad",
    "tức giận": "angry",
    "angry": "angry",
    "thở dài": "sigh",
    "sigh": "sigh",
    "điềm tĩnh": "calm",
    "calm": "calm",
}

TAG_REGEX = re.compile(r'\[(.*?)\]', re.IGNORECASE)

def parse_emotion_script(raw_text):
    # Splits script into segments while retaining the emotion state
    lines = raw_text.split('\n')
    current_emotion = "calm"
    segments = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Tokenize by tags
        tokens = re.split(r'(\[.*?\])', line)
        for tok in tokens:
            tok = tok.strip()
            if not tok:
                continue
            m = TAG_REGEX.match(tok)
            if m:
                tag_content = m.group(1).strip().lower()
                if tag_content in EMOTION_TAGS:
                    current_emotion = EMOTION_TAGS[tag_content]
            else:
                # Actual text
                segments.append({
                    "text": tok,
                    "emotion": current_emotion
                })
    return segments

sample = """
[kịch tính] The year was 1994. Deep inside the Black Forest, investigators discovered an abandoned radio tower.
[thì thầm] Every night at precisely 3:15 AM, the transmission repeated the exact same pattern.
[hào hứng] Now, he only has twenty-four hours to uncover the truth!
"""

segs = parse_emotion_script(sample)
print(f"Parsed {len(segs)} segments:")
for i, s in enumerate(segs):
    print(f"  [{i+1}] ({s['emotion']}): {s['text']}")
