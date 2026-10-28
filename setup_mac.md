# Mac Setup - Live Call ke liye

1. Python install karo (python.org se, ya brew: brew install python)
2. Is folder me Terminal kholo aur run karo:
   ```
   pip3 install -r requirements.txt
   python3 app.py
   ```
3. BlackHole install karo (free, existential.audio/BlackHole - 2ch version)
   - Install ke baad Mac restart karna par sakta hai
   - System Settings > Sound me BlackHole dikhega
4. App me "Devices Dikhao" dabao, BlackHole nazar aana chahiye
5. App me preset chuno, "Live Mode START" dabao
6. Mac System Settings > Sound > Input ko "BlackHole 2ch" par set karo
   - WhatsApp Desktop Mac app system default mic use karta hai
   - Apni awaz sunne ke liye headphones use karo, warna tumhe apni awaz nahi sunai degi
7. WhatsApp Desktop app se test call karo
8. Call khatam ho to App me "Live Mode STOP" dabao aur Mac Input wapas apne asli mic par kar do

Troubleshooting:
- BlackHole nahi dikh raha? BlackHole install ke baad Audio MIDI Setup kholo, wahan check karo
- Awaz nahi ja rahi? App Live ON hai? Mac Input BlackHole par hai?
- Mac par permission: System Settings > Privacy > Microphone me Terminal / Python ko allow karo
