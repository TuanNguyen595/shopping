from sqlite3 import Date
from PySide6.QtWidgets import (
  QCheckBox, QLabel, QLayout, QLineEdit, QMainWindow, QGridLayout, QPushButton, QVBoxLayout, QWidget, QHBoxLayout,
  QFormLayout, QGroupBox, QTableWidget, QComboBox, QHeaderView, QTableWidgetItem, QTabWidget
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from model import Model
from view.components.MyWidget import CWidget
from view.components import gen_vietqr
from view.components.Calendar import CalendarDialog
from view.components.CPushButton import CPushButton
from view.CustomBarcodesWindow import BarcodeListWindow 

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
  def createLayout(self):
    self.utilColumn = CWidget()
    self.utilLayout = QVBoxLayout()
    self.utilTabWidget = QTabWidget()
    self.utilTabWidget.setTabPosition(QTabWidget.TabPosition.North)
    orderTabContent = QHBoxLayout()
    orderTabContent.addWidget(QLabel("Thông tin đơn hàng"))
    orderTabContent.addWidget(QLabel("Kết quả tìm kiếm"))
    tabWidget = CWidget()
    tabWidget.setLayout(orderTabContent)
    self.utilTabWidget.addTab(tabWidget, "Tìm kiếm order")
    self.utilLayout.addWidget(self.utilTabWidget)
    self.utilLayout.addWidget(CPushButton("Tìm kiếm"), alignment=Qt.AlignmentFlag.AlignCenter)
    self.utilColumn.setLayout(self.utilLayout)


    self.infoColumn = CWidget()
    self.infoBox = CWidget()
    layout = QVBoxLayout()
    self.infoBox.setLayout(layout)

    # Table widget
    self.order_items = QTableWidget()
    self.order_items.setColumnCount(6)
    self.order_items.setHorizontalHeaderLabels(["ID", "Sản phẩm", "Giá", "Số lượng", "Tổng",''])
    self.order_items.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    self.order_items.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

    # Order items data
    self.total_order_price = 0
    self.order_items.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    #self.order_items.setMinimumHeight(20)

    #self.order_items.cellChanged.connect(self.onTableChanged)
    # Fill total row (last row)
    # --- Total row (fixed footer)
    footer = QWidget()
    footer_layout = QHBoxLayout()
    footer_layout.setContentsMargins(0, 0, 0, 0)

    #spacer = QLabel()
    #footer_layout.addWidget(spacer, 3)

    total_label = QLabel("Total:")
    total_label.setAlignment(Qt.AlignmentFlag.AlignLeft| Qt.AlignmentFlag.AlignVCenter)
    total_label.setStyleSheet("font-size: 16px; font-weight: bold;")
    footer_layout.addWidget(total_label, 3)

    self.total_value = QLabel(f"{self.total_order_price:,}")
    self.total_value.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
    self.total_value.setStyleSheet("font-weight: bold;")
    footer_layout.addWidget(self.total_value, 1)

    footer.setLayout(footer_layout)

    header = CWidget()
    header_layout = QGridLayout()
    self.order_id = QLineEdit()
    self.order_date = QLineEdit()
    self.order_date.setPlaceholderText(Date.today().strftime("%Y-%m-%d"))
    self.customer_name = QLineEdit()
    self.customer_name_lable = QLabel("Tên khách hàng")
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
    header_layout.addWidget(QLabel("Mã đơn hàng"), 0, 0)
    header_layout.addWidget(self.order_id, 0, 1)
    header_layout.addWidget(QLabel("Ngày/giờ"), 1, 0)
    header_layout.addWidget(order_date_widget, 1, 1)
    header_layout.addWidget(self.customer_name_lable, 2, 0)
    header_layout.addWidget(self.customer_name, 2, 1)
    header_layout.addWidget(QLabel("Đã thanh toán"), 3, 0)
    header_layout.addWidget(self.order_status, 3, 1)
    header_layout.setColumnStretch(0,1)
    header_layout.setColumnStretch(1,2)
    header.setLayout(header_layout)

    layout.addWidget(header)
    layout.addWidget(self.order_items)
    layout.addWidget(footer)


    self.createOrderBtn = CPushButton("Thanh toán")
    self.cancelOrderBtn = CPushButton("Hủy")
   
    self.saveOrderBtn = CPushButton("Lưu trữ")
    self.customBarcodes = QPushButton("")
    self.customBarcodes.setIcon(QIcon.fromTheme("barcode"))
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
  
  def onScannerResult(self, text):
    item = self.db.getItemById(text)
    if item is None: return
    self.order_items.insertRow(0)
    self.order_items.setItem(0, 0, QTableWidgetItem(item[0]))
    self.order_items.setItem(0, 1, QTableWidgetItem(item[1]))
    self.order_items.setItem(0, 2, QTableWidgetItem(f"{item[4]:,}"))
    quantity = 1;
    total = item[4] * quantity
    self.order_items.setItem(0, 4, QTableWidgetItem(f"{total:,}"))
    self.order_items.setItem(0, 3, QTableWidgetItem(f"{quantity:,}"))
    self.sumTotalPrice()
    delete_item = QTableWidgetItem("❌")  # or just "X"
    delete_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    delete_item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
    self.order_items.setItem(0, 5, delete_item)

  def sumTotalPrice(self):
    total = 0
    for row in range(self.order_items.rowCount()):
      quantity = int(self.order_items.item(row, 3).text().replace(",", ""))
      price_per_unit = int(self.order_items.item(row, 2).text().replace(",", ""))
      total += quantity * price_per_unit
    self.total_order_price = total
    self.total_value.setText(f"{self.total_order_price:,}")
    return total
  def show_calendar(self):
    dialog = CalendarDialog()
    if dialog.exec_():
      self.order_date.setText(dialog.selected_date().toString("yyyy-MM-dd"))
 
