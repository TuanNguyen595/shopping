from controllers.controller import Controller
import signal   
import sys
# Allow Ctrl+C to interrupt the Qt event loop
signal.signal(signal.SIGINT, signal.SIG_DFL)

def main():
  controller = Controller()
  controller.run()

if __name__ == '__main__':
  main()
