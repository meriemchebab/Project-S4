import sys
from PySide6.QtWidgets import QApplication
from controller import Controler

def main():
    app = QApplication(sys.argv)
    controller = Controler()
    controller.ui.show()  # Show the main window
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
