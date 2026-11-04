@echo off
title OmniVoice Studio Pro (Next.js Studio UI + GPU Backend)
cd /d E:\VoiceAI
set HF_HOME=E:\VoiceAI\hf_cache
set TORCH_HOME=E:\VoiceAI\torch_cache
set TEMP=E:\VoiceAI\temp
set TMP=E:\VoiceAI\temp

echo ========================================================
echo   Thanh Am - OmniVoice Studio Pro (GTX 1650 CUDA FP16)
echo   Local PC:   http://127.0.0.1:7860
echo   Dien thoai: http://192.168.1.8:7860
echo ========================================================

:: 1. Launch FastAPI Backend in background on port 8000
start "FastAPI GPU Backend" /min "E:\VoiceAI\venv\Scripts\python.exe" api_server.py

:: 2. Wait 2 seconds for backend to initialize
timeout /t 2 /nobreak >nul

:: 3. Launch default browser
start http://127.0.0.1:7860

:: 4. Start Next.js production server on port 7860
cd /d E:\VoiceAI\ui_v2
pnpm start -p 7860 -H 0.0.0.0
pause
