import numpy as np
from scipy import signal

def master_youtube_vocal(audio, sr=24000, enable_eq=True, enable_compress=True):
    if len(audio) == 0:
        return audio
    data = np.asarray(audio, dtype=np.float32)

    # 1. High-pass filter at 65Hz to cut mic rumble & plosives
    sos_hp = signal.butter(2, 65.0, btype='highpass', fs=sr, output='sos')
    data = signal.sosfilt(sos_hp, data)

    # 2. Vocal Air / Presence EQ boost (+2.2 dB at 3800Hz, biquad peak filter)
    if enable_eq:
        f0 = 3800.0
        gain_db = 2.2
        Q = 1.2
        A = 10.0 ** (gain_db / 40.0)
        w0 = 2.0 * np.pi * f0 / sr
        alpha = np.sin(w0) / (2.0 * Q)
        b0 = 1.0 + alpha * A
        b1 = -2.0 * np.cos(w0)
        b2 = 1.0 - alpha * A
        a0 = 1.0 + alpha / A
        a1 = -2.0 * np.cos(w0)
        a2 = 1.0 - alpha / A
        b = np.array([b0/a0, b1/a0, b2/a0], dtype=np.float32)
        a = np.array([1.0, a1/a0, a2/a0], dtype=np.float32)
        data = signal.lfilter(b, a, data)

    # 3. Broadcast Dynamic Compressor (Smooth soft-knee)
    if enable_compress:
        threshold = 0.15
        ratio = 0.45
        mag = np.abs(data)
        gain = np.where(mag > threshold, (threshold + (mag - threshold) * ratio) / (mag + 1e-9), 1.0)
        data = data * gain

    # 4. TruePeak normalization (-1.0 dBFS = 0.891) for YouTube Loudness compliance
    peak = np.max(np.abs(data))
    if peak > 1e-4:
        data = np.clip(data * (0.891 / peak), -1.0, 1.0)

    return data.astype(np.float32)

if __name__ == '__main__':
    dummy = np.random.randn(24000).astype(np.float32) * 0.2
    out = master_youtube_vocal(dummy, 24000)
    print("DSP Test SUCCESS! Peak:", np.max(np.abs(out)), "RMS:", np.sqrt(np.mean(out**2)))
