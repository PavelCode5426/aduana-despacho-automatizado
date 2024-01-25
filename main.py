import sys

from PyQt6.QtWidgets import QApplication

from config import init_config
from views.MainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    init_config()
    window = MainWindow()
    sys.exit(app.exec())