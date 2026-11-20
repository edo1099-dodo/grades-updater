import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt

GITHUB_URL = "https://github.com/edo1099-dodo/grades-updater"


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setFixedSize(380, 460)
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f7fb;
                color: #1e293b;
                font-family: Arial;
            }
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        image_label = QLabel()
        image_path = os.path.join(os.path.dirname(__file__), "avatar.png")
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            image_label.setPixmap(pixmap.scaled(130, 130, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)

        name_label = QLabel("Edo Israel")
        name_label.setFont(QFont("Arial", 18, QFont.Bold))
        name_label.setAlignment(Qt.AlignCenter)

        email_label = QLabel("edo1099@gmail.com")
        email_label.setFont(QFont("Arial", 12))
        email_label.setStyleSheet("color: #475569;")
        email_label.setAlignment(Qt.AlignCenter)

        linkedin_label = QLabel(
            '<a href="https://www.linkedin.com" style="color: #0a66c2; text-decoration: none;">LinkedIn</a>'
        )
        linkedin_label.setFont(QFont("Arial", 13, QFont.Bold))
        linkedin_label.setAlignment(Qt.AlignCenter)
        linkedin_label.setOpenExternalLinks(True)

        github_label = QLabel(
            f'<a href="{GITHUB_URL}" style="color: #2563eb; text-decoration: none;">GitHub: {GITHUB_URL}</a>'
        )
        github_label.setFont(QFont("Arial", 12, QFont.Bold))
        github_label.setAlignment(Qt.AlignCenter)
        github_label.setOpenExternalLinks(True)
        github_label.setWordWrap(True)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)

        layout.addWidget(image_label)
        layout.addWidget(name_label)
        layout.addWidget(email_label)
        layout.addWidget(linkedin_label)
        layout.addWidget(github_label)
        layout.addSpacing(8)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)
