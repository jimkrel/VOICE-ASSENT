"""
Kokoro-82M (StyleTTS2 Architecture) Inference Engine
High-fidelity, ultra-fast neural speech synthesis for Thanh Am Studio.
Output: 24,000 Hz float32 numpy audio, compatible with Studio Mastering chain.
"""

import os
import time
import logging
import numpy as np
import torch
from typing import Optional, Tuple, Dict, Any, List

logger = logging.getLogger("kokoro_engine")

_PIPELINES: Dict[str, Any] = {}
_DEVICE: Optional[str] = None

# Kokoro Voice Catalog
KOKORO_VOICES: List[Dict[str, Any]] = [
    {
        "id": "af_heart",
        "name": "Heart (Kokoro)",
        "engine": "kokoro",
        "style": "ấm áp, chân thực bậc nhất",
        "locale": "US",
        "gender": "Nữ",
        "language": "English (US)",
        "description": "Giọng nữ Mỹ truyền cảm, độ tự nhiên và cảm xúc cao nhất",
        "sampleText": "The year was 1994. Deep inside the Black Forest, investigators discovered an abandoned radio tower broadcasting an unbroken seven-digit code.",
        "categories": ["Kokoro 82M", "US English", "Nữ (Female)"],
        "source": "Kokoro-82M",
        "tone": "aqua",
    },
    {
        "id": "af_bella",
        "name": "Bella (Kokoro)",
        "engine": "kokoro",
        "style": "tươi sáng, rõ nét",
        "locale": "US",
        "gender": "Nữ",
        "language": "English (US)",
        "description": "Giọng nữ Mỹ trẻ trung, rõ ràng và giàu năng lượng",
        "sampleText": "Welcome to our studio. Everything you hear is generated in real time with neural speech synthesis.",
        "categories": ["Kokoro 82M", "US English", "Nữ (Female)"],
        "source": "Kokoro-82M",
        "tone": "coral",
    },
    {
        "id": "af_nicole",
        "name": "Nicole (Kokoro)",
        "engine": "kokoro",
        "style": "nhẹ nhàng, thì thầm",
        "locale": "US",
        "gender": "Nữ",
        "language": "English (US)",
        "description": "Giọng nữ Mỹ êm dịu, phù hợp audiobook và ASMR",
        "sampleText": "Close your eyes, take a deep breath, and let the quiet surrounding take over.",
        "categories": ["Kokoro 82M", "US English", "Nữ (Female)"],
        "source": "Kokoro-82M",
        "tone": "violet",
    },
    {
        "id": "am_adam",
        "name": "Adam (Kokoro)",
        "engine": "kokoro",
        "style": "trầm ấm, uy tín phát thanh",
        "locale": "US",
        "gender": "Nam",
        "language": "English (US)",
        "description": "Giọng nam Mỹ đĩnh đạc, ấm áp, chuẩn phim tài liệu và podcast",
        "sampleText": "Every night at precisely 3:15 AM, the transmission repeated the exact same pattern.",
        "categories": ["Kokoro 82M", "US English", "Nam (Male)"],
        "source": "Kokoro-82M",
        "tone": "blue",
    },
    {
        "id": "am_michael",
        "name": "Michael (Kokoro)",
        "engine": "kokoro",
        "style": "tự nhiên, đối thoại",
        "locale": "US",
        "gender": "Nam",
        "language": "English (US)",
        "description": "Giọng nam Mỹ đời thường, gần gũi và chân thật",
        "sampleText": "I never thought technology would get this good, but hearing this voice changes everything.",
        "categories": ["Kokoro 82M", "US English", "Nam (Male)"],
        "source": "Kokoro-82M",
        "tone": "blue",
    },
    {
        "id": "am_fenrir",
        "name": "Fenrir (Kokoro)",
        "engine": "kokoro",
        "style": "điện ảnh, kịch tính",
        "locale": "US",
        "gender": "Nam",
        "language": "English (US)",
        "description": "Giọng nam Mỹ trầm nội lực, hợp trailer phim và cốt truyện ly kỳ",
        "sampleText": "In the shadow of the mountains, an ancient secret was waiting to be unlocked.",
        "categories": ["Kokoro 82M", "US English", "Nam (Male)"],
        "source": "Kokoro-82M",
        "tone": "coral",
    },
    {
        "id": "bf_emma",
        "name": "Emma (Kokoro)",
        "engine": "kokoro",
        "style": "quý phái, chuẩn London",
        "locale": "UK",
        "gender": "Nữ",
        "language": "English (UK)",
        "description": "Giọng nữ Anh sang trọng, phát âm chuẩn Received Pronunciation",
        "sampleText": "Good evening. It is an absolute pleasure to welcome you to tonight's performance.",
        "categories": ["Kokoro 82M", "UK English", "Nữ (Female)"],
        "source": "Kokoro-82M",
        "tone": "violet",
    },
    {
        "id": "bm_george",
        "name": "George (Kokoro)",
        "engine": "kokoro",
        "style": "BBC, học thuật, uyên bác",
        "locale": "UK",
        "gender": "Nam",
        "language": "English (UK)",
        "description": "Giọng nam Anh trưởng thành, chuẩn đài phát thanh BBC",
        "sampleText": "History reminds us that true progress often arrives not with a shout, but with a whisper.",
        "categories": ["Kokoro 82M", "UK English", "Nam (Male)"],
        "source": "Kokoro-82M",
        "tone": "green",
    },
    {
        "id": "bm_lewis",
        "name": "Lewis (Kokoro)",
        "engine": "kokoro",
        "style": "thân thiện, ấm áp",
        "locale": "UK",
        "gender": "Nam",
        "language": "English (UK)",
        "description": "Giọng nam Anh trẻ trung, nhịp điệu tự nhiên và cuốn hút",
        "sampleText": "Have you ever wondered what lies beyond the edges of the known universe?",
        "categories": ["Kokoro 82M", "UK English", "Nam (Male)"],
        "source": "Kokoro-82M",
        "tone": "blue",
    },
]

