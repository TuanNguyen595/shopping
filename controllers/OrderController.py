from PySide6.QtGui import Qt
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem
from view.OrderWindow import OrderWindow
from PySide6.QtCore import QObject, Signal, Slot
from view.components import gen_vietqr
from model import Model

class OrderController(QObject):
  def __init__(self, view: OrderWindow, model:Model):
    super().__init__()
    self.view = view
    self.model = model
    self.view.order_items.cellChanged.connect(self.onTableChanged)
    self.view.order_items.cellClicked.connect(self.onTableClicked)
    self.view.createOrderBtn.clicked.connect(self.onPaymentButtonClicked)
    self.view.cancelOrderBtn.clicked.connect(self.onCancelButtonClicked)
    self.view.saveOrderBtn.clicked.connect(self.onSaveButtonClicked)

  def onSaveButtonClicked(self):
    customer_id = None
    if self.view.customer_name.text().strip() :
      customer_id = self.model.addCustomer(self.view.customer_name.text())
      self.view.customer_name_lable.setStyleSheet("")
    else:
      self.view.customer_name_lable.setStyleSheet("color: red;")
      return
    order_id = self.model.addOrder(None or customer_id, 
                        self.view.order_date.text() or self.view.order_date.placeholderText(), 
                        self.view.total_value.text(), self.view.order_status.checkState() == Qt.CheckState.Checked)
    for row in range(self.view.order_items.rowCount()):
      self.model.addOrderItem(order_id, self.view.order_items.item(row, 0).text(), int(self.view.order_items.item(row, 3).text()))

    pass
  def onPaidButtonClicked(self):
    self.view.QRDialog.close()
    customer_id = None
    if self.view.customer_name.text().strip() :
      customer_id = self.model.addCustomer(self.view.customer_name.text(), debt=self.view.total_order_price)
    order_id = self.model.addOrder(None or customer_id, 
                        self.view.order_date.text() or self.view.order_date.placeholderText(), 
                        self.view.total_value.text())

    for row in range(self.view.order_items.rowCount()):
      quantity = int(self.view.order_items.item(row, 3).text().replace(",", ""))
      item_id = self.view.order_items.item(row, 0).text()
      current_stock = self.model.getItemStock(item_id) or 0
      remaining_stock = current_stock - quantity
      if remaining_stock < 0:
        remaining_stock = 0
      self.model.changeItemStock(item_id, current_stock - quantity)
      self.model.addOrderItem(order_id, self.view.order_items.item(row, 0).text(), int(self.view.order_items.item(row, 3).text()))
    self.view.order_items.setRowCount(0)
    self.sumTotalPrice()
    pass
  def onUnpaidButtonClicked(self):
    self.view.QRDialog.close()
    pass

  def onCancelButtonClicked(self):
    self.view.order_items.setRowCount(0)
    self.sumTotalPrice()
    pass
  def onPaymentButtonClicked(self):
    self.view.popupQRCode()
    self.view.QRDialog.paid_button.clicked.connect(self.onPaidButtonClicked)
    self.view.QRDialog.unpaid_button.clicked.connect(self.onUnpaidButtonClicked)
    self.view.QRDialog.exec()
    pass
  def onTableClicked(self, row, col):
    if(col == 5):
      self.view.order_items.removeRow(row)
      self.sumTotalPrice()

  def onTableChanged(self, row, col):
    if(col != 3): return
    quantity = int(self.view.order_items.item(row, 3).text().replace(",", ""))
    price_per_unit = int(self.view.order_items.item(row, 2).text().replace(",", ""))
    total = quantity * price_per_unit
    self.view.order_items.item(row, 4).setText(f"{total:,}")
    self.sumTotalPrice()   

  def sumTotalPrice(self):
    total = 0
    for row in range(self.view.order_items.rowCount()):
      quantity = int(self.view.order_items.item(row, 3).text().replace(",", ""))
      price_per_unit = int(self.view.order_items.item(row, 2).text().replace(",", ""))
      total += quantity * price_per_unit
    self.view.total_order_price = total
    self.view.total_value.setText(f"{self.view.total_order_price:,}")
    return total
    
  @Slot(str)
  def onScannerResult(self, text):
    if(self.view.isVisible()):
      self.view.onScannerResult(text)


