import os
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
    self.infoColumn = QVBoxLayout()
    self.toolColumn = QHBoxLayout()
    layout.addLayout(self.infoColumn)
    layout.addLayout(self.toolColumn)
    itemIDLayout = QHBoxLayout()
    itemIDWidget = QWidget()
    itemIDWidget.setLayout(itemIDLayout)
    itemNameLayout = QHBoxLayout()
    itemNameWidget = QWidget()
    itemNameWidget.setLayout(itemNameLayout)
    itemInStockLayout = QHBoxLayout()
    itemInStockWidget = QWidget()
    itemInStockWidget.setLayout(itemInStockLayout)
    importPriceLayout = QHBoxLayout()
    importPriceWidget = QWidget()
    importPriceWidget.setLayout(importPriceLayout)
    retailPriceLayout = QHBoxLayout()
    retailPriceWidget = QWidget()
    retailPriceWidget.setLayout(retailPriceLayout)
    itemIDLayout.addWidget(QLabel("Mã sản phẩm"))
    self.itemNameLabel = QLabel("Tên sản phẩm")
    itemNameLayout.addWidget(self.itemNameLabel)
    itemInStockLayout.addWidget(QLabel("Số lượng"))
    importPriceLayout.addWidget(QLabel("Giá nhập vào"))
    retailPriceLayout.addWidget(QLabel("Giá bán lẻ"))
    #self.headerColumn.addWidget(QLabel("Giá bán buôn"))
    self.itemID = QLineEdit()
    self.itemID.setPlaceholderText("Ma san pham")
    itemIDLayout.addWidget(self.itemID)
    self.autoGenerateBarcode = QPushButton("")
    self.autoGenerateBarcode.setIcon(QIcon.fromTheme("view-refresh"))
    self.autoGenerateBarcode.setFixedSize(27, 27)
    itemIDLayout.addWidget(self.autoGenerateBarcode)
    self.itemName = QLineEdit()
    self.itemName.setPlaceholderText("Ten san pham")
    itemNameLayout.addWidget(self.itemName)
    self.itemInStock = QLineEdit()
    self.itemInStock.setPlaceholderText("So luong")
    self.itemInStock.setValidator(QIntValidator(0, 9999999))
    itemInStockLayout.addWidget(self.itemInStock)
    self.importPrice = QLineEdit()
    self.importPrice.setPlaceholderText("Gia nhap vao")
    self.importPrice.setValidator(QIntValidator(0, 9999999))
    importPriceLayout.addWidget(self.importPrice)
    self.retailPrice = QLineEdit()
    self.retailPrice.setPlaceholderText("Gia ban le")
    self.retailPrice.setValidator(QIntValidator(0, 9999999))
    retailPriceLayout.addWidget(self.retailPrice)
    self.wholesalePrice = QLineEdit()
    self.wholesalePrice.setPlaceholderText("Gia ban buon")
    self.wholesalePrice.setValidator(QIntValidator(0, 9999999))

    itemIDLayout.setStretch(0, 1)
    itemIDLayout.setStretch(1, 8)
    itemNameLayout.setStretch(0, 1)
    itemNameLayout.setStretch(1, 8)
    itemInStockLayout.setStretch(0, 1)
    itemInStockLayout.setStretch(1, 8)
    importPriceLayout.setStretch(0, 1)
    importPriceLayout.setStretch(1, 8)
    retailPriceLayout.setStretch(0, 1)
    retailPriceLayout.setStretch(1, 8)
    self.infoColumn.addWidget(itemIDWidget)
    self.infoColumn.addWidget(itemNameWidget)
    self.infoColumn.addWidget(itemInStockWidget)
    self.infoColumn.addWidget(importPriceWidget)
    self.infoColumn.addWidget(retailPriceWidget)
    #self.infoColumn.addWidget(self.wholesalePrice)
    self.addButton = CPushButton("Thêm mới")
    self.editButton = CPushButton("Cập nhật")
    self.removeButton = CPushButton("Xóa")
    self.findButton = CPushButton("Tìm kiếm")
    self.customBarcodes = QPushButton()
    icon_path = os.path.join(os.getcwd(), "resource", "barcode.jpg")
    self.customBarcodes.setIcon(QIcon(icon_path))
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
    self.generatingBarcode = False
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
 
  
