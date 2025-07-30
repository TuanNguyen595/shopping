from PySide6.QtWidgets import (
    QLabel, QLineEdit, QMainWindow, QGridLayout, QVBoxLayout, QWidget, QTabWidget
)
from PySide6.QtCore import Qt, Signal, Slot
from view.components.MyWidget import CWidget
from view.OrderWindow import OrderWindow
from view.ImportWindow import ImportWindow

class MainWindow(QMainWindow):
  mockScannerSignal = Signal(str)
  def __init__(self):
    super().__init__()
    self.setWindowTitle('Tạp Hóa Hiền Dương')
    #self.showMaximized()
    self.setGeometry(0, 0, 800, 600)
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
    self.mockScanner.returnPressed.connect(lambda: self.mockScannerSignal.emit(self.mockScanner.text()))

  def setDatabase(self, database):
    self.db = database
    self.orderWindow.setDatabase(database)
    self.importWindow.setDatabase(database)

