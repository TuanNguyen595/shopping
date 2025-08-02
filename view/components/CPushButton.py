from PySide6.QtWidgets import QPushButton

class CPushButton(QPushButton):
  def __init__(self, text, parent=None):
    super().__init__(text, parent);
    self.setStyleSheet("""
      QPushButton {
        background-color: #3498db;
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px;
        border-radius: 6px;
      }
      QPushButton:hover {
        background-color: #2980b9;
      }
      QPushButton:pressed {
        background-color: #1e8449;
      }
    """)
