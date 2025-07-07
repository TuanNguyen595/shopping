from PySide6.QtWidgets import (
    QLabel, QMainWindow, QGridLayout, QVBoxLayout, QWidget, QTabWidget
)
from PySide6.QtCore import Qt
from view.components.MyWidget import CWidget
from view.OrderWindow import OrderWindow

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle('Tạp Hóa Hiền Dương')
    self.showMaximized()
    mainTab = QTabWidget()
    mainTab.setTabPosition(QTabWidget.TabPosition.North)
    mainTab.addTab(OrderWindow(), "Ban hang")
    mainTab.addTab(CWidget(), "Mua hang")
    mainTab.addTab(CWidget(), "Thong ke")
    mainTab.addTab(CWidget(), "Reversed")
    mainTab.addTab(CWidget(), "Reversed")
    #layout = QGridLayout()
    #layout.addWidget(self.createNavigationBar(), 0, 0)
    #layout.addWidget(OrderWindow(), 0, 1)
    #layout.setColumnStretch(0, 1)
    #layout.setColumnStretch(1, 7)
    #layout.setSpacing(0)
    #layout.setContentsMargins(0, 0, 0, 0)
    #container = QWidget()
    #container.setLayout(layout)
    self.setCentralWidget(mainTab)

  def createNavigationBar(self):
    layout = QVBoxLayout()
    label = QLabel()
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setText("Bán hàng")
    layout.addWidget(label)
    label = QLabel()
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setText("Mua hàng")
    layout.addWidget(label)
    label = QLabel()
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setText("Thống kê")
    layout.addWidget(label)
    label = QLabel()
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setText("Reversed")
    layout.addWidget(label)
    label = QLabel()
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setText("Reversed")
    layout.addWidget(label)
    widget = CWidget()
    widget.setLayout(layout)
    return widget

