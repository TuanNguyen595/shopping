from view.ImportWindow import ImportWindow
from PySide6.QtCore import QObject, Signal, Slot
from model import Model
import random

class ImportController(QObject):
  def __init__(self, view:ImportWindow, model:Model):
    super().__init__()
    self.view = view
    self.model = model
    self.view.addButton.clicked.connect(self.onAddButtonClicked)
    self.view.editButton.clicked.connect(self.onEditButtonClicked)
    self.view.findButton.clicked.connect(self.onFindButtonClicked)
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
    if itemName.strip() :
      self.view.itemNameLabel.setStyleSheet("")
    else:
      self.view.itemNameLabel.setStyleSheet("color: red;")
      return
    if self.view.itemInStock.text() == "":
      itemInStock = 0
    else:
      itemInStock = int(self.view.itemInStock.text())
    if self.view.importPrice.text() == "":
      importPrice = 0
    else:
      importPrice = int(self.view.importPrice.text())
    if self.view.retailPrice.text() == "":
      retailPrice = 0
    else:
      retailPrice = int(self.view.retailPrice.text())
    if self.view.wholesalePrice.text() == "":
      wholesalePrice = 0
    else:
      wholesalePrice = int(self.view.wholesalePrice.text())
    self.model.addItem(itemID, itemName, itemInStock, importPrice, retailPrice, wholesalePrice)
    if self.view.generatingBarcode:
      code = self.view.itemID.text()
      name = self.view.itemName.text()
      self.model.addBarcode(name, code)
  def onEditButtonClicked(self):
    self.model.changeItemName(self.view.itemID.text(), self.view.itemName.text())
    if self.view.itemInStock.text() != "":
      self.model.changeItemStock(self.view.itemID.text(), int(self.view.itemInStock.text()))
    if self.view.retailPrice.text() != "":
      self.model.changeItemPrice(self.view.itemID.text(), int(self.view.retailPrice.text()))
    if self.view.importPrice.text() != "":
      self.model.changeItemImportedPrice(self.view.itemID.text(), int(self.view.importPrice.text()))
    if self.view.wholesalePrice.text() != "":
      self.model.changeItemWholesalePrice(self.view.itemID.text(), int(self.view.wholesalePrice.text()))
    pass
  def onFindButtonClicked(self):
    item = self.model.getItemById(self.view.itemID.text())
    if item:
      self.view.itemName.setText(item[1])
      self.view.itemInStock.setText(str(item[2]))
      self.view.importPrice.setText(str(item[5]))
      self.view.retailPrice.setText(str(item[3]))
      self.view.wholesalePrice.setText(str(item[4]))
    pass
  def onRemoveButtonClicked(self):
    self.model.removeItemById(self.view.itemID.text())
    pass
