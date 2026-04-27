import sys
from pywinauto import Application
import win32gui
import io

hwnds = []
def callback(h, hwnds):
    if win32gui.IsWindowVisible(h) and "WhatsApp" in win32gui.GetWindowText(h):
        hwnds.append(h)
    return True
win32gui.EnumWindows(callback, hwnds)

if not hwnds:
    print("WhatsApp not found!")
    sys.exit(1)

print(f"Found {len(hwnds)} WhatsApp windows.")
for h in hwnds:
    print(f"HWND: {h}, Title: {win32gui.GetWindowText(h)}")

try:
    app = Application(backend="uia").connect(handle=hwnds[0], timeout=5)
    window = app.window(handle=hwnds[0])
    
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    
    window.print_control_identifiers(depth=8)
    
    sys.stdout = old_stdout
    
    with open("dump.txt", "w", encoding="utf-8") as f:
        f.write(new_stdout.getvalue())
        
    print("Dumped tree to dump.txt")
except Exception as e:
    print(f"Error: {e}")
