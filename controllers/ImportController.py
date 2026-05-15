from view.ImportWindow import ImportWindow
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QMessageBox
from model import Model
import random
from i18n import t

class ImportController(QObject):
  def __init__(self, view:ImportWindow, model:Model):
    super().__init__()
    self.view = view
    self.model = model
    self.view.addButton.clicked.connect(self.onAddButtonClicked)
    self.view.editButton.clicked.connect(self.onEditButtonClicked)
    self.view.findButton.clicked.connect(self.onFindButtonClicked)
    self.view.itemID.returnPressed.connect(self.onFindButtonClicked)
    self.view.itemID.editingFinished.connect(self.onFindButtonClicked)
    self.view.removeButton.clicked.connect(self.onRemoveButtonClicked)
    self.view.autoGenerateBarcode.clicked.connect(self.onAutoGenerateBarcodeClicked)

  @Slot(str)
  def onScannerResult(self, text):
    if(self.view.isVisible()):
      self.view.onScannerResult(text)

  def onAutoGenerateBarcodeClicked(self):
    code = ''.join(random.choices("0123456789", k=12))
    self.view.itemID.setText(code)
    self.view.generatingBarcode = True

  def onAddButtonClicked(self):
    itemID = self.view.itemID.text()
    itemName = self.view.itemName.text()
    if itemName.strip():
      self.view.itemNameLabel.setStyleSheet("")
    else:
      self.view.itemNameLabel.setStyleSheet("color: red;")
      return
    existing = self.model.getItemByName(itemName.strip())
    if existing:
      self.view.itemNameLabel.setStyleSheet("color: red;")
      QMessageBox.warning(
        self.view,
        t("warn_dup_name_title"),
        t("warn_dup_name_msg").format(name=itemName.strip())
      )
      return
    self.view.itemNameLabel.setStyleSheet("")
    unit = self.view.currency_unit
    if self.view.itemInStock.text() == "":
      itemInStock = 0
    else:
      itemInStock = int(self.view.itemInStock.text())
    if self.view.importPrice.text() == "":
      importPrice = 0
    else:
      importPrice = int(self.view.importPrice.text()) * unit
    if self.view.retailPrice.text() == "":
      retailPrice = 0
    else:
      retailPrice = int(self.view.retailPrice.text()) * unit
    if self.view.wholesalePrice.text() == "":
      wholesalePrice = 0
    else:
      wholesalePrice = int(self.view.wholesalePrice.text()) * unit
    self.model.addItem(itemID, itemName, itemInStock, retailPrice, wholesalePrice, importPrice)
    if self.view.generatingBarcode:
      code = self.view.itemID.text()
      name = self.view.itemName.text()
      self.model.addBarcode(name, code)
    self.view.clearInput()
  def onEditButtonClicked(self):
    itemID = self.view.itemID.text().strip()
    if not itemID:
      return
    unit = self.view.currency_unit
    self.model.changeItemName(itemID, self.view.itemName.text())
    add_qty = self.view.addStock.text().strip()
    if self.view.itemInStock.text() != "":
      new_stock = int(self.view.itemInStock.text())
      if add_qty:
        new_stock += int(add_qty)
      self.model.changeItemStock(itemID, new_stock)
    elif add_qty:
      current = self.model.getItemStock(itemID) or 0
      self.model.changeItemStock(itemID, current + int(add_qty))
    if self.view.retailPrice.text() != "":
      self.model.changeItemPrice(itemID, int(self.view.retailPrice.text()) * unit)
    if self.view.importPrice.text() != "":
      self.model.changeItemImportedPrice(itemID, int(self.view.importPrice.text()) * unit)
    if self.view.wholesalePrice.text() != "":
      self.model.changeItemWholesalePrice(itemID, int(self.view.wholesalePrice.text()) * unit)
    self.view.clearInput()

  def onFindButtonClicked(self):
    item = self.model.getItemById(self.view.itemID.text())
    if item:
      unit = self.view.currency_unit
      self.view.itemName.setText(item[1])
      self.view.itemInStock.setText(str(item[2]))
      self.view.importPrice.setText(str((item[5] or 0) // unit))
      self.view.retailPrice.setText(str((item[3] or 0) // unit))
      self.view.wholesalePrice.setText(str((item[4] or 0) // unit) if item[4] is not None else "")
    pass
  def onRemoveButtonClicked(self):
    itemID = self.view.itemID.text().strip()
    if not itemID:
      return
    self.model.removeItemById(itemID)
    self.view.clearInput()
