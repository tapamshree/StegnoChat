from pywinauto import Application
import win32gui

print("Finding WhatsApp windows...")
hwnds = []
def callback(h, hwnds):
    if win32gui.IsWindowVisible(h) and "WhatsApp" in win32gui.GetWindowText(h):
        hwnds.append(h)
    return True
win32gui.EnumWindows(callback, hwnds)

for h in hwnds:
    print(f"Found window: {win32gui.GetWindowText(h)} (HWND: {h})")

if hwnds:
    print("Attempting to read text elements from the first window...")
    try:
        app = Application(backend="uia").connect(handle=hwnds[0], timeout=5)
        bubbles = app.window(handle=hwnds[0]).descendants(control_type="Text")
        print(f"Found {len(bubbles)} text elements.")
        for b in bubbles[:10]: # Print first 10
            print(repr(b.window_text()))
    except Exception as e:
        print(f"Error: {e}")
else:
    print("No WhatsApp window found.")
