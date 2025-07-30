from view.OrderWindow import OrderWindow
from PySide6.QtCore import QObject, Signal, Slot
from controllers.utils import gen_vietqr

class OrderController(QObject):
  def __init__(self, view: OrderWindow, model):
    super().__init__()
    self.view = view
    self.model = model
    self.view.order_items.cellChanged.connect(self.onTableChanged)
    self.view.order_items.cellClicked.connect(self.onTableClicked)
    self.view.createOrderBtn.clicked.connect(self.onPaymentButtonClicked)

  def onPaymentButtonClicked(self):
    account_number = '1029332970'
    bank_bin = '970436'
    name = 'Tap hoa hien duong' 
    amount = self.view.total_order_price
    qr = gen_vietqr.generate_vietqr(account_number, bank_bin, name, amount, "Thanh toan don hang", "vietqr.png")
    dialog = gen_vietqr.QRDialog(qr, self.view)
    dialog.exec()
    pass
  def onTableClicked(self, row, col):
    if(col == 4):
      self.view.order_items.removeRow(row)
      self.sumTotalPrice()

  def onTableChanged(self, row, col):
    if(col != 2): return
    quantity = int(self.view.order_items.item(row, 2).text().replace(",", ""))
    price_per_unit = int(self.view.order_items.item(row, 1).text().replace(",", ""))
    total = quantity * price_per_unit
    self.view.order_items.item(row, 3).setText(f"{total:,}")
    self.sumTotalPrice()   

  def sumTotalPrice(self):
    total = 0
    for row in range(self.view.order_items.rowCount()):
      quantity = int(self.view.order_items.item(row, 2).text().replace(",", ""))
      price_per_unit = int(self.view.order_items.item(row, 1).text().replace(",", ""))
      total += quantity * price_per_unit
    self.view.total_order_price = total
    self.view.total_value.setText(f"{self.view.total_order_price:,}")
    return total
    
  @Slot(str)
  def onScannerResult(self, text):
    if(self.view.isVisible()):
      self.view.onScannerResult(text)


