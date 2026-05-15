from PySide6.QtCore import Qt, QBuffer, QByteArray, QIODevice, QTimer
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit,
    QVBoxLayout, QHBoxLayout, QGridLayout, QInputDialog, QMessageBox, QScrollArea, QFrame
)
from model import Model
from view.components.BarcodeWidget import BarcodeWidget
import random
from i18n import t

GRID_COLS = 2

class BarcodeListWindow(QWidget):
    """Main window containing a grid of barcodes with search + add."""

    def __init__(self, db: Model):
        super().__init__()
        self.setWindowTitle(t("custom_barcodes_title"))
        self.resize(700, 500)
        self.db = db

        # search bar
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(t("search_barcode_ph"))
        self.search_box.textChanged.connect(self.filter_barcodes)

        # scroll area for barcode grid
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.list_container = QWidget()
        self.grid = QGridLayout(self.list_container)
        self.grid.setSpacing(10)
        self.scroll.setWidget(self.list_container)

        # buttons
        self.add_btn = QPushButton(t("btn_add_barcode"))
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
        # clear existing widgets from grid
        while self.grid.count():
            item = self.grid.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)

        rows = self.db.getAllBarcodes()
        rows.sort(key=lambda r: r[2].lower())
        col = 0
        row = 0
        for bid, code, name in rows:
            if filter_text and filter_text.lower() not in name.lower():
                continue
            card = self._make_card(code, name)
            self.grid.addWidget(card, row, col)
            col += 1
            if col >= GRID_COLS:
                col = 0
                row += 1
        # push remaining cells to top
        self.grid.setRowStretch(row + 1, 1)

    def _make_card(self, code: str, name: str) -> QWidget:
        card = QFrame()
        card.setFrameShape(QFrame.Shape.Box)
        card.setLineWidth(1)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(4, 4, 4, 4)
        item = BarcodeWidget(code, name)
        item.deleteEmitter.connect(self.deleteBarcode)
        item.editNameEmitter.connect(self.editBarcodeName)
        card_layout.addWidget(item)
        return card

    def editBarcodeName(self, code: str, new_name: str):
        barcode = self.db.getBarcodeByCode(code)
        if barcode:
            self.db.updateBarcodeName(barcode[0], new_name)
        self.load_barcodes()

    def deleteBarcode(self, code: str):
        barcode = self.db.getBarcodeByCode(code)
        name = barcode[2] if barcode else "Unknown"
        confirm = QMessageBox.question(
            self, t("confirm_delete_title"),
            t("confirm_delete_msg").format(name=name),
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.db.removeBarcodeByCode(code)
        self.load_barcodes()

    def filter_barcodes(self, text: str):
        self.load_barcodes(text.strip())

    def add_barcode(self):
        code = ''.join(random.choices("0123456789", k=12))
        name, ok2 = QInputDialog.getText(self, t("new_barcode_title"), t("new_barcode_prompt"))
        if not ok2 or not name.strip():
            return
        self.db.addBarcode(name.strip(), code)
        self.load_barcodes()

    def retranslate(self):
        self.setWindowTitle(t("custom_barcodes_title"))
        self.search_box.setPlaceholderText(t("search_barcode_ph"))
        self.add_btn.setText(t("btn_add_barcode"))
        self.load_barcodes()

    def showEvent(self, event):
        super().showEvent(event)
        for w in QApplication.topLevelWidgets():
            if w is not self and w.isVisible():
                geo = w.geometry()
                new_w = int(geo.width() * 0.9)
                new_h = int(geo.height() * 0.9)
                self.resize(new_w, new_h)
                self.move(geo.x() + (geo.width() - new_w) // 2,
                          geo.y() + (geo.height() - new_h) // 2)
                break
        self.load_barcodes()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)




