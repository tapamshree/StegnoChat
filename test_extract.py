from pywinauto import Application
import win32gui

hwnds = []
def callback(h, hwnds):
    if win32gui.IsWindowVisible(h) and "WhatsApp" in win32gui.GetWindowText(h):
        hwnds.append(h)
    return True
win32gui.EnumWindows(callback, hwnds)

with open("text_dump_all.txt", "w", encoding="utf-8") as f:
    for h in hwnds:
        try:
            f.write(f"--- WINDOW HWND: {h} TITLE: {win32gui.GetWindowText(h)} ---\n")
            app = Application(backend="uia").connect(handle=h, timeout=2)
            win = app.window(handle=h)
            
            # Use descendants without control_type to get EVERYTHING
            elements = win.descendants()
            for e in elements:
                try:
                    text = e.window_text()
                    name = getattr(e.element_info, "name", "")
                    if text or name:
                        if "\U0001f44b" in text or "\U0001f44b" in name or "You:" in text or "You:" in name:
                            f.write(f"MATCH: {e.element_info.control_type} | TEXT: {repr(text)} | NAME: {repr(name)} | RECT: {e.rectangle()}\n")
                except Exception as ex:
                    pass
        except Exception as ex:
            f.write(f"Error on HWND {h}: {ex}\n")
