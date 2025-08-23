from PySide6.QtCore import QObject, Signal, Slot
from pynput import keyboard
from serial import Serial, SerialException
import threading
class ScannerListenner(QObject):
  scannerResultEmiter = Signal(str)
  def __init__(self, port, baudrate=115200):
    super().__init__()
    self.port = port
    self.baudrate = baudrate 
    self._stop_event = threading.Event()
    self._thread = None
    self._ser = None
    self.buffer = ''
    pass

  @Slot(str)
  def onScannerResult(self, text):
    self.scannerResultEmiter.emit(text)
    pass

  def _listen(self):
    try:
      self._ser = Serial(self.port, self.baudrate, timeout=0.01)
      print(f"Listening on {self.port} at {self.baudrate} baud...")
      while not self._stop_event.is_set():
        if self._ser.readable():
          #line = self._ser.readline()
          line = self._ser.readline().decode(errors='ignore').strip()
          import re
          barcode = re.match(r'^\d+', line)
          if barcode:
            self.onScannerResult(barcode.group(0))
    except SerialException as e:
      print(f"Serial error: {e}")
    finally:
      if self._ser and self._ser.is_open:
        self._ser.close()
      print("Serial listener stopped.")

  def start(self):
    """Start listening in a background thread."""
    self._stop_event.clear()
    self._thread = threading.Thread(target=self._listen, daemon=True)
    self._thread.start()

  def stop(self):
    """Stop listening and close the serial port."""
    self._stop_event.set()
    if self._thread:
      self._thread.join()
