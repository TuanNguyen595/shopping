from view.SettingWindow import SettingWindow 
from PySide6.QtCore import QObject, Signal, Slot
from model import Model
from PySide6.QtWidgets import QLabel, QApplication
from PySide6.QtGui import QFont
from PySide6.QtCore import QTimer
from PySide6.QtCore import Qt
from i18n import get_translator, t

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
    lang = self.view.languageCombo.currentData()
    self.model.saveSetting("language", lang)
    get_translator().load(lang)
    font_size = self.view.fontSizeCombo.currentData()
    self.model.saveSetting("font_size", str(font_size))
    app = QApplication.instance()
    if app:
      f = app.font()
      f.setPointSize(font_size)
      app.setFont(f)
    label = QLabel(t("settings_saved"))
    label.setWindowFlags(Qt.WindowType.ToolTip)
    label.show()
    QTimer.singleShot(2000, label.close)


