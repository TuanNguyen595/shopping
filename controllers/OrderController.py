from PySide6.QtGui import Qt
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem
from view.OrderWindow import OrderWindow
from PySide6.QtCore import QObject, Signal, Slot
from view.components import gen_vietqr
from model import Model
from i18n import t

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
    self.view.searchBtn.clicked.connect(self.onSearchButtonClicked)
    self.view.search_results_table.cellClicked.connect(self.onSearchResultClicked)

  def onSaveButtonClicked(self):
    customer_id = None
    name = self.view.customer_name.text().strip()
    if name:
      existing = self.model.getCustomerByName(name)
      customer_id = existing[0] if existing else self.model.addCustomer(name)
      self.view.customer_name_lable.setStyleSheet("")
    else:
      self.view.customer_name_lable.setStyleSheet("color: red;")
      return
    is_paid = self.view.order_status.checkState() == Qt.CheckState.Checked
    order_date = self.view.order_date.text() or self.view.order_date.placeholderText()
    total = int(self.view.total_value.text().replace(",", ""))

    existing_order_id = self.view.order_id.text().strip()
    if existing_order_id:
      # Update mode: restore old stock, replace items
      order_id = int(existing_order_id)
      old_order = self.model.getOrderById(order_id)
      old_was_paid = bool(old_order[4]) if old_order else False
      old_items = self.model.getOrderedItemsByOrderId(order_id)
      if old_was_paid:
        for oi in old_items:  # oi: (items_id, order_id, item_id, quantity)
          stock = self.model.getItemStock(oi[2]) or 0
          self.model.changeItemStock(oi[2], stock + oi[3])
      self.model.deleteOrderedItemsByOrderId(order_id)
      self.model.updateOrder(order_id, customer_id, order_date, total, is_paid)
    else:
      order_id = self.model.addOrder(customer_id, order_date, total, is_paid)

    for row in range(self.view.order_items.rowCount()):
      quantity = self.view.getRowQuantity(row)
      item_id = self.view.order_items.item(row, 0).text()
      self.model.addOrderItem(order_id, item_id, quantity)
      if is_paid:
        current_stock = self.model.getItemStock(item_id) or 0
        self.model.changeItemStock(item_id, max(0, current_stock - quantity))

    self.view.order_id.setText(str(order_id))
  def onPaidButtonClicked(self):
    self.view.QRDialog.close()
    customer_id = None
    name = self.view.customer_name.text().strip()
    if name:
      existing = self.model.getCustomerByName(name)
      customer_id = existing[0] if existing else self.model.addCustomer(name, debt=self.view.total_order_price)
    order_id = self.model.addOrder(customer_id,
                        self.view.order_date.text() or self.view.order_date.placeholderText(),
                        int(self.view.total_value.text().replace(",", "")))

    for row in range(self.view.order_items.rowCount()):
      quantity = self.view.getRowQuantity(row)
      item_id = self.view.order_items.item(row, 0).text()
      current_stock = self.model.getItemStock(item_id) or 0
      remaining_stock = current_stock - quantity
      if remaining_stock < 0:
        remaining_stock = 0
      self.model.changeItemStock(item_id, remaining_stock)
      self.model.addOrderItem(order_id, self.view.order_items.item(row, 0).text(), quantity)
    self.view.order_items.setRowCount(0)
    self.view.cash_input.clear()
    self.sumTotalPrice()
    pass
  def onUnpaidButtonClicked(self):
    self.view.QRDialog.close()
    pass

  def onCancelButtonClicked(self):
    self.view.order_id.clear()
    self.view.order_date.clear()
    self.view.customer_name.clear()
    self.view.order_status.setChecked(False)
    self.view.order_items.setRowCount(0)
    self.view.cash_input.clear()
    self.sumTotalPrice()
  def onPaymentButtonClicked(self):
    self.view.popupQRCode()
    try:
      self.view.QRDialog.paid_button.clicked.disconnect()
    except Exception:
      pass
    try:
      self.view.QRDialog.unpaid_button.clicked.disconnect()
    except Exception:
      pass
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
    try:
      quantity = int(self.view.order_items.item(row, 3).text().replace(",", ""))
      price_per_unit = int(self.view.order_items.item(row, 2).text().replace(",", ""))
    except (ValueError, AttributeError):
      return
    total = quantity * price_per_unit
    self.view.order_items.item(row, 4).setText(f"{total:,}")
    self.sumTotalPrice()

  def sumTotalPrice(self):
    total = 0
    for row in range(self.view.order_items.rowCount()):
      try:
        quantity = int(self.view.order_items.item(row, 3).text().replace(",", ""))
        price_per_unit = int(self.view.order_items.item(row, 2).text().replace(",", ""))
      except (ValueError, AttributeError):
        continue
      total += quantity * price_per_unit
    self.view.total_order_price = total
    self.view.total_value.setText(f"{self.view.total_order_price:,}")
    return total
    
  @Slot(str)
  def onScannerResult(self, text):
    if(self.view.isVisible()):
      self.view.onScannerResult(text)

  def onSearchButtonClicked(self):
    customer = self.view.search_customer.text().strip()
    date_from = self.view.search_date_from.text().strip()
    date_to = self.view.search_date_to.text().strip()
    unpaid_only = self.view.search_unpaid_only.isChecked()
    results = self.model.searchOrders(customer, date_from, date_to, unpaid_only)
    table = self.view.search_results_table
    table.setRowCount(0)
    for order_id, customer_name, order_date, total, paid in results:
      row = table.rowCount()
      table.insertRow(row)
      table.setItem(row, 0, QTableWidgetItem(str(order_id)))
      table.setItem(row, 1, QTableWidgetItem(customer_name or ""))
      table.setItem(row, 2, QTableWidgetItem(order_date or ""))
      table.setItem(row, 3, QTableWidgetItem(f"{int(str(total or 0).replace(',', '')):,}"))
      table.setItem(row, 4, QTableWidgetItem(t("val_paid") if paid else t("val_unpaid")))

  def onSearchResultClicked(self, row, col):
    order_id_item = self.view.search_results_table.item(row, 0)
    if not order_id_item:
      return
    order = self.model.getOrderById(int(order_id_item.text()))
    if not order:
      return
    # order: (order_id, customer_id, order_date, total_amount, paid)
    customer = self.model.getCustomerById(order[1]) if order[1] else None
    self.view.order_id.setText(str(order[0]))
    self.view.order_date.setText(order[2] or "")
    self.view.customer_name.setText(customer[1] if customer else "")
    self.view.order_status.setChecked(bool(order[4]))
    self.view.order_items.blockSignals(True)
    self.view.order_items.setRowCount(0)
    for oi in self.model.getOrderedItemsByOrderId(order[0]):
      # oi: (items_id, order_id, item_id, quantity)
      item = self.model.getItemById(oi[2])
      if item is None:
        continue
      r = self.view.order_items.rowCount()
      self.view.order_items.insertRow(r)
      self.view.order_items.setItem(r, 0, QTableWidgetItem(str(item[0])))
      self.view.order_items.setItem(r, 1, QTableWidgetItem(item[1]))
      self.view.order_items.setItem(r, 2, QTableWidgetItem(f"{item[3]:,}"))
      quantity = oi[3]
      self.view.order_items.setCellWidget(r, 3, self.view._make_qty_widget(quantity))
      self.view.order_items.setItem(r, 4, QTableWidgetItem(f"{item[3] * quantity:,}"))
      delete_item = QTableWidgetItem("\u274c")
      delete_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
      delete_item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
      self.view.order_items.setItem(r, 5, delete_item)
    self.view.order_items.blockSignals(False)
    self.sumTotalPrice()


