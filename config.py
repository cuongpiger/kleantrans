from PyQt6.QtGui import QIcon


def _load_images():
    return {
        'icon': QIcon('images/icon.png'),
        'notebook': QIcon('images/notebook--pencil.png'),
        'document': QIcon('images/blue-document--plus.png'),
        'arrow': QIcon('images/arrow-turn-000-left.png'),
        'cross': QIcon('images/cross.png'),
        'swap': QIcon('images/swap.png'),
        'exit': QIcon('images/exit.png'),
        'window': QIcon('images/window.png')
    }


class Config:
    def __init__(self):
        self.images = _load_images()
