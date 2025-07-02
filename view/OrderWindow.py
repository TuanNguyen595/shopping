from PySide6.QtWidgets import (
  QLabel, QLayout, QMainWindow, QGridLayout, QPushButton, QVBoxLayout, QWidget, QHBoxLayout,
  QFormLayout, QGroupBox, QTableWidget, QComboBox
)
from PySide6.QtCore import Qt
from view.components.MyWidget import CWidget

class OrderWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.createLayout()
  def createLayout(self):
    self.utilColumn = CWidget()
    self.infoColumn = CWidget()
    self.createOrderBtn = QPushButton("Payment")
    self.createOrderBtn.setMinimumHeight(40)
    self.cancelOrderBtn = QPushButton("Cancel")
    self.cancelOrderBtn.setMinimumHeight(40)
    self.infoBox = CWidget()
   
    layout = QGridLayout()
    layout.addWidget(self.infoBox, 0, 0, 1, 2)
    layout.addWidget(self.createOrderBtn, 1, 0)
    layout.addWidget(self.cancelOrderBtn, 1, 1)
    layout.setRowStretch(0, 1)
    layout.setRowStretch(1, 1)
    self.infoColumn.setLayout(layout)
    layout = QHBoxLayout()
    layout.addWidget(self.utilColumn)
    layout.addWidget(self.infoColumn)
    self.setLayout(layout)
    
