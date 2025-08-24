from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
  QLabel, QLayout, QLineEdit, QMainWindow, QGridLayout, QPushButton, QVBoxLayout, QWidget, QHBoxLayout,
  QFormLayout, QGroupBox, QTableWidget, QComboBox, QHeaderView, QTableWidgetItem, QTabWidget
)
from PySide6.QtCore import Qt
from view.components.MyWidget import CWidget
from view.components.CPushButton import CPushButton
from model import Model
from view.CustomBarcodesWindow import BarcodeListWindow
from PySide6.QtGui import QIcon

class ImportWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.createLayout()
  def setDatabase(self, database: Model):
    self.db = database
    self.customBarcodesWindow = BarcodeListWindow(self.db)
    self.customBarcodes.clicked.connect(self.customBarcodesWindow.show)
 
  def createLayout(self):
    layout = QVBoxLayout()
    self.layoutGrid = QHBoxLayout()
    self.infoColumn = QVBoxLayout()
    self.headerColumn = QVBoxLayout()
    self.toolColumn = QHBoxLayout()
    self.layoutGrid.addLayout(self.headerColumn)
    self.layoutGrid.addLayout(self.infoColumn)
    layout.addLayout(self.layoutGrid)
    layout.addLayout(self.toolColumn)
    self.headerColumn.addWidget(QLabel("Mã sản phẩm"))
    self.headerColumn.addWidget(QLabel("Tên sản phẩm"))
    self.headerColumn.addWidget(QLabel("Số lượng"))
    self.headerColumn.addWidget(QLabel("Giá nhập vào"))
    self.headerColumn.addWidget(QLabel("Giá bán lẻ"))
    #self.headerColumn.addWidget(QLabel("Giá bán buôn"))
    self.itemID = QLineEdit()
    self.itemID.setPlaceholderText("Ma san pham")
    self.itemName = QLineEdit()
    self.itemName.setPlaceholderText("Ten san pham")
    self.itemInStock = QLineEdit()
    self.itemInStock.setPlaceholderText("So luong")
    self.itemInStock.setValidator(QIntValidator(0, 9999999))
    self.importPrice = QLineEdit()
    self.importPrice.setPlaceholderText("Gia nhap vao")
    self.importPrice.setValidator(QIntValidator(0, 9999999))
    self.retailPrice = QLineEdit()
    self.retailPrice.setPlaceholderText("Gia ban le")
    self.retailPrice.setValidator(QIntValidator(0, 9999999))
    self.wholesalePrice = QLineEdit()
    self.wholesalePrice.setPlaceholderText("Gia ban buon")
    self.wholesalePrice.setValidator(QIntValidator(0, 9999999))
    self.infoColumn.addWidget(self.itemID)
    self.infoColumn.addWidget(self.itemName)
    self.infoColumn.addWidget(self.itemInStock)
    self.infoColumn.addWidget(self.importPrice)
    self.infoColumn.addWidget(self.retailPrice)
    #self.infoColumn.addWidget(self.wholesalePrice)
    self.addButton = CPushButton("Thêm mới")
    self.editButton = CPushButton("Cập nhật")
    self.removeButton = CPushButton("Xóa")
    self.findButton = CPushButton("Tìm kiếm")
    self.customBarcodes = QPushButton()
    self.customBarcodes.setIcon(QIcon.fromTheme("barcode"))
    self.customBarcodes.setFixedSize(40, 40)
    self.customBarcodes.setIconSize(self.customBarcodes.size() * 0.8)


    self.toolColumn.addWidget(self.addButton)
    self.toolColumn.addWidget(self.editButton)
    self.toolColumn.addWidget(self.removeButton)
    self.toolColumn.addWidget(self.findButton)
    self.toolColumn.addWidget(self.customBarcodes)
    self.setLayout(layout)

  def clearInput(self):
    self.itemID.clear()
    self.itemName.clear()
    self.itemInStock.clear()
    self.importPrice.clear()
    self.retailPrice.clear()
    self.wholesalePrice.clear()

  def onScannerResult(self, text):
    self.clearInput()
    self.itemID.setText(text)
    item = self.db.getItemById(text)
    if item:
      self.itemName.setText(item[1])
      self.itemInStock.setText(str(item[2]))
      self.importPrice.setText(str(item[5]))
      self.retailPrice.setText(str(item[3]))
      self.wholesalePrice.setText(str(item[4]))
    item = self.db.getBarcodeByCode(text)
    if item:
      self.itemName.setText(item[2])
 
  
