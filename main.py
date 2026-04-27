import sys
sys.coinit_flags = 2
import threading
import os
from PyQt6.QtWidgets import QApplication
from ui.overlay import OverlayWindow
from ui.tray_icon import TrayIcon
from ui.chat_view import ChatOverlay
from wa_watcher import watch_loop
import config

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    overlay = OverlayWindow()
    overlay.show()
    
    tray = TrayIcon(overlay, app)
    tray.setup()
    tray.run()
    
    active_overlays = []
    
    def sync_overlays_threadsafe(items):
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(0, lambda: perform_sync(items))

    import logging
    logging.basicConfig(filename='watcher_debug.log', level=logging.DEBUG, format='%(asctime)s - %(message)s')

    def perform_sync(items):
        nonlocal active_overlays
        logging.debug("perform_sync received %d items. unlocked=%s", len(items), config.session.unlocked)
        
        if not config.session.unlocked:
            for o in active_overlays:
                o.close()
            active_overlays.clear()
            return
            
        new_overlays = []
        for item in items:
            rect = item["rect"]
            text = item["text"]
            
            matched = None
            for o in active_overlays:
                if o.label.text() == text:
                    if abs(o.geometry().y() - rect.top) < 300:
                        matched = o
                        break
            
            if matched:
                active_overlays.remove(matched)
                matched.update_rect(rect)
                new_overlays.append(matched)
            else:
                o = ChatOverlay(rect, text)
                o.show()
                new_overlays.append(o)
                
        for o in active_overlays:
            o.close()
            
        active_overlays = new_overlays

    stop_event = threading.Event()
    watcher_thread = threading.Thread(target=watch_loop, args=(sync_overlays_threadsafe, stop_event), daemon=True)
    watcher_thread.start()
    
    try:
        app.exec()
    finally:
        stop_event.set()
        os._exit(0)

if __name__ == "__main__":
    main()
