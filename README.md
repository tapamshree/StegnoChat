# Stegnochat

Stegnochat is a secure desktop companion application that provides visual steganography for WhatsApp Desktop. It allows you to send hidden, encrypted messages embedded within seemingly normal text or emojis (like "👋"). 

When "Secure Mode" is activated, Stegnochat intercepts your outgoing messages, encodes them into zero-width characters, and sends them via WhatsApp. On the receiving end (or your own screen when Secure Mode is active), Stegnochat automatically decodes these hidden messages and displays them as a seamless green overlay directly on top of the WhatsApp interface.

## ✨ Features
* **Zero-Width Steganography**: Messages are encoded into invisible characters and attached to a cover text (e.g., an emoji). To anyone without the app, it just looks like you sent a normal emoji.
* **Secure Mode & PIN Gate**: Your decrypted messages are protected by a secure PIN. If Secure Mode is OFF, all overlays are hidden, and only the cover text is visible.
* **Local Message Cache**: Since WhatsApp strips zero-width characters in its accessibility APIs, Stegnochat caches your sent messages locally. This ensures you can seamlessly read the messages you've already sent when you switch Secure Mode back ON.
* **Floating UI Overlay**: Provides a clean, non-intrusive toolbar at the top of your WhatsApp window to easily toggle Secure Mode.
* **System Tray Integration**: Run the app in the background and control it directly from your Windows system tray.

## 🚀 How to Run

### Requirements
* Python 3.10+
* Windows OS (Relies on `pywinauto` and `win32gui` for window tracking)
* WhatsApp Desktop installed and running

### Setup
1. Clone this repository to your local machine.
2. Create and activate a virtual environment:
   ```cmd
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install the dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
4. Run the application:
   ```cmd
   python main.py
   ```

## 🛠️ Building the Executable
If you want to package Stegnochat into a standalone Windows executable (`.exe`), simply run the included build script:
```cmd
python build.py
```
The compiled executable will be located in the `dist` folder.

## 📝 Usage
1. Open WhatsApp Desktop.
2. Launch **Stegnochat**. You will see a toolbar overlay appear at the top of your WhatsApp window.
3. Click the toggle switch to turn **ON** Secure Mode. You will be prompted to set or enter your PIN.
4. Once unlocked, type any message in WhatsApp and press `Enter`. The app will automatically intercept your text, hide it inside an emoji, and send it. 
5. A green bubble overlay will instantly appear over the sent message, showing you the decrypted plaintext.
6. Turn **OFF** Secure Mode to hide all overlays and secure your local session.
