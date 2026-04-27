from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

class ChatOverlay(QWidget):
    def __init__(self, rect, text):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool | Qt.WindowType.WindowTransparentForInput)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.label = QLabel(text)
        self.label.setStyleSheet("""
            background-color: #005c4b;
            color: #e9edef;
            padding: 8px 12px;
            border-radius: 8px;
            font-family: 'Segoe UI', Helvetica, sans-serif;
            font-size: 14.5px;
            border: 1px solid #00a884;
        """)
        self.label.setWordWrap(True)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        
        self.update_rect(rect)
        
    def update_rect(self, rect):
        width = rect.right - rect.left
        height = rect.bottom - rect.top
        self.setGeometry(rect.left, rect.top, width, height)
