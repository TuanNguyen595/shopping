from PySide6.QtWidgets import (
  QLabel, QLayout, QLineEdit, QMainWindow, QGridLayout, QPushButton, QVBoxLayout, QWidget, QHBoxLayout,
  QFormLayout, QGroupBox, QTableWidget, QComboBox, QHeaderView, QTableWidgetItem, QTabWidget
)
from PySide6.QtCore import Qt
from view.components.MyWidget import CWidget

class OrderWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.createLayout()
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
    items = [
        {"name": "Milk", "price": 20000, "quantity": 2},
        {"name": "Bread", "price": 10000, "quantity": 3},
        {"name": "Eggs", "price": 5000, "quantity": 6},
    ]
    self.total_order_price = sum(item["price"] * item["quantity"] for item in items)
    self.order_items.setRowCount(len(items))  # +1 for the total row
    self.order_items.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    #self.order_items.setMinimumHeight(20)
    for row, item in enumerate(items):
        total = item["price"] * item["quantity"]
        self.order_items.setItem(row, 0, QTableWidgetItem(item["name"]))
        self.order_items.setItem(row, 1, QTableWidgetItem(f"{item['price']:,}"))
        self.order_items.setItem(row, 2, QTableWidgetItem(str(item["quantity"])))
        self.order_items.setItem(row, 3, QTableWidgetItem(f"{total:,}"))

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

    total_value = QLabel(f"{self.total_order_price:,}")
    total_value.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
    total_value.setStyleSheet("font-weight: bold;")
    footer_layout.addWidget(total_value, 1)

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
    
