import keyboard
import pyperclip
import stego
import config
import msg_cache
import win32gui
import time
from wa_watcher import trigger_scan

_hooked = False

def is_whatsapp_focused():
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        title = win32gui.GetWindowText(hwnd)
        return "WhatsApp" in title
    return False

def on_enter():
    if not config.session.unlocked or not is_whatsapp_focused():
        keyboard.send('enter')
        return

    try:
        old_clipboard = pyperclip.paste()
    except Exception:
        old_clipboard = ""

    keyboard.send('ctrl+a')
    time.sleep(0.05)
    keyboard.send('ctrl+x')
    time.sleep(0.05)
    
    try:
        text = pyperclip.paste()
    except Exception:
        text = ""
        
    if not text.strip():
        keyboard.send('enter')
        return

    cover = config.get_cover_text()
    encoded = stego.encode(text, cover=cover)
    
    # Cache the plaintext so overlays can display it
    msg_cache.add_message(text, cover)
    
    pyperclip.copy(encoded)
    time.sleep(0.05)
    keyboard.send('ctrl+v')
    time.sleep(0.05)
    
    keyboard.send('enter')
    
    trigger_scan()
    
    time.sleep(0.05)
    try:
        pyperclip.copy(old_clipboard)
    except Exception:
        pass

def update_hook_state(unlocked):
    global _hooked
    if unlocked and not _hooked:
        keyboard.add_hotkey('enter', on_enter, suppress=True)
        _hooked = True
    elif not unlocked and _hooked:
        keyboard.remove_hotkey('enter')
        _hooked = False
