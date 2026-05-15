from PySide6.QtWidgets import (
    QLabel, QLineEdit, QMainWindow, QGridLayout, QVBoxLayout, QWidget, QTabWidget,
    QPushButton
)
from PySide6.QtCore import Qt, Signal, Slot
from view.components.MyWidget import CWidget
from view.OrderWindow import OrderWindow
from view.ImportWindow import ImportWindow
from view.SettingWindow import SettingWindow
from view.StatisticWindow import StatisticWindow
from i18n import t

class MainWindow(QMainWindow):
  mockScannerSignal = Signal(str)
  def __init__(self):
    super().__init__()
    self.setWindowTitle(t('app_title'))
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
    self.statisticWindow = StatisticWindow()
    self.mainTab.addTab(self.orderWindow, t("tab_order"))
    self.mainTab.addTab(self.importWindow, t("tab_import"))
    self.mainTab.addTab(self.statisticWindow, t("tab_statistic"))
    self.settingWindow = SettingWindow()
    self.mainTab.addTab(self.settingWindow, t("tab_setting"))
    layout.addWidget(self.mainTab)
    mainWidget = CWidget()
    mainWidget.setLayout(layout)
    self.setCentralWidget(mainWidget)
    self.mockScanner.returnPressed.connect(lambda: self.mockScannerSignal.emit(self.mockScanner.text()))

  def retranslate(self):
    self.setWindowTitle(t('app_title'))
    self.mainTab.setTabText(0, t('tab_order'))
    self.mainTab.setTabText(1, t('tab_import'))
    self.mainTab.setTabText(2, t('tab_statistic'))
    self.mainTab.setTabText(3, t('tab_setting'))

  def setDatabase(self, database):
    self.db = database
    self.orderWindow.setDatabase(database)
    self.importWindow.setDatabase(database)
    self.statisticWindow.setDatabase(database)
    self.settingWindow.setDatabase(database)
