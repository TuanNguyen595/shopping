import os
from sqlite3 import Date
from PySide6.QtWidgets import (
  QAbstractItemView, QCheckBox, QCompleter, QLabel, QLayout, QLineEdit, QMainWindow, QGridLayout, QPushButton, QVBoxLayout, QWidget, QHBoxLayout,
  QFormLayout, QGroupBox, QTableWidget, QComboBox, QHeaderView, QTableWidgetItem, QTabWidget
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QStringListModel
from model import Model
from view.components.MyWidget import CWidget
from view.components import gen_vietqr
from view.components.Calendar import CalendarDialog
from view.components.CPushButton import CPushButton
from view.CustomBarcodesWindow import BarcodeListWindow
from i18n import t

class OrderWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.createLayout()
  def popupQRCode(self):
    account_number = self.db.loadSetting("bank_number") or "0711000273413"
    bank_bin = self.db.loadSetting("bank_bin") or "970436"
    name = 'Tap hoa hien duong' 
    amount = self.total_order_price
    qr = gen_vietqr.generate_vietqr(account_number, bank_bin, name, amount, "Thanh toan don hang", "vietqr.png")
    self.QRDialog = gen_vietqr.QRDialog(qr, self)
  def setDatabase(self, database: Model):
    self.db = database
    self.customBarcodesWindow = BarcodeListWindow(self.db)
    self.customBarcodes.clicked.connect(self.customBarcodesWindow.show)
    # Shared completer model — updated whenever user focuses a name field
    self._customer_completer_model = QStringListModel()
    for field in (self.customer_name, self.search_customer):
      completer = QCompleter(self._customer_completer_model, self)
      completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
      completer.setFilterMode(Qt.MatchFlag.MatchContains)
      field.setCompleter(completer)
    self.customer_name.textEdited.connect(self._refresh_customer_completions)
    self.search_customer.textEdited.connect(self._refresh_customer_completions)
    self._refresh_customer_completions()

  def _refresh_customer_completions(self, _text=""):
    names = self.db.getAllCustomerNames()
    self._customer_completer_model.setStringList(names)
  def createLayout(self):
    self.utilColumn = CWidget()
    self.utilLayout = QVBoxLayout()
    self.utilTabWidget = QTabWidget()
    self.utilTabWidget.setTabPosition(QTabWidget.TabPosition.North)

    # --- Search tab ---
    searchTabWidget = CWidget()
    searchTabLayout = QVBoxLayout()

    formLayout = QGridLayout()
    self.searchCustomerLabel = QLabel(t("customer_name_label"))
    self.search_customer = QLineEdit()
    self.search_customer.setPlaceholderText(t("search_customer_ph"))
    self.search_customer.setClearButtonEnabled(True)
    self.searchDateFromLabel = QLabel(t("search_date_from_label"))
    self.search_date_from = QLineEdit()
    self.search_date_from.setPlaceholderText(t("search_date_from_ph"))
    self.search_date_from.setReadOnly(True)
    self.search_date_from.setClearButtonEnabled(True)
    cal_from_btn = QPushButton()
    cal_from_btn.setIcon(QIcon.fromTheme("calendar"))
    cal_from_btn.setFixedWidth(30)
    cal_from_btn.clicked.connect(lambda: self._pick_date(self.search_date_from))
    date_from_widget = CWidget()
    date_from_layout = QHBoxLayout()
    date_from_layout.setContentsMargins(0, 0, 0, 0)
    date_from_layout.addWidget(self.search_date_from)
    date_from_layout.addWidget(cal_from_btn)
    date_from_widget.setLayout(date_from_layout)

    self.searchDateToLabel = QLabel(t("search_date_to_label"))
    self.search_date_to = QLineEdit()
    self.search_date_to.setPlaceholderText(t("search_date_to_ph"))
    self.search_date_to.setReadOnly(True)
    self.search_date_to.setClearButtonEnabled(True)
    cal_to_btn = QPushButton()
    cal_to_btn.setIcon(QIcon.fromTheme("calendar"))
    cal_to_btn.setFixedWidth(30)
    cal_to_btn.clicked.connect(lambda: self._pick_date(self.search_date_to))
    date_to_widget = CWidget()
    date_to_layout = QHBoxLayout()
    date_to_layout.setContentsMargins(0, 0, 0, 0)
    date_to_layout.addWidget(self.search_date_to)
    date_to_layout.addWidget(cal_to_btn)
    date_to_widget.setLayout(date_to_layout)

    self.search_unpaid_only = QCheckBox(t("search_unpaid_only_label"))
    self.searchBtn = CPushButton(t("btn_search"))
    formLayout.addWidget(self.searchCustomerLabel, 0, 0)
    formLayout.addWidget(self.search_customer, 0, 1)
    formLayout.addWidget(self.searchDateFromLabel, 1, 0)
    formLayout.addWidget(date_from_widget, 1, 1)
    formLayout.addWidget(self.searchDateToLabel, 2, 0)
    formLayout.addWidget(date_to_widget, 2, 1)
    formLayout.addWidget(self.search_unpaid_only, 3, 0, 1, 2)
    formLayout.addWidget(self.searchBtn, 4, 0, 1, 2)
    formLayout.setColumnStretch(0, 1)
    formLayout.setColumnStretch(1, 2)

    self.search_results_table = QTableWidget()
    self.search_results_table.setColumnCount(5)
    self.search_results_table.setHorizontalHeaderLabels(
      [t("col_order_id"), t("col_customer"), t("col_date"), t("col_total"), t("col_paid")])
    self.search_results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    self.search_results_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    self.search_results_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

    searchTabLayout.addLayout(formLayout)
    searchTabLayout.addWidget(self.search_results_table)
    searchTabWidget.setLayout(searchTabLayout)

    self.utilTabWidget.addTab(searchTabWidget, t("tab_search_order"))
    self.utilLayout.addWidget(self.utilTabWidget)
    self.utilColumn.setLayout(self.utilLayout)


    self.infoColumn = CWidget()
    self.infoBox = CWidget()
    layout = QVBoxLayout()
    self.infoBox.setLayout(layout)

    # Table widget
    self.order_items = QTableWidget()
    self.order_items.setColumnCount(6)
    self.order_items.setHorizontalHeaderLabels([t("col_id"), t("col_product"), t("col_price"), t("col_qty"), t("col_total"), ""])
    self.order_items.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    self.order_items.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
    self.order_items.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

    # Order items data
    self.total_order_price = 0
    self.order_items.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    #self.order_items.setMinimumHeight(20)

    #self.order_items.cellChanged.connect(self.onTableChanged)
    # Fill total row (last row)
    # --- Footer: Total / Cash / Change
    footer = QWidget()
    footer_layout = QGridLayout()
    footer_layout.setContentsMargins(4, 4, 4, 4)
    footer_layout.setVerticalSpacing(4)

    self.total_label = QLabel(t("total_label"))
    self.total_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    self.total_label.setStyleSheet("font-size: 16px; font-weight: bold;")
    self.total_value = QLabel(f"{self.total_order_price:,}")
    self.total_value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    self.total_value.setStyleSheet("font-size: 16px; font-weight: bold;")

    self.cash_label = QLabel(t("cash_label"))
    self.cash_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    self.cash_input = QLineEdit()
    self.cash_input.setPlaceholderText("0")
    self.cash_input.setClearButtonEnabled(True)
    self.cash_input.setAlignment(Qt.AlignmentFlag.AlignRight)
    self.cash_input.textChanged.connect(self._updateChange)
    self.cash_input.textEdited.connect(self._onCashEdited)

    self.change_label = QLabel(t("change_label"))
    self.change_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    self.change_value = QLabel("0")
    self.change_value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    self.change_value.setStyleSheet("font-weight: bold;")

    footer_layout.addWidget(self.total_label,  0, 0)
    footer_layout.addWidget(self.total_value,  0, 1)
    footer_layout.addWidget(self.cash_label,   1, 0)
    footer_layout.addWidget(self.cash_input,   1, 1)
    footer_layout.addWidget(self.change_label, 2, 0)
    footer_layout.addWidget(self.change_value, 2, 1)
    footer_layout.setColumnStretch(0, 1)
    footer_layout.setColumnStretch(1, 1)
    footer.setLayout(footer_layout)

    header = CWidget()
    header_layout = QGridLayout()
    self.order_id = QLineEdit()
    self.order_id.setReadOnly(True)
    self.order_id.setClearButtonEnabled(True)
    self.order_date = QLineEdit()
    self.order_date.setPlaceholderText(Date.today().strftime("%Y-%m-%d"))
    self.customer_name = QLineEdit()
    self.customer_name.setClearButtonEnabled(True)
    self.customer_name_lable = QLabel(t("customer_name_label"))
    order_date_layout = QHBoxLayout()
    order_date_layout.addWidget(self.order_date)
    calendar_button = QPushButton()
    calendar_button.setIcon(QIcon.fromTheme("calendar"))  # Uses system icon if available
    calendar_button.setFixedWidth(30)
    calendar_button.clicked.connect(self.show_calendar)
    order_date_layout.addWidget(calendar_button)
    order_date_widget = CWidget()
    order_date_widget.setLayout(order_date_layout)
    self.order_status = QCheckBox()
    self.order_id_label = QLabel(t("order_id_label"))
    self.order_date_label = QLabel(t("order_date_label"))
    self.paid_label = QLabel(t("paid_status_label"))
    header_layout.addWidget(self.order_id_label, 0, 0)
    header_layout.addWidget(self.order_id, 0, 1)
    header_layout.addWidget(self.order_date_label, 1, 0)
    header_layout.addWidget(order_date_widget, 1, 1)
    header_layout.addWidget(self.customer_name_lable, 2, 0)
    header_layout.addWidget(self.customer_name, 2, 1)
    header_layout.addWidget(self.paid_label, 3, 0)
    header_layout.addWidget(self.order_status, 3, 1)
    header_layout.setColumnStretch(0,1)
    header_layout.setColumnStretch(1,2)
    header.setLayout(header_layout)

    layout.addWidget(header)
    layout.addWidget(self.order_items)
    layout.addWidget(footer)


    self.createOrderBtn = CPushButton(t("btn_payment"))
    self.cancelOrderBtn = CPushButton(t("btn_cancel"))
   
    self.saveOrderBtn = CPushButton(t("btn_save_order"))
    self.customBarcodes = QPushButton("")
    icon_path = os.path.join(os.getcwd(), "resource", "barcode.jpg")
    self.customBarcodes.setIcon(QIcon(icon_path))
    self.customBarcodes.setFixedSize(40, 40)
    self.customBarcodes.setIconSize(self.customBarcodes.size() * 0.8)

   
    layout = QGridLayout()
    layout.addWidget(self.infoBox, 0, 0, 1, 4)
    layout.addWidget(self.createOrderBtn, 1, 0)
    layout.addWidget(self.cancelOrderBtn, 1, 1)
    layout.addWidget(self.saveOrderBtn, 1, 2)
    layout.addWidget(self.customBarcodes, 1, 3)
    layout.setRowStretch(0, 1)
    layout.setRowStretch(1, 1)
    self.infoColumn.setLayout(layout)
    layout = QHBoxLayout()
    layout.addWidget(self.utilColumn, stretch=1)
    layout.addWidget(self.infoColumn, stretch=2)
    self.setLayout(layout)
  
  def _make_qty_widget(self, qty: int) -> QWidget:
    w = QWidget()
    layout = QHBoxLayout(w)
    layout.setContentsMargins(2, 0, 2, 0)
    layout.setSpacing(2)
    minus_btn = QPushButton("−")
    minus_btn.setFixedWidth(26)
    qty_label = QLabel(f"{qty:,}")
    qty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    qty_label.setMinimumWidth(30)
    plus_btn = QPushButton("+")
    plus_btn.setFixedWidth(26)
    layout.addWidget(minus_btn)
    layout.addWidget(qty_label)
    layout.addWidget(plus_btn)

    def _change(delta):
      row = self._find_widget_row(w)
      if row < 0:
        return
      cur = int(qty_label.text().replace(",", ""))
      new_qty = max(1, cur + delta)
      qty_label.setText(f"{new_qty:,}")
      price_item = self.order_items.item(row, 2)
      total_item = self.order_items.item(row, 4)
      if price_item and total_item:
        price = int(price_item.text().replace(",", ""))
        total_item.setText(f"{new_qty * price:,}")
      self.sumTotalPrice()

    minus_btn.clicked.connect(lambda: _change(-1))
    plus_btn.clicked.connect(lambda: _change(1))
    return w

  def _find_widget_row(self, widget: QWidget) -> int:
    for r in range(self.order_items.rowCount()):
      if self.order_items.cellWidget(r, 3) is widget:
        return r
    return -1

  def getRowQuantity(self, row: int) -> int:
    w = self.order_items.cellWidget(row, 3)
    if w:
      lbl = w.findChild(QLabel)
      if lbl:
        return int(lbl.text().replace(",", ""))
    item = self.order_items.item(row, 3)
    return int(item.text().replace(",", "")) if item else 1

  def _onCashEdited(self, text):
    digits = "".join(c for c in text if c.isdigit())
    if not digits:
      return
    formatted = f"{int(digits):,}"
    if formatted != text:
      cursor = self.cash_input.cursorPosition()
      old_len = len(text)
      self.cash_input.setText(formatted)
      self.cash_input.setCursorPosition(cursor + len(formatted) - old_len)

  def _updateChange(self, text):
    if not text.strip():
      self.change_value.setText("")
      self.change_value.setStyleSheet("font-weight: bold;")
      return
    try:
      cash = int(text.replace(",", ""))
    except ValueError:
      cash = 0
    change = cash - self.total_order_price
    self.change_value.setText(f"{change:,}")
    self.change_value.setStyleSheet(
      "font-weight: bold; color: green;" if change >= 0 else "font-weight: bold; color: red;"
    )

  def retranslate(self):
    self.order_items.setHorizontalHeaderLabels(
      [t("col_id"), t("col_product"), t("col_price"), t("col_qty"), t("col_total"), ""])
    self.search_results_table.setHorizontalHeaderLabels(
      [t("col_order_id"), t("col_customer"), t("col_date"), t("col_total"), t("col_paid")])
    self.searchCustomerLabel.setText(t("customer_name_label"))
    self.searchDateFromLabel.setText(t("search_date_from_label"))
    self.searchDateToLabel.setText(t("search_date_to_label"))
    self.search_customer.setPlaceholderText(t("search_customer_ph"))
    self.search_date_from.setPlaceholderText(t("search_date_from_ph"))
    self.search_date_to.setPlaceholderText(t("search_date_to_ph"))
    self.search_unpaid_only.setText(t("search_unpaid_only_label"))
    self.searchBtn.setText(t("btn_search"))
    self.total_label.setText(t("total_label"))
    self.cash_label.setText(t("cash_label"))
    self.change_label.setText(t("change_label"))
    self.order_id_label.setText(t("order_id_label"))
    self.order_date_label.setText(t("order_date_label"))
    self.customer_name_lable.setText(t("customer_name_label"))
    self.paid_label.setText(t("paid_status_label"))
    self.createOrderBtn.setText(t("btn_payment"))
    self.cancelOrderBtn.setText(t("btn_cancel"))
    self.saveOrderBtn.setText(t("btn_save_order"))
    self.utilTabWidget.setTabText(0, t("tab_search_order"))

  def onScannerResult(self, text):
    item = self.db.getItemById(text)
    if item is None: return
    self.order_items.insertRow(0)
    self.order_items.setItem(0, 0, QTableWidgetItem(item[0]))
    self.order_items.setItem(0, 1, QTableWidgetItem(item[1]))
    self.order_items.setItem(0, 2, QTableWidgetItem(f"{item[3]:,}"))
    quantity = 1
    total = item[3] * quantity
    self.order_items.setItem(0, 4, QTableWidgetItem(f"{total:,}"))
    self.order_items.setCellWidget(0, 3, self._make_qty_widget(quantity))
    self.sumTotalPrice()
    delete_item = QTableWidgetItem("❌")  # or just "X"
    delete_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    delete_item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
    self.order_items.setItem(0, 5, delete_item)

  def sumTotalPrice(self):
    total = 0
    for row in range(self.order_items.rowCount()):
      quantity = self.getRowQuantity(row)
      price_per_unit = int(self.order_items.item(row, 2).text().replace(",", ""))
      total += quantity * price_per_unit
    self.total_order_price = total
    self.total_value.setText(f"{self.total_order_price:,}")
    self._updateChange(self.cash_input.text())
    return total
  def show_calendar(self):
    dialog = CalendarDialog()
    if dialog.exec_():
      self.order_date.setText(dialog.selected_date().toString("yyyy-MM-dd"))

  def _pick_date(self, target: QLineEdit):
    dialog = CalendarDialog(self)
    if dialog.exec_():
      target.setText(dialog.selected_date().toString("yyyy-MM-dd"))
 
