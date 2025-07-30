import qrcode
from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt

def generate_vietqr(account_number: str, bank_bin: str, name: str, amount: int, message: str, output_file="vietqr.png"):
    # VietQR static payload (simplified, not full EMV standard with CRC)
    # This string is for demo/testing purposes. For production, build full EMV TLV + CRC.

    # Just use an unofficial format many apps still support:
    qr_data = f"bank:{bank_bin}|acc:{account_number}|name:{name}|amount:{amount}|memo:{message}"

    # OR build a string similar to EMV (not fully spec-compliant):
    emv_payload = (
        "000201"  # Payload Format Indicator
        "010212"  # Point of Initiation Method (static)
        f"38{14 + (4 + (4 + len(bank_bin)) + (4 + len(account_number)) + 12)}"  # Placeholder for VietQR merchant account info (length prefix)
        "0010A000000727"
        f"01{((4 + len(bank_bin)) + (4 + len(account_number)))}"
        f"00{len(bank_bin):02}{bank_bin}"
        f"01{len(account_number):02}{account_number}"  # Format: BIN + Account
        "0208QRIBFTTA"
        "5303704"  # Currency: VND
        f"54{len(str(amount)):02}{amount}"  # Amount
        "5802VN"
        f"62{len(message) + 4:02}08{len(message):02}{message}"
        "6304"  # CRC placeholder (not included in this demo)
    )
    crc = vietqr_crc16(emv_payload)
    emv_payload = emv_payload + crc

    # Generate QR
    qr = qrcode.make(emv_payload)
    return qr

def vietqr_crc16(data_str: str) -> str:
    data = data_str.encode('utf-8')
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return f"{crc:04X}"

class QRDialog(QDialog):
    def __init__(self, qr_pil_image, parent=None):
        super().__init__(parent)
        self.setWindowTitle("QR Code")
        self.setFixedSize(300, 320)

        from io import BytesIO
        from PySide6.QtGui import QPixmap, QImage
        from PySide6.QtWidgets import QLabel, QVBoxLayout

        # Convert PIL image to QImage
        buffer = BytesIO()
        qr_pil_image.save(buffer, format="PNG")
        qimage = QImage.fromData(buffer.getvalue())

        # Show image
        layout = QVBoxLayout()
        label = QLabel()
        label.setPixmap(QPixmap.fromImage(qimage).scaled(250, 250))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        self.setLayout(layout)

