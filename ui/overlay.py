from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QApplication
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QRect
from PyQt6.QtGui import QColor, QPainter, QBrush, QPen
import win32gui
import config
import ui.pin_dialog as pin_dialog

class ToggleSwitch(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(50, 26)
        self._checked = False

    @property
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, value):
        self._checked = value
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._checked = not self._checked
            self.toggled.emit(self._checked)
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        bg_color = QColor("#00a884") if self._checked else QColor("#3b4a54")
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 13, 13)
        
        handle_color = QColor("#ffffff")
        painter.setBrush(QBrush(handle_color))
        if self._checked:
            painter.drawEllipse(self.width() - 24, 2, 22, 22)
        else:
            painter.drawEllipse(2, 2, 22, 22)

class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.toolbar = QWidget()
        self.toolbar.setStyleSheet("""
            QWidget { background-color: #202c33; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; border: 1px solid #111b21; border-top: none; }
            QLabel { color: #e9edef; font-family: 'Segoe UI', Helvetica, Arial, sans-serif; font-size: 13px; font-weight: bold; }
        """)
        
        tb_layout = QHBoxLayout(self.toolbar)
        tb_layout.setContentsMargins(15, 8, 15, 8)
        
        self.status_label = QLabel("Secure Mode")
        
        self.toggle = ToggleSwitch()
        self.toggle.checked = config.session.unlocked
        self.toggle.toggled.connect(self.on_toggle)
        
        tb_layout.addWidget(self.status_label)
        tb_layout.addStretch()
        tb_layout.addWidget(self.toggle)
        
        self.layout.addWidget(self.toolbar)
        self.setLayout(self.layout)
        
        self.wa_hwnd = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.track_whatsapp)
        self.timer.start(200)

    def on_toggle(self, checked):
        if checked:
            if not config.has_pin():
                dialog = pin_dialog.PinDialog(mode="set")
                if dialog.exec():
                    config.session.unlocked = True
                else:
                    self.toggle.checked = False
            else:
                dialog = pin_dialog.PinDialog(mode="check")
                if dialog.exec():
                    config.session.unlocked = True
                else:
                    self.toggle.checked = False
        else:
            config.session.unlocked = False
            from wa_watcher import trigger_scan
            trigger_scan()
            
        from wa_bridge import update_hook_state
        update_hook_state(config.session.unlocked)
        
        if config.session.unlocked:
            from wa_watcher import trigger_scan
            trigger_scan()

    def update_ui_state(self):
        self.toggle.checked = config.session.unlocked

    def track_whatsapp(self):
        try:
            hwnds = []
            def callback(h, hwnds):
                if win32gui.IsWindowVisible(h) and "WhatsApp" in win32gui.GetWindowText(h):
                    hwnds.append(h)
                return True
            win32gui.EnumWindows(callback, hwnds)
            
            if hwnds:
                hwnd = hwnds[0]
                self.wa_hwnd = hwnd
                rect = win32gui.GetWindowRect(hwnd)
                width = rect[2] - rect[0]
                
                overlay_width = 180
                x = rect[0] + (width - overlay_width) // 2
                y = rect[1]
                
                self.setGeometry(x, y, overlay_width, 42)
                if not self.isVisible():
                    self.show()
            else:
                self.hide()
        except Exception:
            pass
