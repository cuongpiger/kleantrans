import json
import os
from pathlib import Path

from PyQt6.QtGui import QIcon

CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


def _load_images():
    return {
        'icon': QIcon(os.path.join(CURRENT_DIRECTORY, "images", "icon.png")),
        'notebook': QIcon(os.path.join(CURRENT_DIRECTORY, "images", "notebook--pencil.png")),
        'document': QIcon(os.path.join(CURRENT_DIRECTORY, "images", "blue-document--plus.png")),
        'arrow': QIcon(os.path.join(CURRENT_DIRECTORY, "images", "arrow-turn-000-left.png")),
        'cross': QIcon(os.path.join(CURRENT_DIRECTORY, "images", "cross.png")),
        'swap': QIcon(os.path.join(CURRENT_DIRECTORY, "images", "swap.png")),
        'exit': QIcon(os.path.join(CURRENT_DIRECTORY, "images", "exit.png")),
        'window': QIcon(os.path.join(CURRENT_DIRECTORY, "images", "window.png")),
        'highlight': QIcon(os.path.join(CURRENT_DIRECTORY, "images", "highlighter-text.png")),
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
