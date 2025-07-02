from PySide6.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QLabel
import random

class CWidget(QWidget):
  def __init__(self):
    super().__init__()
    #self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    # Generate random RGB color
    r = random.randint(100, 255)
    g = random.randint(100, 255)
    b = random.randint(100, 255)
    color = f"rgb({r}, {g}, {b})"
    
    # Apply background and border using stylesheet
    self.setStyleSheet(f"""
        background-color: {color};
        border: 1px solid black;
    """)
    #layout = QVBoxLayout()
    #label = QLabel()
    #layout.addWidget(label)
    #self.setLayout(layout)

