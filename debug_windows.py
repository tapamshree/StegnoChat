import win32gui

print("Listing all visible windows...")
hwnds = []
def callback(h, hwnds):
    if win32gui.IsWindowVisible(h):
        title = win32gui.GetWindowText(h)
        if title.strip():
            hwnds.append(title)
    return True
win32gui.EnumWindows(callback, hwnds)

for t in sorted(hwnds):
    print(repr(t))
