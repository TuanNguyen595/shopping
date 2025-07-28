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
    self.editButton = QPushButton("Update")
    self.removeButton = QPushButton("Remove")
    self.findButton = QPushButton("Find")
    self.toolColumn.addWidget(self.findButton)
    self.toolColumn.addWidget(self.editButton)
    self.toolColumn.addWidget(self.addButton)
    self.toolColumn.addWidget(self.removeButton)
    self.setLayout(self.layoutGrid)

  def onScannerResult(self, text):
    self.itemID.setText(text)
    item = self.db.getItemById(text)
    if item:
      self.itemName.setText(item[1])
      self.itemInStock.setText(str(item[2]))
      self.importPrice.setText(str(item[4]))
      self.retailPrice.setText(str(item[3]))
      self.wholesalePrice.setText(str(item[5]))
  
