# Voice Changer v1 - Windows + Mac

Apna khud ka voice changer, Voicemod ke baghair.

## Kya karta hai?
- **Voice Note mode:** Apni awaz record karo ya .wav file do, girl preset me convert karo, phir WhatsApp Desktop me bhej do. Ye mode foran kaam karta hai, kisi virtual cable ki zaroorat nahi.
- **Live Call mode:** Mic -> App -> Virtual Cable -> WhatsApp Desktop. Windows par VB-Cable, Mac par BlackHole chahiye. Detail ke liye setup_windows.md aur setup_mac.md parho.

## Run kaise karein?
Windows:
```
pip install -r requirements.txt
python app.py
```
Mac:
```
pip3 install -r requirements.txt
python3 app.py
```

## Presets
- Natural Girl (4 steps up) - sab se pehle ye try karo
- Soft Girl (5 steps up)
- Energetic Girl (6 steps up)

## Sachhi limit (important)
Ye v1 pitch-shift technology hai, AI cloning nahi. Is liye:
- Voice note me awaz achhi aur usable hogi
- Live call me thori latency aur thora robotic feel aa sakta hai, ye normal hai is technology me
- Fully natural AI voice ke liye RVC model + GPU chahiye hota hai, wo is v1 me nahi hai
- Apni awaz, mic quality aur quiet room se result bohat behtar hota hai

## Files
- app.py - GUI app
- audio_engine.py - pitch shift engine
- setup_windows.md - Windows live setup
- setup_mac.md - Mac live setup
- run_windows.bat / run_mac.sh - one-click run
