from view.SettingWindow import SettingWindow 
from PySide6.QtCore import QObject, Signal, Slot
from model import Model
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer
from PySide6.QtCore import Qt

class SettingController(QObject):
  def __init__(self, view:SettingWindow, model:Model):
    super().__init__()
    self.view = view
    self.model = model
    self.view.saveButton.clicked.connect(self.saveSettings)
  def saveSettings(self):
    print("Saving settings...")
    self.model.saveSetting("scanner_port", self.view.portEdit.text())
    self.model.saveSetting("scanner_baudrate", self.view.baudrateEdit.text())
    self.model.saveSetting("bank_number", self.view.bankNumberEdit.text())
    self.model.saveSetting("bank_bin", self.view.bankBinEdit.text())
    #Popup save success message for 2 seconds
    label = QLabel("✅ Settings saved successfully")
    label.setWindowFlags(Qt.WindowType.ToolTip)   # looks like a tooltip
    label.show()

    QTimer.singleShot(2000, label.close)


