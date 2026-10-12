"""Punto de entrada: python3 -m pm3gui"""

import sys

from PyQt5.QtWidgets import QApplication

from .mainwindow import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Proxmark3 Easy GUI")
    app.setApplicationDisplayName("Proxmark3 Easy GUI")
    win = MainWindow()
    win.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
