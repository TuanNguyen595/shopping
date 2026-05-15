import os
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
  QGroupBox, QLabel, QLineEdit, QGridLayout, QPushButton,
  QVBoxLayout, QWidget, QHBoxLayout, QFrame, QSizePolicy, QCompleter, QComboBox
)
from PySide6.QtCore import Qt, QStringListModel
from view.components.MyWidget import CWidget
from view.components.CPushButton import CPushButton
from model import Model
from view.CustomBarcodesWindow import BarcodeListWindow
from PySide6.QtGui import QIcon
from i18n import t

class ImportWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.generatingBarcode = False
    self.createLayout()

  def setDatabase(self, database: Model):
    self.db = database
    self.customBarcodesWindow = BarcodeListWindow(self.db)
    self.customBarcodes.clicked.connect(self.customBarcodesWindow.show)
    # restore saved currency unit
    saved_unit = self.db.loadSetting("currency_unit") or "1000"
    idx = self.currencyUnitCombo.findData(int(saved_unit))
    if idx >= 0:
      self.currencyUnitCombo.setCurrentIndex(idx)
    self.currencyUnitCombo.currentIndexChanged.connect(
      lambda: self.db.saveSetting("currency_unit", str(self.currency_unit))
    )
    # item name completer
    self._item_name_model = QStringListModel()
    completer = QCompleter(self._item_name_model, self)
    completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    completer.setFilterMode(Qt.MatchFlag.MatchContains)
    self.itemName.setCompleter(completer)
    self.itemName.textEdited.connect(self._refresh_item_name_completions)
    completer.activated.connect(self._onItemNameSelected)
    self._refresh_item_name_completions()

  def _refresh_item_name_completions(self, _text=""):
    self._item_name_model.setStringList(self.db.getAllItemNames())

  def _onItemNameSelected(self, name: str):
    item = self.db.getItemByName(name)
    if not item:
      return
    # item: (item_id, item_name, stock, retail_price, wholesale_price, imported_price)
    unit = self.currency_unit
    self.itemID.setText(str(item[0]))
    self.itemInStock.setText(str(item[2]))
    self.retailPrice.setText(str((item[3] or 0) // unit))
    self.wholesalePrice.setText(str((item[4] or 0) // unit) if item[4] is not None else "")
    self.importPrice.setText(str((item[5] or 0) // unit))

  @property
  def currency_unit(self) -> int:
    return self.currencyUnitCombo.currentData()

  def createLayout(self):
    # ── outer: form (left) | actions (right) ───────────────────────────
    outer = QHBoxLayout()
    outer.setSpacing(16)

    # ── LEFT: info group ──────────────────────────────────────────────
    self.infoGroup = QGroupBox(t("group_item_info"))
    formGrid = QGridLayout()
    formGrid.setVerticalSpacing(10)
    formGrid.setHorizontalSpacing(12)

    # Item ID row
    self.itemIDLabel = QLabel(t("item_id_label"))
    id_row = QHBoxLayout()
    id_row.setSpacing(4)
    self.itemID = QLineEdit()
    self.itemID.setReadOnly(True)
    self.itemID.setPlaceholderText(t("ph_item_id"))
    self.itemID.setClearButtonEnabled(True)
    self.autoGenerateBarcode = QPushButton()
    self.autoGenerateBarcode.setIcon(QIcon.fromTheme("view-refresh"))
    self.autoGenerateBarcode.setFixedSize(30, 30)
    self.autoGenerateBarcode.setToolTip(t("tooltip_auto_barcode"))
    id_row.addWidget(self.itemID)
    id_row.addWidget(self.autoGenerateBarcode)
    id_widget = QWidget()
    id_widget.setLayout(id_row)
    formGrid.addWidget(self.itemIDLabel, 0, 0)
    formGrid.addWidget(id_widget, 0, 1, 1, 3)

    # Item Name row
    self.itemNameLabel = QLabel(t("item_name_label"))
    self.itemName = QLineEdit()
    self.itemName.setPlaceholderText(t("ph_item_name"))
    self.itemName.setClearButtonEnabled(True)
    formGrid.addWidget(self.itemNameLabel, 1, 0)
    formGrid.addWidget(self.itemName, 1, 1, 1, 3)

    # In Stock row
    self.itemInStockLabel = QLabel(t("in_stock_label"))
    self.itemInStock = QLineEdit()
    self.itemInStock.setPlaceholderText(t("ph_in_stock"))
    self.itemInStock.setClearButtonEnabled(True)
    self.itemInStock.setValidator(QIntValidator(0, 9999999))
    formGrid.addWidget(self.itemInStockLabel, 2, 0)
    formGrid.addWidget(self.itemInStock, 2, 1, 1, 3)

    # Add stock row
    self.addStockLabel = QLabel(t("add_stock_label"))
    self.addStock = QLineEdit()
    self.addStock.setPlaceholderText(t("ph_add_stock"))
    self.addStock.setClearButtonEnabled(True)
    self.addStock.setValidator(QIntValidator(0, 9999999))
    formGrid.addWidget(self.addStockLabel, 3, 0)
    formGrid.addWidget(self.addStock, 3, 1, 1, 3)

    # Separator
    sep = QFrame()
    sep.setFrameShape(QFrame.Shape.HLine)
    sep.setFrameShadow(QFrame.Shadow.Sunken)
    formGrid.addWidget(sep, 4, 0, 1, 4)

    # Currency unit row
    self.currencyUnitLabel = QLabel(t("currency_unit_label"))
    self.currencyUnitCombo = QComboBox()
    self.currencyUnitCombo.addItem("1 đ", 1)
    self.currencyUnitCombo.addItem("1,000 đ", 1000)
    self.currencyUnitCombo.addItem("10,000 đ", 10000)
    self.currencyUnitCombo.addItem("100,000 đ", 100000)
    self.currencyUnitCombo.setCurrentIndex(1)  # default 1,000
    formGrid.addWidget(self.currencyUnitLabel, 5, 0)
    formGrid.addWidget(self.currencyUnitCombo, 5, 1)

    # Prices: Import | Retail | Wholesale
    self.importPriceLabel = QLabel(t("import_price_label"))
    self.importPrice = QLineEdit()
    self.importPrice.setPlaceholderText(t("ph_import_price"))
    self.importPrice.setClearButtonEnabled(True)
    self.importPrice.setValidator(QIntValidator(0, 9999999))

    self.retailPriceLabel = QLabel(t("retail_price_label"))
    self.retailPrice = QLineEdit()
    self.retailPrice.setPlaceholderText(t("ph_retail_price"))
    self.retailPrice.setClearButtonEnabled(True)
    self.retailPrice.setValidator(QIntValidator(0, 9999999))

    self.wholesalePriceLabel = QLabel(t("wholesale_price_label"))
    self.wholesalePrice = QLineEdit()
    self.wholesalePrice.setPlaceholderText(t("ph_wholesale_price"))
    self.wholesalePrice.setClearButtonEnabled(True)
    self.wholesalePrice.setValidator(QIntValidator(0, 9999999))

    formGrid.addWidget(self.importPriceLabel,   6, 0)
    formGrid.addWidget(self.importPrice,        6, 1)
    formGrid.addWidget(self.retailPriceLabel,   6, 2)
    formGrid.addWidget(self.retailPrice,        6, 3)
    formGrid.addWidget(self.wholesalePriceLabel, 7, 0)
    formGrid.addWidget(self.wholesalePrice,      7, 1)

    formGrid.setColumnStretch(1, 1)
    formGrid.setColumnStretch(3, 1)
    formGrid.setRowStretch(8, 1)  # pushes all rows to the top

    self.infoGroup.setLayout(formGrid)
    self.infoGroup.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    # ── RIGHT: action buttons ─────────────────────────────────────────
    actionLayout = QVBoxLayout()
    actionLayout.setSpacing(8)
    actionLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

    self.findButton    = CPushButton(t("btn_find"))
    self.findButton.hide()
    self.addButton     = CPushButton(t("btn_add"))
    self.editButton    = CPushButton(t("btn_edit"))
    self.removeButton  = CPushButton(t("btn_remove"))

    for btn in (self.addButton, self.editButton, self.removeButton):
      btn.setMinimumHeight(36)
      actionLayout.addWidget(btn)

    sep2 = QFrame()
    sep2.setFrameShape(QFrame.Shape.HLine)
    sep2.setFrameShadow(QFrame.Shadow.Sunken)
    actionLayout.addWidget(sep2)

    self.customBarcodes = QPushButton()
    icon_path = os.path.join(os.getcwd(), "resource", "barcode.jpg")
    self.customBarcodes.setIcon(QIcon(icon_path))
    self.customBarcodes.setFixedSize(44, 44)
    self.customBarcodes.setIconSize(self.customBarcodes.size() * 0.8)
    self.customBarcodes.setToolTip(t("tooltip_custom_barcodes"))
    actionLayout.addWidget(self.customBarcodes, alignment=Qt.AlignmentFlag.AlignHCenter)
    actionLayout.addStretch()

    actionWidget = QWidget()
    actionWidget.setLayout(actionLayout)
    actionWidget.setFixedWidth(130)

    outer.addWidget(self.infoGroup, stretch=1)
    outer.addWidget(actionWidget)
    self.setLayout(outer)

  def clearInput(self):
    self.itemID.clear()
    self.itemName.clear()
    self.itemInStock.clear()
    self.addStock.clear()
    self.importPrice.clear()
    self.retailPrice.clear()
    self.wholesalePrice.clear()

  def retranslate(self):
    self.infoGroup.setTitle(t("group_item_info"))
    self.itemIDLabel.setText(t("item_id_label"))
    self.itemNameLabel.setText(t("item_name_label"))
    self.itemInStockLabel.setText(t("in_stock_label"))
    self.addStockLabel.setText(t("add_stock_label"))
    self.currencyUnitLabel.setText(t("currency_unit_label"))
    self.importPriceLabel.setText(t("import_price_label"))
    self.retailPriceLabel.setText(t("retail_price_label"))
    self.wholesalePriceLabel.setText(t("wholesale_price_label"))
    self.itemID.setPlaceholderText(t("ph_item_id"))
    self.itemName.setPlaceholderText(t("ph_item_name"))
    self.itemInStock.setPlaceholderText(t("ph_in_stock"))
    self.addStock.setPlaceholderText(t("ph_add_stock"))
    self.importPrice.setPlaceholderText(t("ph_import_price"))
    self.retailPrice.setPlaceholderText(t("ph_retail_price"))
    self.wholesalePrice.setPlaceholderText(t("ph_wholesale_price"))
    self.addButton.setText(t("btn_add"))
    self.editButton.setText(t("btn_edit"))
    self.removeButton.setText(t("btn_remove"))
    self.findButton.setText(t("btn_find"))
    self.autoGenerateBarcode.setToolTip(t("tooltip_auto_barcode"))
    self.customBarcodes.setToolTip(t("tooltip_custom_barcodes"))

  def onScannerResult(self, text):
    self.generatingBarcode = False
    self.clearInput()
    self.itemID.setText(text)
    item = self.db.getItemById(text)
    if item:
      self.itemName.setText(item[1])
      self.itemInStock.setText(str(item[2]))
      self.importPrice.setText(str(item[5]))
      self.retailPrice.setText(str(item[3]))
      self.wholesalePrice.setText(str(item[4]))
    item = self.db.getBarcodeByCode(text)
    if item:
      self.itemName.setText(item[2])
 
  
