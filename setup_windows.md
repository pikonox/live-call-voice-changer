# Windows Setup - Live Call ke liye

1. Python install karo (python.org se, install ke waqt "Add Python to PATH" tick karo)
2. Is folder me terminal kholo aur run karo:
   ```
   pip install -r requirements.txt
   python app.py
   ```
3. VB-Cable install karo (free, vb-audio.com se VB-Cable download karo)
   - Install ke baad PC restart karo
   - Windows Sound Settings > Input me "CABLE Output" dikhega, Output me "CABLE Input"
4. App me "Devices Dikhao" dabao, CABLE nazar aana chahiye
5. App me preset chuno, "Live Mode START" dabao
6. Windows Sound Settings > Input (Microphone) ko "CABLE Output" par set karo
   - WhatsApp Desktop ki apni mic setting nahi hoti, wo Windows default hi use karta hai
7. Headphones lagao, WhatsApp Desktop app (Web nahi) se test call karo
8. Call khatam ho to App me "Live Mode STOP" dabao aur Windows mic wapas apne asli mic par kar do

Troubleshooting:
- Awaz change nahi ho rahi? Pehle check karo App Live ON hai ya nahi, aur Windows Input CABLE par hai ya nahi
- Echo aa raha hai? Speaker band karo, headphones use karo
- Awaz robotic lag rahi hai? Preset Natural Girl try karo, mic kareeb rakho, quiet room me betho
