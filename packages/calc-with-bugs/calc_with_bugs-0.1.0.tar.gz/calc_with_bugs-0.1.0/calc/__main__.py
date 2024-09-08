import sys
from PyQt6.QtWidgets import QApplication

from calc.app import CalcController
from calc.window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    controller = CalcController()
    main_window = MainWindow(controller)
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
