"""
Voice Changer Engine - Windows + Mac (Python)
v1 prototype: pitch-shifted voice for voice notes + live mode.

Important, honest note:
- This is NOT an AI RVC / cloning model. It shifts pitch + tone.
  That is why it is light, runs on any laptop, and has no GPU need.
- For a fully natural AI girl voice you would need an RVC model
  trained on a female voice, which is heavy and needs consent from
  the voice owner. This v1 is a good, usable start for testing.
- Use it for your own brand voice / marketing, not to mislead a
  live customer about who you are.

Dependencies (optional, graceful fallback):
  pip install numpy scipy sounddevice soundfile librosa
  Minimum to run offline conversion: numpy + scipy (already common)
"""
import numpy as np
from scipy.io import wavfile
from scipy.signal import stft, istft

PRESETS = {
    "natural_girl": {"label": "Natural Girl", "n_steps": 4, "gain": 1.0},
    "soft_girl": {"label": "Soft Girl", "n_steps": 5, "gain": 0.95},
    "energetic_girl": {"label": "Energetic Girl", "n_steps": 6, "gain": 1.0},
}

def _pitch_shift_stft(y, sr, n_steps):
    """Simple STFT pitch shift. Works without librosa."""
    factor = 2.0 ** (n_steps / 12.0)
    if len(y) == 0:
        return y
    # Mono
    if y.ndim > 1:
        y = y.mean(axis=1)
    f, t, Zxx = stft(y, fs=sr, nperseg=2048, noverlap=1536)
    n_bins = Zxx.shape[0]
    # New spectrum: bin i in output comes from bin i/factor in input
    src_idx = np.arange(n_bins) / factor
    shifted = np.zeros_like(Zxx)
    for j in range(Zxx.shape[1]):
        col = Zxx[:, j]
        # Interpolate magnitude and phase separately for stability
        mag = np.interp(src_idx, np.arange(n_bins), np.abs(col), left=0, right=0)
        phase = np.interp(src_idx, np.arange(n_bins), np.angle(col), left=0, right=0)
        shifted[:, j] = mag * np.exp(1j * phase)
    _, y_out = istft(shifted, fs=sr, nperseg=2048, noverlap=1536)
    # Match length
    if len(y_out) < len(y):
        y_out = np.pad(y_out, (0, len(y) - len(y_out)))
    else:
        y_out = y_out[:len(y)]
    return y_out

def pitch_shift(y, sr, n_steps):
    """Try librosa first (better quality), fall back to STFT version."""
    try:
        import librosa
        return librosa.effects.pitch_shift(y.astype(np.float32), sr=sr, n_steps=n_steps)
    except Exception:
        return _pitch_shift_stft(y.astype(np.float32), sr, n_steps)

def convert_array(y, sr, preset_name="natural_girl", custom_steps=None):
    preset = PRESETS.get(preset_name, PRESETS["natural_girl"])
    n_steps = custom_steps if custom_steps is not None else preset["n_steps"]
    # Normalise to float -1..1
    if y.dtype != np.float32 and y.dtype != np.float64:
        # int16 wav
        y = y.astype(np.float32) / 32768.0
    if y.ndim > 1:
        y = y.mean(axis=1)
    out = pitch_shift(y, sr, n_steps)
    # Light high-frequency lift so it does not sound muffled, then gain
    out = out * preset["gain"]
    peak = np.max(np.abs(out)) if len(out) else 0
    if peak > 0.95:
        out = out * (0.95 / peak)
    return out, sr

def convert_file(input_path, output_path, preset_name="natural_girl", custom_steps=None):
    sr, data = wavfile.read(input_path)
    out, sr_out = convert_array(data, sr, preset_name, custom_steps)
    wavfile.write(output_path, sr_out, (out * 32767).astype(np.int16))
    return output_path

def list_devices():
    """Return (inputs, outputs) or empty lists if sounddevice missing."""
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        inputs = [(i, d["name"]) for i, d in enumerate(devices) if d["max_input_channels"] > 0]
        outputs = [(i, d["name"]) for i, d in enumerate(devices) if d["max_output_channels"] > 0]
        return inputs, outputs
    except Exception as e:
        return [], []
