"""
Voice Changer App - Windows + Mac
Run:  python app.py

What it does:
1) VOICE NOTE MODE (works right away, no virtual cable needed):
   - Record from mic OR choose a .wav file
   - Convert to girl preset
   - Save as *_girl.wav -> send it on WhatsApp Desktop by drag & drop

2) LIVE CALL MODE (needs virtual cable, see setup_windows.md / setup_mac.md):
   - Mic -> App (pitch shift) -> Virtual Cable / BlackHole
   - In Windows Sound Settings, set WhatsApp input = Virtual Cable
   - On Mac, set WhatsApp input = BlackHole
   - WhatsApp Desktop does NOT have its own mic picker, it uses system default.
   - Use headphones to avoid echo.

If sounddevice is not installed, live/record buttons will show the install command.
"""
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from audio_engine import PRESETS, convert_file, list_devices

APP_DIR = os.path.dirname(os.path.abspath(__file__))

class App:
    def __init__(self, root):
        self.root = root
        root.title("Voice Changer - Windows + Mac v1")
        root.geometry("560x520")
        self.preset = tk.StringVar(value="natural_girl")
        self.status = tk.StringVar(value="Ready. Pehle Voice Note mode try karo, phir Live mode.")
        self.live_running = False
        self.stream = None

        tk.Label(root, text="Voice Changer v1", font=("Arial", 18, "bold")).pack(pady=10)
        tk.Label(root, text="Voice Note + Live Call (WhatsApp Desktop ke liye)", font=("Arial", 11)).pack()

        frame = tk.LabelFrame(root, text="Voice Preset", padx=10, pady=10)
        frame.pack(fill="x", padx=15, pady=12)
        for key, p in PRESETS.items():
            tk.Radiobutton(frame, text=f"{p['label']}  ({p['n_steps']} steps up)", variable=self.preset, value=key).pack(anchor="w")

        btns = tk.Frame(root)
        btns.pack(pady=8)
        tk.Button(btns, text="1. File Convert Karo (.wav)", command=self.convert_file_ui, width=32).pack(pady=4)
        tk.Button(btns, text="2. Record + Convert (10 sec)", command=self.record_convert, width=32).pack(pady=4)
        tk.Button(btns, text="3. Live Mode START", command=self.start_live, width=32, bg="#d4edda").pack(pady=4)
        tk.Button(btns, text="Live Mode STOP", command=self.stop_live, width=32, bg="#f8d7da").pack(pady=4)
        tk.Button(btns, text="Devices Dikhao", command=self.show_devices, width=32).pack(pady=4)

        tk.Label(root, textvariable=self.status, wraplength=500, justify="left").pack(padx=15, pady=12)
        tk.Label(root, text="Live mode ke liye pehle setup_windows.md ya setup_mac.md parho.\nVirtual cable ke baghair live awaz WhatsApp tak nahi jayegi.",
                 wraplength=500, justify="left", fg="gray").pack(padx=15)

    def convert_file_ui(self):
        path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if not path:
            return
        out = path.replace(".wav", "_girl.wav")
        try:
            convert_file(path, out, self.preset.get())
            self.status.set(f"Ho gaya! Saved: {out}\nIs file ko WhatsApp Desktop me drag kar ke bhej do.")
            messagebox.showinfo("Done", f"Saved:\n{out}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def record_convert(self):
        def run():
            try:
                import sounddevice as sd
                from scipy.io import wavfile
                import numpy as np
                self.status.set("Recording... 10 sec bolo, mic ke kareeb.")
                sr = 44100
                rec = sd.rec(int(10 * sr), samplerate=sr, channels=1)
                sd.wait()
                raw = os.path.join(APP_DIR, "my_voice.wav")
                wavfile.write(raw, sr, (rec * 32767).astype(np.int16))
                out = os.path.join(APP_DIR, "my_voice_girl.wav")
                convert_file(raw, out, self.preset.get())
                self.status.set(f"Ho gaya! Saved: {out}")
            except Exception as e:
                self.status.set(f"Record nahi hua. Install karo: pip install sounddevice soundfile\nError: {e}")
        threading.Thread(target=run, daemon=True).start()

    def show_devices(self):
        inputs, outputs = list_devices()
        if not inputs and not outputs:
            messagebox.showinfo("Devices", "sounddevice install nahi hai.\nRun: pip install sounddevice")
            return
        msg = "INPUT (Mic):\n" + "\n".join(f"{i}: {n}" for i, n in inputs)
        msg += "\n\nOUTPUT:\n" + "\n".join(f"{i}: {n}" for i, n in outputs)
        msg += "\n\nLive ke liye OUTPUT me VB-Cable ya BlackHole hona chahiye."
        messagebox.showinfo("Devices", msg)

    def start_live(self):
        if self.live_running:
            return
        try:
            import sounddevice as sd
            import numpy as np
            from audio_engine import pitch_shift
        except Exception as e:
            messagebox.showerror("Missing", f"Live ke liye install karo:\npip install sounddevice\nError: {e}")
            return
        inputs, outputs = list_devices()
        # Pick virtual output if present, else default output
        out_idx = None
        for i, name in outputs:
            if "CABLE" in name.upper() or "BLACKHOLE" in name.upper() or "VOICEMEETER" in name.upper():
                out_idx = i
                break
        if out_idx is None:
            messagebox.showwarning("Virtual Cable nahi mila",
                "VB-Cable (Windows) ya BlackHole (Mac) install karo, phir dobara try karo.\nSetup file parho: setup_windows.md / setup_mac.md")
            return
        preset = PRESETS[self.preset.get()]
        n_steps = preset["n_steps"]
        sr = 44100
        def callback(indata, outdata, frames, time, status):
            try:
                mono = indata[:, 0].astype(np.float32)
                shifted = pitch_shift(mono, sr, n_steps)
                outdata[:, 0] = shifted[:frames] if len(shifted) >= frames else np.pad(shifted, (0, frames - len(shifted)))
                if outdata.shape[1] > 1:
                    outdata[:, 1] = outdata[:, 0]
            except Exception:
                outdata[:] = indata[:outdata.shape[0]] if indata.shape[0] >= outdata.shape[0] else 0
        try:
            self.stream = sd.Stream(samplerate=sr, channels=1, callback=callback, dtype="float32")
            # Note: sounddevice Stream defaults to system in/out. For virtual routing,
            # set Windows/Mac default output to the virtual device in system settings,
            # or edit device= below to out_idx. We use explicit output device here:
            self.stream.close()
            self.stream = sd.Stream(device=(None, out_idx), samplerate=sr, channels=1, callback=callback, dtype="float32")
            self.stream.start()
            self.live_running = True
            self.status.set(f"Live ON hai! Output device: {dict(outputs)[out_idx]}\nAb WhatsApp Desktop me call karo. Headphones use karo.")
        except Exception as e:
            messagebox.showerror("Live Error", str(e))

    def stop_live(self):
        try:
            if self.stream:
                self.stream.stop()
                self.stream.close()
        except Exception:
            pass
        self.live_running = False
        self.stream = None
        self.status.set("Live OFF ho gaya.")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
