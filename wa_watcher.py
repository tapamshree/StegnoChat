from pywinauto import Application
import win32gui
import time
import threading
import logging
import msg_cache
import config

logging.basicConfig(filename='watcher_debug.log', level=logging.DEBUG, format='%(asctime)s - %(message)s')

force_scan_event = threading.Event()

def trigger_scan():
    force_scan_event.set()

def is_whatsapp_focused():
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        title = win32gui.GetWindowText(hwnd)
        return "WhatsApp" in title
    return False

def watch_loop(on_sync, stop_event):
    logging.debug("Started watch_loop")
    while not stop_event.is_set():
        forced = force_scan_event.is_set()
        if forced:
            force_scan_event.clear()
            
        if not forced and not is_whatsapp_focused():
            force_scan_event.wait(timeout=1.5)
            continue
        
        if not config.session.unlocked:
            # Not in secure mode, send empty list to clear overlays
            on_sync([])
            force_scan_event.wait(timeout=2.0)
            continue

        logging.debug("Starting scan. forced=%s", forced)
        found_items = []
        
        # Get cached messages to match against UI
        cached = msg_cache.get_messages()
        if not cached:
            logging.debug("No cached messages, skipping scan")
            on_sync([])
            force_scan_event.wait(timeout=2.0)
            continue
        
        # Build a lookup: cover_text -> list of plaintext messages
        cover_lookup = {}
        for entry in cached:
            cover = entry["cover"]
            if cover not in cover_lookup:
                cover_lookup[cover] = []
            cover_lookup[cover].append(entry["plain"])
        
        try:
            hwnds = []
            def callback(h, hwnds):
                if win32gui.IsWindowVisible(h) and "WhatsApp" in win32gui.GetWindowText(h):
                    hwnds.append(h)
                return True
            win32gui.EnumWindows(callback, hwnds)
            
            if hwnds:
                app = Application(backend="uia").connect(handle=hwnds[0], timeout=1)
                bubbles = app.window(handle=hwnds[0]).descendants(control_type="Text")
                logging.debug("Found %d text elements in WhatsApp", len(bubbles))
                
                for i, b in enumerate(bubbles):
                    try:
                        text = b.window_text()
                        if not text:
                            continue
                        
                        # Check if this text matches any cover text
                        text_stripped = text.strip()
                        if text_stripped in cover_lookup:
                            plaintexts = cover_lookup[text_stripped]
                            # Use the most recent plaintext for this cover
                            plain = plaintexts[-1]
                            logging.debug("Bubble %d matched cover '%s' -> '%s'", i, text_stripped, plain)
                            found_items.append({
                                "rect": b.rectangle(),
                                "text": plain
                            })
                    except Exception as ex:
                        logging.debug("Bubble %d error: %s", i, ex)
        except Exception as e:
            logging.error("Scan error: %s", e)
            
        logging.debug("Scan finished. Found %d items.", len(found_items))
        on_sync(found_items)
        
        # Sleep for 2s unless interrupted by a force scan
        force_scan_event.wait(timeout=2.0)
