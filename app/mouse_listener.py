import os
import pyperclip

from PyQt6.QtCore import pyqtSignal, QObject

from pynput import mouse

from .translator import Translator, TranslatedText
from .config import Config


class MouseListener(QObject):
    raw_text_signal = pyqtSignal(TranslatedText)

    def __init__(self, translator: Translator, system_config: Config):
        super().__init__()
        self.translator = translator
        self.system_config = system_config
        self.mouse = mouse.Listener(on_click=self._on_click)
        self.mouse.start()

    def _on_click(self, x, y, button: mouse.Button, pressed: bool):  # noqa
        if self.system_config.active_capture_text and button == mouse.Button.middle and pressed:
            os.system("xclip -out -selection primary | xclip -in -selection clipboard")

            text = self.translator.clean_text(pyperclip.paste())
            trans_text = self.translator.translate(text, self.system_config.source_lang, self.system_config.target_lang)

            self.raw_text_signal.emit(TranslatedText(text, trans_text))  # noqa