KOKORO_VOICE_MAP = {v["id"]: v for v in KOKORO_VOICES}


def get_device() -> str:
    global _DEVICE
    if _DEVICE is None:
        _DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    return _DEVICE


def get_pipeline(lang_code: str = "a"):
    """
    Lazy load singleton KPipeline per language code:
    'a': American English (voices starting with 'a')
    'b': British English (voices starting with 'b')
    """
    global _PIPELINES
    if lang_code not in _PIPELINES:
        from kokoro import KPipeline

        device = get_device()
        logger.info(f"Khởi tạo KPipeline(lang_code='{lang_code}', device='{device}')")
        _PIPELINES[lang_code] = KPipeline(
            lang_code=lang_code,
            repo_id="hexgrad/Kokoro-82M",
            device=device,
        )
    return _PIPELINES[lang_code]


def is_kokoro_voice(voice_id: str) -> bool:
    if not voice_id:
        return False
    vid = voice_id.lower().strip()
    return vid in KOKORO_VOICE_MAP or vid.startswith(("af_", "am_", "bf_", "bm_"))


def resolve_kokoro_voice(voice_id: str) -> str:
    """Normalize user input or catalog id to standard Kokoro voice name."""
    vid = voice_id.lower().strip()
    if vid.startswith("kokoro-"):
        vid = vid.replace("kokoro-", "")
    if vid in KOKORO_VOICE_MAP:
        return vid
    # Default fallback
    if "emma" in vid:
        return "bf_emma"
    if "george" in vid:
        return "bm_george"
    if "adam" in vid:
        return "am_adam"
    if "bella" in vid:
        return "af_bella"
    return "af_heart"


def generate_kokoro(
    text: str,
    voice: str = "af_heart",
    speed: float = 1.0,
    callback=None,
) -> Tuple[np.ndarray, int]:
    """
    Synthesize text using Kokoro-82M model.
    Returns:
        (audio_np, sample_rate=24000)
    """
    voice_name = resolve_kokoro_voice(voice)
    # Check language code ('b' for British 'bf_' or 'bm_', else 'a' for American)
    lang_code = "b" if voice_name.startswith(("bf_", "bm_")) else "a"
    pipeline = get_pipeline(lang_code)

    t0 = time.time()
    chunks = []
    chunk_idx = 0
    with torch.inference_mode():
        generator = pipeline(text, voice=voice_name, speed=speed, split_pattern=r"\n+")
        for result in generator:
            if result is not None and getattr(result, "audio", None) is not None:
                audio_tensor = result.audio
                if isinstance(audio_tensor, torch.Tensor):
                    audio_np = audio_tensor.detach().cpu().numpy()
                else:
                    audio_np = np.asarray(audio_tensor)
                if audio_np.ndim > 1:
                    audio_np = audio_np.squeeze()
                chunks.append(audio_np)
                chunk_idx += 1
                if callback:
                    callback(chunk_idx, getattr(result, "graphemes", ""))

    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    if not chunks:
        # Fallback 0.5s silence
        full_audio = np.zeros(12000, dtype=np.float32)
    else:
        full_audio = np.concatenate(chunks).astype(np.float32)

    logger.info(
        f"Kokoro synth done: voice={voice_name}, length={len(full_audio)/24000:.2f}s in {time.time()-t0:.2f}s"
    )
    return full_audio, 24000
