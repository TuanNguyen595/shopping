from view.MainWindow import MainWindow
from model import Model
from PySide6.QtWidgets import QApplication
import sys
from controllers.OrderController import OrderController
from controllers.ImportController import ImportController
from view.components.ScannerListenner import ScannerListenner

class Controller:
  def __init__(self):
    self.db = Model()
  def run(self):
    app = QApplication()
    self.view = MainWindow()
    self.orderController = OrderController(self.view.orderWindow, self.db)
    self.importController = ImportController(self.view.importWindow, self.db)
    self.scannerListenner = ScannerListenner()
    self.view.mockScannerSignal.connect(self.scannerListenner.onScannerResult)
    self.scannerListenner.scannerResultEmiter.connect(self.orderController.onScannerResult)
    self.scannerListenner.scannerResultEmiter.connect(self.importController.onScannerResult)
    self.view.setDatabase(self.db)
    self.view.show()
    sys.exit(app.exec())
