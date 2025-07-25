from PySide6.QtWidgets import (
    QLabel, QLineEdit, QMainWindow, QGridLayout, QVBoxLayout, QWidget, QTabWidget
)
from PySide6.QtCore import Qt
from view.components.MyWidget import CWidget
from view.OrderWindow import OrderWindow
from view.ImportWindow import ImportWindow

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle('Tạp Hóa Hiền Dương')
    self.showMaximized()
    self.mockScanner = QLineEdit()
    self.mockScanner.setPlaceholderText('Fake scanner output')
    layout = QVBoxLayout()
    layout.addWidget(self.mockScanner)
    mainTab = QTabWidget()
    mainTab.setTabPosition(QTabWidget.TabPosition.North)
    self.orderWindow = OrderWindow()
    self.importWindow = ImportWindow()
    mainTab.addTab(self.orderWindow, "Ban hang")
    mainTab.addTab(self.importWindow, "Mua hang")
    mainTab.addTab(CWidget(), "Thong ke")
    layout.addWidget(mainTab)
    mainWidget = CWidget()
    mainWidget.setLayout(layout)
    self.setCentralWidget(mainWidget)
    self.mockScanner.returnPressed.connect(self.onScannerResult)

  def onScannerResult(self):
    if(self.orderWindow.isVisible()):
      self.orderWindow.onScannerResult(self.mockScanner.text())
    elif(self.importWindow.isVisible()):
      self.importWindow.onScannerResult(self.mockScanner.text())
  def setDatabase(self, database):
    self.db = database
    self.orderWindow.setDatabase(database)
    self.importWindow.setDatabase(database)

