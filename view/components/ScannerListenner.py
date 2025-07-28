from PySide6.QtCore import QObject, Signal, Slot
class ScannerListenner(QObject):
  scannerResultEmiter = Signal(str)
  def __init__(self):
    super().__init__()
    pass

  @Slot(str)
  def onScannerResult(self, text):
    self.scannerResultEmiter.emit(text)
    pass
