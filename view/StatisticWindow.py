from PySide6.QtWidgets import (
  QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
  QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QSplitter, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from i18n import t
import datetime


class StatisticWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.db = None
    self._build_ui()

  def _build_ui(self):
    outer = QVBoxLayout(self)
    outer.setSpacing(10)

    # ── Top bar: year selector + refresh ─────────────────────────────
    top = QHBoxLayout()
    self.year_label = QLabel(t("stat_year_label"))
    self.year_combo = QComboBox()
    current_year = datetime.datetime.now().year
    for y in range(current_year, current_year - 10, -1):
      self.year_combo.addItem(str(y), y)
    self.refresh_btn = QPushButton(t("stat_refresh_btn"))
    self.refresh_btn.clicked.connect(self.load)
    top.addWidget(self.year_label)
    top.addWidget(self.year_combo)
    top.addStretch()
    top.addWidget(self.refresh_btn)
    outer.addLayout(top)

    # ── Splitter: monthly table (top) + daily chart (bottom) ─────────
    splitter = QSplitter(Qt.Orientation.Vertical)

    # Monthly table
    self.table = QTableWidget(13, 4)   # 12 months + 1 total row
    self.table.setHorizontalHeaderLabels([
      t("stat_col_month"), t("stat_col_revenue"),
      t("stat_col_cost"),  t("stat_col_profit")
    ])
    self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    self.table.verticalHeader().setVisible(False)
    self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    self.table.cellClicked.connect(self._onMonthClicked)
    splitter.addWidget(self.table)

    # Daily bar chart
    self._bar_set = QBarSet(t("stat_daily_orders_label"))
    self._bar_series = QBarSeries()
    self._bar_series.append(self._bar_set)

    self._chart = QChart()
    self._chart.addSeries(self._bar_series)
    self._chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

    self._axis_x = QBarCategoryAxis()
    self._chart.addAxis(self._axis_x, Qt.AlignmentFlag.AlignBottom)
    self._bar_series.attachAxis(self._axis_x)

    self._axis_y = QValueAxis()
    self._axis_y.setLabelFormat("%d")
    self._chart.addAxis(self._axis_y, Qt.AlignmentFlag.AlignLeft)
    self._bar_series.attachAxis(self._axis_y)

    self._chart_title_tpl = t("stat_daily_chart_title")
    self._chart.setTitle("")

    self._chart_view = QChartView(self._chart)
    self._chart_view.setVisible(False)
    self._chart_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    splitter.addWidget(self._chart_view)

    splitter.setStretchFactor(0, 1)
    splitter.setStretchFactor(1, 1)
    outer.addWidget(splitter)

  def setDatabase(self, db):
    self.db = db
    years = self.db.getOrderYears()
    if years:
      self.year_combo.clear()
      for y in years:
        self.year_combo.addItem(str(y), y)
    self.load()

  def load(self):
    if self.db is None:
      return
    year = self.year_combo.currentData()
    if year is None:
      return
    rows = self.db.getMonthlyStats(year)
    month_names = [
      t("month_jan"), t("month_feb"), t("month_mar"),
      t("month_apr"), t("month_may"), t("month_jun"),
      t("month_jul"), t("month_aug"), t("month_sep"),
      t("month_oct"), t("month_nov"), t("month_dec"),
    ]
    total_rev = total_cost = total_profit = 0
    for i, (month, revenue, cost, profit) in enumerate(rows):
      total_rev    += revenue
      total_cost   += cost
      total_profit += profit
      self._set_row(i, month_names[month - 1], revenue, cost, profit,
                    bold=False, bg=None)
    self._set_row(12, t("stat_total_row"), total_rev, total_cost, total_profit,
                  bold=True, bg=QColor("#e8f4e8"))
    self.table.resizeRowsToContents()
    self._chart_view.setVisible(False)

  def _onMonthClicked(self, row, col):
    if row == 12 or self.db is None:   # ignore total row
      return
    year = self.year_combo.currentData()
    month = row + 1  # rows 0-11 → months 1-12
    daily = self.db.getDailyOrderCounts(year, month)

    self._bar_set.remove(0, self._bar_set.count())
    self._axis_x.clear()

    labels = [str(d) for d, _ in daily]
    counts = [c for _, c in daily]
    for c in counts:
      self._bar_set.append(c)
    self._axis_x.append(labels)
    max_count = max(counts) if counts else 1
    self._axis_y.setRange(0, max(max_count + 1, 5))

    month_names = [
      t("month_jan"), t("month_feb"), t("month_mar"),
      t("month_apr"), t("month_may"), t("month_jun"),
      t("month_jul"), t("month_aug"), t("month_sep"),
      t("month_oct"), t("month_nov"), t("month_dec"),
    ]
    self._chart.setTitle(t("stat_daily_chart_title").format(
      month=month_names[month - 1], year=year))
    self._bar_set.setLabel(t("stat_daily_orders_label"))
    self._chart_view.setVisible(True)

  def _set_row(self, row, label, revenue, cost, profit, bold, bg):
    items = [
      QTableWidgetItem(label),
      QTableWidgetItem(f"{revenue:,}"),
      QTableWidgetItem(f"{cost:,}"),
      QTableWidgetItem(f"{profit:,}"),
    ]
    for col, item in enumerate(items):
      item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
      if bold:
        item.setFont(QFont("", -1, QFont.Weight.Bold))
      if bg:
        item.setBackground(bg)
      if col == 3 and profit < 0:
        item.setForeground(QColor("red"))
      elif col == 3:
        item.setForeground(QColor("green"))
      self.table.setItem(row, col, item)

  def retranslate(self):
    self.year_label.setText(t("stat_year_label"))
    self.refresh_btn.setText(t("stat_refresh_btn"))
    self.table.setHorizontalHeaderLabels([
      t("stat_col_month"), t("stat_col_revenue"),
      t("stat_col_cost"),  t("stat_col_profit")
    ])
    self._bar_set.setLabel(t("stat_daily_orders_label"))
    self.load()
