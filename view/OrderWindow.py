from PySide6.QtWidgets import (
  QLabel, QLayout, QLineEdit, QMainWindow, QGridLayout, QPushButton, QVBoxLayout, QWidget, QHBoxLayout,
  QFormLayout, QGroupBox, QTableWidget, QComboBox, QHeaderView, QTableWidgetItem, QTabWidget
)
from PySide6.QtCore import Qt
from model import Model
from view.components.MyWidget import CWidget

class OrderWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.createLayout()
  def setDatabase(self, database: Model):
    self.db = database
  def createLayout(self):
    self.utilColumn = CWidget()
    self.utilLayout = QVBoxLayout()
    self.utilTabWidget = QTabWidget()
    self.utilTabWidget.setTabPosition(QTabWidget.TabPosition.North)
    orderTabContent = QHBoxLayout()
    orderTabContent.addWidget(QLabel("Thong tin order"))
    orderTabContent.addWidget(QLabel("Ket qua tim kiem"))
    tabWidget = CWidget()
    tabWidget.setLayout(orderTabContent)
    self.utilTabWidget.addTab(tabWidget, "Tim kiem order")
    self.utilLayout.addWidget(self.utilTabWidget)
    self.utilLayout.addWidget(QPushButton("Tim kiem"), alignment=Qt.AlignmentFlag.AlignCenter)
    self.utilColumn.setLayout(self.utilLayout)


    self.infoColumn = CWidget()
    self.infoBox = CWidget()
    layout = QVBoxLayout()
    self.infoBox.setLayout(layout)

    # Table widget
    self.order_items = QTableWidget()
    self.order_items.setColumnCount(4)
    self.order_items.setHorizontalHeaderLabels(["Item", "Unit Price", "Quantity", "Total"])
    self.order_items.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    self.order_items.setColumnWidth(0, 120)

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
    header_layout.addWidget(QLabel("Ma don hang"), 0, 0)
    header_layout.addWidget(QLineEdit(), 0, 1)
    header_layout.addWidget(QLabel("Ngay/gio"), 1, 0)
    header_layout.addWidget(QLineEdit(), 1, 1)
    header_layout.addWidget(QLabel("Ten khac hang"), 2, 0)
    header_layout.addWidget(QLineEdit(), 2, 1)
    header_layout.addWidget(QLabel("Trang thai"), 3, 0)
    header_layout.addWidget(QLineEdit(), 3, 1)
    header_layout.setColumnStretch(0,1)
    header_layout.setColumnStretch(1,2)
    header.setLayout(header_layout)

    layout.addWidget(header)
    layout.addWidget(self.order_items)
    layout.addWidget(footer)


    self.createOrderBtn = QPushButton("Payment")
    self.createOrderBtn.setMinimumHeight(40)
    self.cancelOrderBtn = QPushButton("Cancel")
    self.cancelOrderBtn.setMinimumHeight(40)
   
    layout = QGridLayout()
    layout.addWidget(self.infoBox, 0, 0, 1, 2)
    layout.addWidget(self.createOrderBtn, 1, 0)
    layout.addWidget(self.cancelOrderBtn, 1, 1)
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
    self.order_items.setItem(0, 0, QTableWidgetItem(item[1]))
    self.order_items.setItem(0, 1, QTableWidgetItem(f"{item[4]:,}"))
    quantity = 1;
    total = item[4] * quantity
    self.order_items.setItem(0, 3, QTableWidgetItem(f"{total:,}"))
    self.order_items.setItem(0, 2, QTableWidgetItem(f"{quantity:,}"))
    self.sumTotalPrice()

  def sumTotalPrice(self):
    total = 0
    for row in range(self.order_items.rowCount()):
      quantity = int(self.order_items.item(row, 2).text().replace(",", ""))
      price_per_unit = int(self.order_items.item(row, 1).text().replace(",", ""))
      total += quantity * price_per_unit
    self.total_order_price = total
    self.total_value.setText(f"{self.total_order_price:,}")
    return total
    
