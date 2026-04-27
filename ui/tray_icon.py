from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPixmap, QColor, QPainter
import config

def create_icon():
    pixmap = QPixmap(64, 64)
    pixmap.fill(QColor(30, 30, 30))
    painter = QPainter(pixmap)
    painter.fillRect(16, 16, 32, 32, QColor(74, 222, 128))
    painter.end()
    return QIcon(pixmap)

class TrayIcon:
    def __init__(self, overlay_window, app):
        self.overlay = overlay_window
        self.app = app
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(create_icon())
        self.tray.setToolTip("WA-Stego")

    def setup(self):
        menu = QMenu()
        
        toggle_action = menu.addAction("Show/Hide Toolbar")
        toggle_action.triggered.connect(self.toggle_toolbar)
        
        lock_action = menu.addAction("Lock Session")
        lock_action.triggered.connect(self.lock_session)
        
        quit_action = menu.addAction("Quit")
        quit_action.triggered.connect(self.quit_app)
        
        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self.on_activated)

    def run(self):
        self.tray.show()

    def on_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.toggle_toolbar()

    def toggle_toolbar(self):
        if self.overlay.isVisible():
            self.overlay.hide()
        else:
            self.overlay.show()

    def lock_session(self):
        config.session.unlocked = False
        self.overlay.update_ui_state()

    def quit_app(self):
        self.tray.hide()
        self.app.quit()
