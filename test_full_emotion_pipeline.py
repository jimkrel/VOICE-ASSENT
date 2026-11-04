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
    lines = raw_text.split('\n')
    current_emotion = "calm"
    segments = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
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
                segments.append({
                    "text": tok,
                    "emotion": current_emotion
                })
    return segments

def split_smart_sentences(text, max_len=180):
    text = text.strip()
    paras = [p.strip() for p in text.split('\n') if p.strip()]
    chunks = []
    for p in paras:
        raw_sents = re.split(r'(?<=[.!?])\s+', p)
        for s in raw_sents:
            s = s.strip()
            if not s:
                continue
            if len(s) <= max_len:
                chunks.append(s)
            else:
                clauses = re.split(r'(?<=[,;])\s+', s)
                buf = ""
                for c in clauses:
                    if len(buf) + len(c) + 1 <= max_len:
                        buf = f"{buf} {c}".strip()
                    else:
                        if buf:
                            chunks.append(buf)
                        buf = c
                if buf:
                    chunks.append(buf)
    return chunks if chunks else [text]

def parse_and_chunk_script(raw_text, lang="English"):
    raw_segments = parse_emotion_script(raw_text)
    final_chunks = []
    for seg in raw_segments:
        text = seg["text"].strip()
        if not text:
            continue
        sub_sents = split_smart_sentences(text, max_len=180)
        for s in sub_sents:
            final_chunks.append({
                "text": s,
                "emotion": seg["emotion"]
            })
    return final_chunks

test_input = """
[kịch tính] The year was 1994. Deep inside the Black Forest, investigators discovered an abandoned radio tower.
[thì thầm] Every night at precisely 3:15 AM, the transmission repeated the exact same pattern.
[hào hứng] Stop scrolling! What if I told you this voice is fully generated locally?
[điềm tĩnh] Thank you for listening.
"""

chunks = parse_and_chunk_script(test_input)
print(f"Total chunks: {len(chunks)}")
for i, c in enumerate(chunks):
    print(f"[{i+1}] ({c['emotion']}): {c['text']}")
