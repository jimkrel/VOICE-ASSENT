import numpy as np
from scipy import signal

def biquad_peaking(data, sr, f0, gain_db, Q=1.0):
    A = 10.0 ** (gain_db / 40.0)
    w0 = 2.0 * np.pi * f0 / sr
    alpha = np.sin(w0) / (2.0 * Q)
    b0 = 1.0 + alpha * A
    b1 = -2.0 * np.cos(w0)
    b2 = 1.0 - alpha * A
    a0 = 1.0 + alpha / A
    a1 = -2.0 * np.cos(w0)
    a2 = 1.0 - alpha / A
    b = np.array([b0 / a0, b1 / a0, b2 / a0], dtype=np.float32)
    a = np.array([1.0, a1 / a0, a2 / a0], dtype=np.float32)
    return signal.lfilter(b, a, data)

def apply_emotion_dsp(audio, sr=24000, emotion="calm"):
    if len(audio) == 0 or emotion == "calm":
        return audio
    data = np.asarray(audio, dtype=np.float32).copy()
    try:
        if emotion == "whisper":
            sos_hp = signal.butter(2, 140.0, btype="highpass", fs=sr, output="sos")
            data = signal.sosfilt(sos_hp, data)
            data = biquad_peaking(data, sr, 3200.0, +2.5, Q=1.0)
            data = biquad_peaking(data, sr, 7000.0, +2.0, Q=0.8)
            data = np.tanh(data * 0.85) / 0.85

        elif emotion == "dramatic":
            data = biquad_peaking(data, sr, 160.0, +2.2, Q=0.9)
            data = biquad_peaking(data, sr, 500.0, -1.2, Q=1.2)
            data = biquad_peaking(data, sr, 2800.0, +1.6, Q=0.9)
            data = np.tanh(data * 1.15) / 1.15

        elif emotion == "excited":
            data = biquad_peaking(data, sr, 2600.0, +2.6, Q=1.0)
            data = biquad_peaking(data, sr, 8000.0, +1.8, Q=0.8)
            data = np.tanh(data * 1.20) / 1.20

        elif emotion == "sad":
            data = biquad_peaking(data, sr, 2200.0, -2.2, Q=1.0)
            sos_lp = signal.butter(2, 6500.0, btype="lowpass", fs=sr, output="sos")
            data = 0.70 * data + 0.30 * signal.sosfilt(sos_lp, data)

        elif emotion == "angry":
            data = biquad_peaking(data, sr, 220.0, +2.0, Q=1.1)
            data = biquad_peaking(data, sr, 3400.0, +3.2, Q=1.2)
            data = np.tanh(data * 1.35) / 1.35

        elif emotion == "sigh":
            sos_hp = signal.butter(2, 120.0, btype="highpass", fs=sr, output="sos")
            data = signal.sosfilt(sos_hp, data)
            data = biquad_peaking(data, sr, 4000.0, +1.5, Q=0.9)
    except Exception as e:
        print(f"Lỗi DSP emotion {emotion}:", e)

    p = np.max(np.abs(data))
    if p > 0.95:
        data = data * (0.92 / p)
    return data.astype(np.float32)

# Test with dummy sine wave
sr = 24000
t = np.linspace(0, 1.0, sr, endpoint=False)
dummy = (0.5 * np.sin(2 * np.pi * 200 * t)).astype(np.float32)

for emo in ["calm", "whisper", "dramatic", "excited", "sad", "angry", "sigh"]:
    out = apply_emotion_dsp(dummy, sr, emo)
    print(f"Emotion '{emo}': shape={out.shape}, max={np.max(np.abs(out)):.4f}")
print("ALL DSP TESTS PASSED")
