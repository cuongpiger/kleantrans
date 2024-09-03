import sys

from PyQt6.QtWidgets import QApplication

from main_window import MainWindow
from translator import Translator
from config import Config


def run():
    translator = Translator()

    app = QApplication(sys.argv)

    config = Config()
    window = MainWindow(config, translator)
    window.show()

    app.exec()


run()
