import json
from pathlib import Path

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
        'window': QIcon('images/window.png'),
        'highlight': QIcon('images/highlighter-text.png')
    }


class Config:
    def __init__(self):
        self.images = _load_images()
        self.system_config = self._load_config()

    def _load_config(self):  # noqa
        path = Path.home() / ".kleantrans/config.json"
        with open(path, encoding='utf-8') as rd:
            config = json.load(rd)
            return config

    def save_config(self):
        path = Path.home() / ".kleantrans/config.json"
        with open(path, 'w', encoding='utf-8') as wt:
            json.dump(self.system_config, wt)

    @property
    def source_lang(self):
        return self.system_config["swap"][0]

    @property
    def target_lang(self):
        return self.system_config["swap"][1]

    @property
    def active_capture_text(self):
        return self.system_config["active"]

