from PySide6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QCalendarWidget,
    QVBoxLayout, QPushButton, QDialog
)
from PySide6.QtCore import QDate
import sys

class CalendarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select a Date")
        self.resize(300, 250)

        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)

        select_button = QPushButton("Select Date")
        select_button.clicked.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.addWidget(self.calendar)
        layout.addWidget(select_button)

    def selected_date(self):
        return self.calendar.selectedDate()
