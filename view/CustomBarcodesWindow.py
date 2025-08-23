from PySide6.QtCore import Qt, QBuffer, QByteArray, QIODevice, QTimer
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit,
    QVBoxLayout, QHBoxLayout, QInputDialog, QMessageBox, QScrollArea
)
from model import Model
from view.components.BarcodeWidget import BarcodeWidget
import random

class BarcodeListWindow(QWidget):
    """Main window containing a list of barcodes with search + add."""

    def __init__(self, db: Model):
        super().__init__()
        self.setWindowTitle("Barcode Manager")
        self.resize(550, 450)
        self.db = db

        # search bar
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search by name...")
        self.search_box.textChanged.connect(self.filter_barcodes)

        #self.timer = QTimer(self)
        #self.timer.timeout.connect(self.filterTimerCheck)
        #self.timer.start(1000)  # check every 1 second

        # scroll area for barcode list
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.list_container = QWidget()
        self.vbox = QVBoxLayout(self.list_container)
        self.scroll.setWidget(self.list_container)

        # buttons
        self.add_btn = QPushButton("Add New Barcode")
        self.add_btn.clicked.connect(self.add_barcode)

        layout = QVBoxLayout(self)
        layout.addWidget(self.search_box)
        layout.addWidget(self.scroll)
        layout.addWidget(self.add_btn)

        self.load_barcodes()

    def load_barcodes(self, filter_text: str = ""):
        """Load barcodes from DB with optional filter."""
        if filter_text == "":
          filter_text = self.search_box.text().strip()
        # clear existing
        for i in reversed(range(self.vbox.count())):
            item = self.vbox.itemAt(i).widget()
            if item:
                item.setParent(None)
        rows = self.db.getAllBarcodes()
        for bid, code, name in rows:
            if filter_text and filter_text.lower() not in name.lower():
                continue
            item = BarcodeWidget(code, name)
            item.deleteEmitter.connect(self.deleteBarcode)
            item.editNameEmitter.connect(self.editBarcodeName)
            self.vbox.addWidget(item)
        self.vbox.addStretch()

    def editBarcodeName(self, code: str, new_name: str):
        """Edit barcode name and refresh list."""
        print(f"Editing barcode {code} to new name: {new_name}")
        barcode = self.db.getBarcodeByCode(code)
        print(f"Found barcode in DB: {barcode}")
        if barcode:
            self.db.updateBarcodeName(barcode[0], new_name)
        self.load_barcodes()

    def deleteBarcode(self, code: str):
        """Delete barcode and refresh list."""
        barcode = self.db.getBarcodeByCode(code)
        name = barcode[2] if barcode else "Unknown"
        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Ban muon xoa san pham {name}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.db.removeBarcodeByCode(code)
        self.load_barcodes()

    def filter_barcodes(self, text: str):
        """Filter barcodes based on search text."""
        self.load_barcodes(text.strip())

    def add_barcode(self):
        """Add new barcode and refresh list."""
        code = ''.join(random.choices("0123456789", k=12))
        name, ok2 = QInputDialog.getText(self, "New Barcode", "Enter name (label):")
        if not ok2 or not name.strip():
            return
        self.db.addBarcode(name.strip(), code)
        self.load_barcodes()

    def filterTimerCheck(self):
        self.filter_barcodes(self.search_box.text().strip())

