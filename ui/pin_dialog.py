from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt, QTimer
import config

class PinDialog(QDialog):
    def __init__(self, mode="check"):
        super().__init__()
        self.mode = mode
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.container = QWidget()
        self.container.setStyleSheet("""
            QWidget { background-color: #202c33; border-radius: 12px; border: 1px solid #111b21; }
            QLabel { color: #e9edef; font-family: 'Segoe UI', sans-serif; font-size: 15px; font-weight: bold; }
            QLineEdit { background-color: #2a3942; color: #e9edef; border: 1px solid #3b4a54; padding: 10px; border-radius: 6px; font-size: 16px; letter-spacing: 5px; }
            QLineEdit:focus { border: 1px solid #00a884; }
            QPushButton { background-color: #00a884; color: #111b21; font-weight: bold; font-family: 'Segoe UI'; padding: 10px; border-radius: 6px; border: none; font-size: 14px; }
            QPushButton:hover { background-color: #008f6f; }
            QPushButton#cancelBtn { background-color: transparent; color: #00a884; }
            QPushButton#cancelBtn:hover { background-color: #2a3942; }
        """)
        
        c_layout = QVBoxLayout(self.container)
        c_layout.setContentsMargins(20, 20, 20, 20)
        c_layout.setSpacing(15)
        
        title = "Set new PIN" if mode == "set" else "Enter PIN"
        self.label = QLabel(title)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pin_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin_input.returnPressed.connect(self.submit)
        
        btn_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.btn = QPushButton("Unlock" if mode == "check" else "Set PIN")
        self.btn.clicked.connect(self.submit)
        
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.btn)
        
        c_layout.addWidget(self.label)
        c_layout.addWidget(self.pin_input)
        c_layout.addLayout(btn_layout)
        
        self.layout.addWidget(self.container)
        self.setLayout(self.layout)
        self.setFixedSize(280, 180)
        
        self.attempts = 0

    def submit(self):
        pin = self.pin_input.text()
        if not pin:
            return
            
        if self.mode == "set":
            config.set_pin(pin)
            self.accept()
        else:
            if config.check_pin(pin):
                self.accept()
            else:
                self.attempts += 1
                self.pin_input.clear()
                self.label.setText(f"Incorrect PIN ({self.attempts})")
                self.label.setStyleSheet("color: #f28b82;")
                
                pos = self.pos()
                self.move(pos.x() + 10, pos.y())
                QTimer.singleShot(50, lambda: self.move(pos.x() - 20, pos.y()))
                QTimer.singleShot(100, lambda: self.move(pos.x() + 10, pos.y()))
                QTimer.singleShot(150, lambda: self.label.setStyleSheet("color: #e9edef;"))
                
                if self.attempts >= 3:
                    self.pin_input.setEnabled(False)
                    self.btn.setEnabled(False)
                    self.label.setText("Locked for 30s")
                    self.label.setStyleSheet("color: #f28b82;")
                    QTimer.singleShot(30000, self.unlock_input)

    def unlock_input(self):
        self.attempts = 0
        self.pin_input.setEnabled(True)
        self.btn.setEnabled(True)
        self.label.setText("Enter PIN")
        self.label.setStyleSheet("color: #e9edef;")
