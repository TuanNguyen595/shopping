from view.MainWindow import MainWindow
from model import Model
from PySide6.QtWidgets import QApplication
import sys

class Controller:
  def __init__(self):
    self.db = Model()
  def run(self):
    app = QApplication()
    self.view = MainWindow()
    self.view.show()
    sys.exit(app.exec())
