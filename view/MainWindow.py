from PySide6.QtWidgets import (
    QLabel, QLineEdit, QMainWindow, QGridLayout, QVBoxLayout, QWidget, QTabWidget,
    QPushButton
)
from PySide6.QtCore import Qt, Signal, Slot
from view.components.MyWidget import CWidget
from view.OrderWindow import OrderWindow
from view.ImportWindow import ImportWindow
from view.SettingWindow import SettingWindow

class MainWindow(QMainWindow):
  mockScannerSignal = Signal(str)
  def __init__(self):
    super().__init__()
    self.setWindowTitle('Tạp Hóa Hiền Dương')
    self.showMaximized()
    #self.setGeometry(0, 0, 800, 600)
    self.mockScanner = QLineEdit()
    self.mockScanner.setPlaceholderText('Fake scanner output')
    layout = QVBoxLayout()
    #layout.addWidget(self.mockScanner)
    self.mainTab = QTabWidget()
    self.mainTab.setTabPosition(QTabWidget.TabPosition.North)
    self.orderWindow = OrderWindow()
    self.importWindow = ImportWindow()
    self.mainTab.addTab(self.orderWindow, "Bán hàng")
    self.mainTab.addTab(self.importWindow, "Mua hàng")
    #self.mainTab.addTab(CWidget(), "Thong ke")
    self.settingWindow = SettingWindow()
    self.mainTab.addTab(self.settingWindow, "Cài đặt")
    layout.addWidget(self.mainTab)
    mainWidget = CWidget()
    mainWidget.setLayout(layout)
    self.setCentralWidget(mainWidget)
    self.mockScanner.returnPressed.connect(lambda: self.mockScannerSignal.emit(self.mockScanner.text()))

  def setDatabase(self, database):
    self.db = database
    self.orderWindow.setDatabase(database)
    self.importWindow.setDatabase(database)
    self.settingWindow.setDatabase(database)
