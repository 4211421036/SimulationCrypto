from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTextEdit, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from pqcrypto import keygen, encrypt, decrypt


class LAIGUIApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LAICrypto GUI Encryption Tool")
        self.setGeometry(100, 100, 500, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: #f7f9fc;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QLineEdit, QTextEdit {
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 8px;
                background-color: white;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
        """)

        self.layout = QVBoxLayout()
        self.initUI()
        self.setLayout(self.layout)

        # Generate keypair
        self.pk, self.sk = keygen()

    def initUI(self):
        self.plainText = QLineEdit()
        self.plainText.setPlaceholderText("Enter message to encrypt")
        self.layout.addWidget(QLabel("Plaintext:"))
        self.layout.addWidget(self.plainText)

        self.encryptButton = QPushButton("Encrypt")
        self.encryptButton.clicked.connect(self.encryptMessage)
        self.layout.addWidget(self.encryptButton)

        self.encryptedText = QTextEdit()
        self.encryptedText.setReadOnly(True)
        self.layout.addWidget(QLabel("Ciphertext:"))
        self.layout.addWidget(self.encryptedText)

        self.decryptButton = QPushButton("Decrypt")
        self.decryptButton.clicked.connect(self.decryptMessage)
        self.layout.addWidget(self.decryptButton)

        self.decryptedText = QTextEdit()
        self.decryptedText.setReadOnly(True)
        self.layout.addWidget(QLabel("Decrypted Text:"))
        self.layout.addWidget(self.decryptedText)

    def encryptMessage(self):
        msg = self.plainText.text().encode()
        ct = encrypt(self.pk, msg)
        self.encryptedText.setText(str(ct))

        # Store for decryption
        self.last_cipher = ct

    def decryptMessage(self):
        try:
            pt = decrypt(self.sk, self.last_cipher)
            self.decryptedText.setText(pt.decode())
        except Exception as e:
            self.decryptedText.setText("Error during decryption: " + str(e))

