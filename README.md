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
- **Pakistani Female (Urdu accent) (4 steps up) - DEFAULT, sab se pehle ye try karo**
- Natural Girl (4 steps up)
- Soft Girl (5 steps up)
- Energetic Girl (6 steps up)

## Pakistani female accent kaise milega? (important)
Ye app tumhari awaz ko clone nahi karta, sirf pitch badalta hai. Is ka faida ye hai:
- Tum jo accent bologe, wohi accent output me rahega
- Agar tum Urdu me Pakistani lehje me bologe, to output bhi Pakistani female accent me sunai dega
- Voicemod jaisi Western presets ki tarah American/British accent nahi aayega, kyunki wo AI voice tumhari jagah nahi le rahi

Pakistani accent ke liye ye 3 baatein lazmi hain:
1. **Urdu me bolo**, English me bolne se accent automatically Western jaisa lagne lagta hai
2. **Pitch zyada upar mat karo** - Pakistani Female preset isi liye 4 steps par rakha hai, zyada pitch se awaz cartoon aur foreign lagti hai
3. **Normal speed aur natural lehja rakho** - sales call me aahista, saaf aur polite Urdu sab se zyada trust banati hai

Agar tum chaho ke koi aur tumhare liye bole, to us Pakistani female speaker ki awaz record kar ke usi ko convert karo, tab accent 100% original rahega.

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
