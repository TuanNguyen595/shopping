import io
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QHBoxLayout, QInputDialog, QVBoxLayout
)
from barcode import Code128
from barcode.writer import ImageWriter
from view.components.CPushButton import CPushButton


def barcode_qimage(data: str) -> QImage:
  """Generate a Code128 barcode as QImage."""
  barcode = Code128(data, writer=ImageWriter())
  buf = io.BytesIO()
  barcode.write(buf)
  buf.seek(0)
  return QImage.fromData(buf.read(), "PNG")


class BarcodeWidget(QWidget):
  def __init__(self, data="HELLO123", label_text="My Barcode"):
    super().__init__()

    # --- barcode image ---
    self.code = data
    self.barcode_img = QLabel(alignment=Qt.AlignCenter)
    qimg = barcode_qimage(data)
    self.barcode_img.setPixmap(QPixmap.fromImage(qimg).
                               scaled(600, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    # --- label ---
    self.text_label = QLabel(label_text, alignment=Qt.AlignCenter)

    # --- button ---
    self.edit_btn = CPushButton("Doi ten")
    self.edit_btn.clicked.connect(self.editLabel)
    self.delete_btn = CPushButton("Xoa")
    self.delete_btn.clicked.connect(self.deleteBarCode)

    # --- layout ---
    layout = QHBoxLayout()
    code = QVBoxLayout()
    code.addWidget(self.barcode_img)
    code.addWidget(self.text_label)
    code.addStretch()
    codeWidget = QWidget()
    codeWidget.setLayout(code)
    layout.addWidget(codeWidget)
    #layout.addWidget(self.text_label)
    tool = QVBoxLayout()
    tool.addWidget(self.edit_btn)
    tool.addWidget(self.delete_btn)
    #tool.addStretch()
    toolWidget = QWidget()
    toolWidget.setLayout(tool)
    layout.addWidget(toolWidget)
    layout.setStretch(0, 4)
    layout.setStretch(1, 1)
    self.setLayout(layout)

  def editLabel(self):
    new_text, ok = QInputDialog.getText(self, "Edit Label", "Enter new text:", text=self.text_label.text())
    if ok and new_text.strip():
      self.text_label.setText(new_text)
      self.editNameEmitter.emit(self.code, new_text)

  def deleteBarCode(self):
    self.deleteEmitter.emit(self.code)

  deleteEmitter = Signal(str)
  editNameEmitter = Signal(str, str)
