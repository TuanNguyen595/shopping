from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
  QLabel, QLayout, QLineEdit, QMainWindow, QGridLayout, QPushButton, QVBoxLayout, QWidget, QHBoxLayout,
  QFormLayout, QGroupBox, QTableWidget, QComboBox, QHeaderView, QTableWidgetItem, QTabWidget
)
from PySide6.QtCore import Qt
from view.components.MyWidget import CWidget
from model import Model

class ImportWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.createLayout()
  def setDatabase(self, database: Model):
    self.db = database
  def createLayout(self):
    self.layoutGrid = QHBoxLayout()
    self.infoColumn = QVBoxLayout()
    self.toolColumn = QVBoxLayout()
    self.layoutGrid.addLayout(self.infoColumn)
    self.layoutGrid.addLayout(self.toolColumn)
    self.itemID = QLineEdit()
    self.itemID.setPlaceholderText("ID")
    self.itemName = QLineEdit()
    self.itemName.setPlaceholderText("Name")
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
    self.infoColumn.addWidget(self.wholesalePrice)
    self.addButton = QPushButton("Add")
    self.editButton = QPushButton("Edit")
    self.removeButton = QPushButton("Remove")
    self.findButton = QPushButton("Find")
    self.toolColumn.addWidget(self.findButton)
    self.toolColumn.addWidget(self.editButton)
    self.toolColumn.addWidget(self.addButton)
    self.toolColumn.addWidget(self.removeButton)
    self.setLayout(self.layoutGrid)
    self.addButton.clicked.connect(self.onAddButtonClicked)

  def onScannerResult(self, text):
    self.itemID.setText(text)
  def onAddButtonClicked(self):
    itemID = self.itemID.text()
    itemName = self.itemName.text()
    if self.itemInStock.text() == "":
      itemInStock = 0
    else:
      itemInStock = int(self.itemInStock.text())
    if self.importPrice.text() == "":
      importPrice = 0
    else:
      importPrice = int(self.importPrice.text())
    if self.retailPrice.text() == "":
      retailPrice = 0
    else:
      retailPrice = int(self.retailPrice.text())
    if self.wholesalePrice.text() == "":
      wholesalePrice = 0
    else:
      wholesalePrice = int(self.wholesalePrice.text())
    self.db.addItem(itemID, itemName, itemInStock, importPrice, retailPrice, wholesalePrice)
