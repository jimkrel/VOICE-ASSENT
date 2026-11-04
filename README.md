# VOICE-ASSENT

Studio Voice Production & Real-time AI Voice Synthesizer with OmniVoice FP16, Next.js & FastAPI.

## Overview

**VOICE-ASSENT** is a professional voice-production studio web application designed for high-fidelity speech synthesis, voice cloning, and real-time voice changing.

### Key Features
- **High-Fidelity Text-to-Speech (TTS):** 24 kHz studio-grade audio synthesis powered by OmniVoice FP16 with 5-stage mastering (-14 LUFS standard, 5-band EQ matching, tube warmth, and de-esser).
- **Voice Library (Kho giọng đọc):** 23+ built-in studio voices (Vietnamese Northern/Southern accents & ElevenLabs Originals) with instant sample playback.
- **Voice Cloning (Tạo giọng mới):** Rapid zero-shot voice cloning with live waveform preview, hardware telemetry, and progress stages.
- **Voice Changer (Đổi giọng):** Speech-to-speech voice conversion with emotional tone conditioning.
- **Real-Time Hardware Telemetry:** Live GPU %, GPU Temp (°C), VRAM usage, CPU %, and RAM monitoring directly in the studio header.
- **Clean Audio History Management:** Instant playback, download, single-item deletion, and one-click history purge.

---

## Architecture

- **Backend:** FastAPI (`api_server.py`) with CUDA PyTorch (`studio_app.py`), librosa, soundfile, and psutil telemetry.
- **Frontend:** Next.js 16 (`ui_v2`) with React 19, Tailwind CSS, Lucide icons, and Radix UI / Shadcn UI components.
- **Presets & Data:** `presets/` containing studio acoustic reference files and `elevenlabs_catalog.json`.

---

## Quick Start

### 1. Requirements
- Windows 10/11 or Linux
- Python 3.10+ with CUDA support (e.g., NVIDIA GTX 1650 or higher)
- Node.js 18+ and pnpm

### 2. Backend Setup
```bash
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn torch torchaudio soundfile librosa psutil scipy

# Start FastAPI server
python api_server.py
```

### 3. Frontend Setup
```bash
cd ui_v2
pnpm install
pnpm build
pnpm start -p 7860 -H 0.0.0.0
```

Access the studio at: `http://localhost:7860`
API endpoints & telemetry at: `http://localhost:8000`

---

## License
MIT License
