from view.OrderWindow import OrderWindow
from PySide6.QtCore import QObject, Signal, Slot

class OrderController(QObject):
  def __init__(self, view: OrderWindow, model):
    super().__init__()
    self.view = view
    self.model = model
    self.view.order_items.cellChanged.connect(self.onTableChanged)

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
    self.total_order_price = total
    self.view.total_value.setText(f"{self.total_order_price:,}")
    return total
    
  @Slot(str)
  def onScannerResult(self, text):
    if(self.view.isVisible()):
      self.view.onScannerResult(text)


