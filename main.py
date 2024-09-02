import sys

from PyQt6.QtWidgets import QApplication

from main_window import MainWindow
from translator import Translator
from config import Config
from mouse_listener import MouseListener


def run():
    translator = Translator()

    app = QApplication(sys.argv)

    config = Config()
    window = MainWindow(config)
    # Load the mouse listener here

    MouseListener(translator)

    window.show()

    app.exec()


run()
