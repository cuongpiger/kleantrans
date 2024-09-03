import sys
import os

from PyQt6.QtWidgets import QApplication

from .main_window import MainWindow
from .translator import Translator
from .config import Config


def _init_kleantrans_directory():
    import json
    from pathlib import Path

    # Get the home directory of the user
    home_dir = Path.home()

    # Define the path for the .kleantrans directory
    kleantrans_dir = home_dir / ".kleantrans"

    # Check if the directory exists, and if not, create it
    if not kleantrans_dir.exists():
        kleantrans_dir.mkdir(parents=True)
        path = f"{kleantrans_dir}/config.json"
        data = {
            "swap": ["en", "vi"],
            "active": True,
            "hide": False
        }
        with open(path, 'w', encoding='utf-8') as wt:
            json.dump(data, wt)


def run():
    try:
        # First fork
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Exit first parent

    except OSError as e:
        sys.stderr.write(f"Fork #1 failed: {e.strerror}\n")
        sys.exit(1)

    # Decouple from parent environment
    os.chdir("/")
    os.setsid()
    os.umask(0)

    try:
        # Second fork
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Exit second parent

    except OSError as e:
        sys.stderr.write(f"Fork #2 failed: {e.strerror}\n")
        sys.exit(1)

    _init_kleantrans_directory()

    translator = Translator()

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setStyle('Fusion')

    config = Config()
    MainWindow(app, config, translator)

    app.exec()

# if __name__ == '__main__':
#     sys.exit(run())
