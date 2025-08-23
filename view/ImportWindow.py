from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
  QLabel, QLayout, QLineEdit, QMainWindow, QGridLayout, QPushButton, QVBoxLayout, QWidget, QHBoxLayout,
  QFormLayout, QGroupBox, QTableWidget, QComboBox, QHeaderView, QTableWidgetItem, QTabWidget
)
from PySide6.QtCore import Qt
from view.components.MyWidget import CWidget
from view.components.CPushButton import CPushButton
from model import Model

class ImportWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.createLayout()
  def setDatabase(self, database: Model):
    self.db = database
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
    self.headerColumn.addWidget(QLabel("Ma san pham"))
    self.headerColumn.addWidget(QLabel("Ten san pham"))
    self.headerColumn.addWidget(QLabel("So luong"))
    self.headerColumn.addWidget(QLabel("Gia nhap vao"))
    self.headerColumn.addWidget(QLabel("Gia ban le"))
    self.headerColumn.addWidget(QLabel("Gia ban buon"))
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
    self.infoColumn.addWidget(self.wholesalePrice)
    self.addButton = CPushButton("Add")
    self.editButton = CPushButton("Update")
    self.removeButton = CPushButton("Remove")
    self.findButton = CPushButton("Find")
    self.toolColumn.addWidget(self.addButton)
    self.toolColumn.addWidget(self.editButton)
    self.toolColumn.addWidget(self.removeButton)
    self.toolColumn.addWidget(self.findButton)
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
  
