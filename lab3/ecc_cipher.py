import sys
import os
import ecdsa
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5 import uic

# Đường dẫn đến file UI
UI_FILE = "./ui/ecc.ui"

# Tạo thư mục lưu khóa nếu chưa có
if not os.path.exists('cipher/ecc/keys'):
    os.makedirs('cipher/ecc/keys')


class ECCCipher:
    def __init__(self):
        pass

    def generate_keys(self):
        sk = ecdsa.SigningKey.generate()  # Tạo khóa riêng (private key)
        vk = sk.get_verifying_key()       # Tạo khóa công khai từ khóa riêng

        # Ghi khóa ra file
        with open('cipher/ecc/keys/privatekey.pem', 'wb') as f:
            f.write(sk.to_pem())
        with open('cipher/ecc/keys/publickey.pem', 'wb') as f:
            f.write(vk.to_pem())

    def load_keys(self):
        # Tải khóa riêng
        with open('cipher/ecc/keys/privatekey.pem', 'rb') as f:
            sk = ecdsa.SigningKey.from_pem(f.read())

        # Tải khóa công khai
        with open('cipher/ecc/keys/publickey.pem', 'rb') as f:
            vk = ecdsa.VerifyingKey.from_pem(f.read())

        return sk, vk

    def sign(self, message, private_key):
        return private_key.sign(message.encode('utf-8'))

    def verify(self, message, signature, public_key):
        try:
            return public_key.verify(signature, message.encode('utf-8'))
        except ecdsa.BadSignatureError:
            return False


class MyApp(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_FILE, self)

        self.cipher = ECCCipher()

        # Kết nối các nút trong giao diện với hàm xử lý
        self.pushButton.clicked.connect(self.generate_keys_action)  # "Generate Keys"
        self.btn_sign.clicked.connect(self.sign_action)             # "Sign"
        self.btn_verify.clicked.connect(self.verify_action)         # "Verify"

    def generate_keys_action(self):
        self.cipher.generate_keys()
        QMessageBox.information(self, "Success", "Keys generated successfully")

    def sign_action(self):
        message = self.txt_info.toPlainText().strip()
        if not message:
            QMessageBox.critical(self, "Error", "Please enter a message to sign.")
            return

        private_key, _ = self.cipher.load_keys()
        signature = self.cipher.sign(message, private_key)
        self.txt_sign.setText(signature.hex())
        QMessageBox.information(self, "Success", "Message signed successfully")

    def verify_action(self):
        message = self.txt_info.toPlainText().strip()
        signature_hex = self.txt_sign.toPlainText().strip()

        if not message or not signature_hex:
            QMessageBox.critical(self, "Error", "Please enter both message and signature.")
            return

        try:
            signature = bytes.fromhex(signature_hex)
        except ValueError:
            QMessageBox.critical(self, "Error", "Invalid signature format.")
            return

        _, public_key = self.cipher.load_keys()
        if self.cipher.verify(message, signature, public_key):
            QMessageBox.information(self, "Verified", "Signature is valid.")
        else:
            QMessageBox.warning(self, "Invalid", "Signature verification failed.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
