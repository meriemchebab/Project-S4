import sys
from PySide6.QtWidgets import QApplication
from controller import Controler
from welcomepage import SplashScreen

def main():
    app = QApplication(sys.argv)
    controller = None

    def show_main():
        nonlocal controller
        controller = Controler()
        controller.ui.show()

    splash = SplashScreen(on_finish=show_main)
    splash.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
