import numpy as np
import librosa

y, sr = librosa.load("audio.wav", sr=None, mono=True)

rms = np.sqrt(np.mean(y**2))

peak = np.max(np.abs(y))

crest_factor = peak / rms
crest_factor_db = 20 * np.log10(crest_factor)

print("RMS:", rms)
print("Crest factor:", crest_factor_db, "dB")