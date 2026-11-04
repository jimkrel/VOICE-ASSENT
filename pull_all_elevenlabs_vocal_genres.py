import os
os.environ['HF_HOME'] = r'E:\VoiceAI\cache'
import json
import urllib.request
import ssl
import subprocess
import soundfile as sf
import scipy.signal as signal
from transformers import WhisperProcessor, WhisperForConditionalGeneration

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    'https://api.elevenlabs.io/v1/voices',
    headers={'User-Agent': 'Mozilla/5.0'}
)

print("Fetching all voices from ElevenLabs API...")
with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    voices = data.get('voices', [])

PRESET_DIR = r"E:\VoiceAI\presets"
os.makedirs(PRESET_DIR, exist_ok=True)

print("Loading local Whisper model...")
processor = WhisperProcessor.from_pretrained("openai/whisper-tiny.en")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny.en")

# Define target voices mapping
TARGET_VOICES = {
    # 1. American Male
    "Adam": {"genre": "⚡ Shorts & Hook", "accent": "American", "gender": "male", "desc": "US Nam • Đanh thép, quyền lực, nhịp dồn dập • Shorts, Tech Review"},
    "Brian": {"genre": "🎬 Documentary & Essay", "accent": "American", "gender": "male", "desc": "US Nam • Trầm ấm, truyền cảm sâu lắng • Video Essay, Phim tài liệu"},
    "Roger": {"genre": "🎙 Podcast & Conversational", "accent": "American", "gender": "male", "desc": "US Nam • Tự nhiên, phóng khoáng, phong độ • Podcast, Vlogs"},
    "Eric": {"genre": "💼 Corporate & Review", "accent": "American", "gender": "male", "desc": "US Nam • Lịch lãm, đáng tin cậy • Tài chính, Doanh nghiệp"},
    "Will": {"genre": "🎮 Chill & Gaming", "accent": "American", "gender": "male", "desc": "US Nam • Thư thái, gần gũi, trẻ trung • Gaming, Chill Story"},
    "Callum": {"genre": "🎭 Character & Animation", "accent": "American", "gender": "male", "desc": "US Nam • Giọng khàn nhân vật, kịch tính • Hoạt hình, Phim"},
    "Bill": {"genre": "📜 Old Sage & History", "accent": "American", "gender": "male", "desc": "US Nam • Lão thành thông thái, uyên bác • Lịch sử, Sách kinh điển"},

    # 2. American Female
    "Sarah": {"genre": "📺 News & Television", "accent": "American", "gender": "female", "desc": "US Nữ • Chững chạc, điềm tĩnh, chuyên nghiệp • Bản tin, TV, Đánh giá"},
    "Matilda": {"genre": "💡 Explainer & How-To", "accent": "American", "gender": "female", "desc": "US Nữ • Tươi sáng, rành mạch, dễ hiểu • Hướng dẫn, Đời sống"},
    "Jessica": {"genre": "✨ Vlog & Lifestyle", "accent": "American", "gender": "female", "desc": "US Nữ • Trẻ trung, ngọt ngào, tươi vui • Lifestyle, Vlogs, Shorts"},
    "Laura": {"genre": "🔥 Pop Culture & Reaction", "accent": "American", "gender": "female", "desc": "US Nữ • Cá tính, sắc sảo, năng động • Reaction, Pop Culture"},
    "Bella": {"genre": "📖 Audiobook & Narration", "accent": "American", "gender": "female", "desc": "US Nữ • Dịu dàng, chuẩn phát thanh • Đọc truyện, Sách nói"},

    # 3. British Male
    "George": {"genre": "📖 British Storyteller", "accent": "British", "gender": "male", "desc": "UK Nam • Trầm ấm, quý phái, lôi cuốn • Kể chuyện, Phim tài liệu"},
    "Daniel": {"genre": "🎙 Formal News Anchor", "accent": "British", "gender": "male", "desc": "UK Nam • Chuẩn đài BBC, trang trọng, quyền uy • Thời sự, Phân tích"},

    # 4. British Female
    "Alice": {"genre": "🔬 Science & Academic", "accent": "British", "gender": "female", "desc": "UK Nữ • Chuẩn giọng Anh học thuật, sư phạm • Khoa học, E-learning"},
    "Lily": {"genre": "🎭 Drama & Literature", "accent": "British", "gender": "female", "desc": "UK Nữ • Nhung mượt diễn xuất, giàu cảm xúc • Kịch nghệ, Văn học"}
}

catalog = {}

for v in voices:
    vname = v.get('name', '')
    first_name = vname.split(' - ')[0].strip()
    
    if first_name in TARGET_VOICES:
        meta = TARGET_VOICES[first_name]
        purl = v.get('preview_url')
        if not purl:
            continue
            
        slug = f"eleven_{first_name.lower()}"
        raw_mp3 = os.path.join(PRESET_DIR, f"{slug}_raw.mp3")
        wav_path = os.path.join(PRESET_DIR, f"{slug}.wav")
        
        print(f"\n[Downloading] {first_name} ({meta['accent']} {meta['gender']})...")
        try:
            urllib.request.urlretrieve(purl, raw_mp3)
            # Convert to 24000Hz mono wav
            cmd = ["ffmpeg", "-y", "-i", raw_mp3, "-ar", "24000", "-ac", "1", wav_path]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Transcribe with Whisper
            audio, sr = sf.read(wav_path)
            num_samples = int(len(audio) * 16000 / sr)
            audio_16k = signal.resample(audio, num_samples)
            feat = processor(audio_16k, sampling_rate=16000, return_tensors="pt").input_features
            pred = model.generate(feat)
            transcript = processor.batch_decode(pred, skip_special_tokens=True)[0].strip()
            
            full_title = f"{first_name} — ElevenLabs ({meta['accent']} {meta['gender'].capitalize()} • {meta['genre']})"
            
            catalog[full_title] = {
                "audio": wav_path,
                "text": transcript,
                "desc": meta["desc"],
                "gender": meta["gender"],
                "accent": meta["accent"],
                "genre": meta["genre"],
                "lang_category": "en",
                "type": "elevenlabs",
                "preset": True
            }
            print(f" -> OK: '{transcript}'")
        except Exception as e:
            print(f" -> Error on {first_name}: {e}")

out_json = r"E:\VoiceAI\elevenlabs_catalog.json"
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(catalog, f, ensure_ascii=False, indent=2)

print(f"\n✨ Successfully downloaded and transcribed {len(catalog)} voices! Saved catalog to {out_json}")
