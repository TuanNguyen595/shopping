from PySide6.QtWidgets import (
  QCheckBox, QLabel, QLayout, QLineEdit, QMainWindow, QGridLayout, QPushButton, QVBoxLayout, QWidget, QHBoxLayout,
  QFormLayout, QGroupBox, QTableWidget, QComboBox, QHeaderView, QTableWidgetItem, QTabWidget
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from model import Model
from view.components.CPushButton import CPushButton
from i18n import t

class SettingWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.saveButton = CPushButton(t("btn_save_settings"))
    self.saveButton.setIcon(QIcon("icons/save.png"))
 
  def setDatabase(self, database: Model):
    self.db = database
    self.createLayout()
  def createLayout(self):
    layout = QGridLayout()
    self.setLayout(layout)
    self.scannerPortLabel = QLabel(t("scanner_port_label"))
    layout.addWidget(self.scannerPortLabel, 0, 0)
    self.portEdit = QLineEdit()
    self.portEdit.setClearButtonEnabled(True)
    self.portEdit.setText(self.db.loadSetting("scanner_port") or "")
    layout.addWidget(self.portEdit, 0, 1)
    self.scannerBaudrateLabel = QLabel(t("scanner_baudrate_label"))
    layout.addWidget(self.scannerBaudrateLabel, 1, 0)
    self.baudrateEdit = QLineEdit()
    self.baudrateEdit.setClearButtonEnabled(True)
    self.baudrateEdit.setText(self.db.loadSetting("scanner_baudrate") or "")
    layout.addWidget(self.baudrateEdit, 1, 1)
    self.bankNumberLabel = QLabel(t("bank_number_label"))
    layout.addWidget(self.bankNumberLabel, 2, 0)
    self.bankNumberEdit = QLineEdit()
    self.bankNumberEdit.setClearButtonEnabled(True)
    self.bankNumberEdit.setText(self.db.loadSetting("bank_number") or "")
    layout.addWidget(self.bankNumberEdit, 2, 1)
    self.bankBinLabel = QLabel(t("bank_bin_label"))
    layout.addWidget(self.bankBinLabel, 3, 0)
    self.bankBinEdit = QLineEdit()
    self.bankBinEdit.setClearButtonEnabled(True)
    self.bankBinEdit.setText(self.db.loadSetting("bank_bin") or "")
    layout.addWidget(self.bankBinEdit, 3, 1)
    self.languageLabel = QLabel(t("language_label"))
    layout.addWidget(self.languageLabel, 4, 0)
    self.languageCombo = QComboBox()
    self.languageCombo.addItem("Tiếng Việt", "vi")
    self.languageCombo.addItem("English", "en")
    current_lang = self.db.loadSetting("language") or "vi"
    idx = self.languageCombo.findData(current_lang)
    if idx >= 0:
      self.languageCombo.setCurrentIndex(idx)
    layout.addWidget(self.languageCombo, 4, 1)
    self.fontSizeLabel = QLabel(t("font_size_label"))
    layout.addWidget(self.fontSizeLabel, 5, 0)
    self.fontSizeCombo = QComboBox()
    for size in [10, 11, 12, 13, 14, 16, 18, 20]:
      self.fontSizeCombo.addItem(f"{size} pt", size)
    saved_size = int(self.db.loadSetting("font_size") or 12)
    idx2 = self.fontSizeCombo.findData(saved_size)
    if idx2 >= 0:
      self.fontSizeCombo.setCurrentIndex(idx2)
    layout.addWidget(self.fontSizeCombo, 5, 1)
    layout.addWidget(self.saveButton, 6, 0)

  def retranslate(self):
    self.scannerPortLabel.setText(t("scanner_port_label"))
    self.scannerBaudrateLabel.setText(t("scanner_baudrate_label"))
    self.bankNumberLabel.setText(t("bank_number_label"))
    self.bankBinLabel.setText(t("bank_bin_label"))
    self.languageLabel.setText(t("language_label"))
    self.fontSizeLabel.setText(t("font_size_label"))
    self.saveButton.setText(t("btn_save_settings"))
 
