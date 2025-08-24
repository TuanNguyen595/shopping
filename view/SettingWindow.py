from PySide6.QtWidgets import (
  QCheckBox, QLabel, QLayout, QLineEdit, QMainWindow, QGridLayout, QPushButton, QVBoxLayout, QWidget, QHBoxLayout,
  QFormLayout, QGroupBox, QTableWidget, QComboBox, QHeaderView, QTableWidgetItem, QTabWidget
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from model import Model
from view.components.CPushButton import CPushButton

class SettingWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.saveButton = CPushButton("Save")
    self.saveButton.setIcon(QIcon("icons/save.png"))
 
  def setDatabase(self, database: Model):
    self.db = database
    self.createLayout()
  def createLayout(self):
    layout = QGridLayout()
    #layout.setColumnStretch(0, 1)
    #layout.setColumnStretch(1, 3)
    self.setLayout(layout)
    layout.addWidget(QLabel("Scanner Port"), 0, 0)
    self.portEdit = QLineEdit()
    self.portEdit.setText(self.db.loadSetting("scanner_port"))
    layout.addWidget(self.portEdit, 0, 1)
    layout.addWidget(QLabel("Scanner Baudrate"), 1, 0)
    self.baudrateEdit = QLineEdit()
    self.baudrateEdit.setText(self.db.loadSetting("scanner_baudrate"))
    layout.addWidget(self.baudrateEdit, 1, 1)
    self.bankNumberEdit = QLineEdit()
    layout.addWidget(QLabel("Bank number"), 2, 0)
    self.bankNumberEdit.setText(self.db.loadSetting("bank_number"))
    layout.addWidget(self.bankNumberEdit, 2, 1)
    layout.addWidget(QLabel("Bank Bin"), 3, 0)
    self.bankBinEdit = QLineEdit()
    self.bankBinEdit.setText(self.db.loadSetting("bank_bin"))
    layout.addWidget(self.bankBinEdit, 3, 1)


    layout.addWidget(self.saveButton, 4, 0)
    pass
 
