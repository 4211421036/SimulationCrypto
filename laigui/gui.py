from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTextEdit, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from pqcrypto import keygen, encrypt, decrypt

from PyQt5.QtCore import QThread, pyqtSignal

class EncryptWorker(QThread):
    finished = pyqtSignal(object)

    def __init__(self, pk, msg, k, p, a, P0):
        super().__init__()
        self.pk = pk
        self.msg = msg
        self.k = k
        self.p = p
        self.a = a
        self.P0 = P0

    def run(self):
        from pqcrypto import encrypt
        ct = encrypt(self.pk, self.msg, self.k, self.p, self.a, self.P0)
        self.finished.emit(ct)

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

        self.p = 10007
        self.a = 5
        self.P0 = (1, 0)
        self.k = 7

        # Generate keypair
        self.pk, self.sk = keygen(self.p, self.a, self.P0)

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
        self.encryptButton.setEnabled(False)
        self.encryptButton.setText("Encrypting...")

        self.worker = EncryptWorker(self.pk, msg, self.k, self.p, self.a, self.P0)
        self.worker.finished.connect(self.onEncryptionDone)
        self.worker.start()

    def onEncryptionDone(self, ct):
        self.last_cipher = ct
        self.encryptedText.setText(str(ct))
        self.encryptButton.setEnabled(True)
        self.encryptButton.setText("Encrypt")


    def decryptMessage(self):
        try:
            pt = decrypt(self.sk, self.last_cipher, self.k, self.p, self.a, self.P0)
            self.decryptedText.setText(pt.decode())
        except Exception as e:
            self.decryptedText.setText("Error during decryption: " + str(e))

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = LAIGUIApp()
    window.show()
    sys.exit(app.exec_())
