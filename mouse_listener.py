import os
import pyperclip

from PyQt6.QtCore import pyqtSignal, QObject

from pynput import mouse

from translator import Translator, TranslatedText


class MouseListener(QObject):
    raw_text_signal = pyqtSignal(TranslatedText)

    def __init__(self, translator: Translator):
        super().__init__()
        self.translator = translator
        self.mouse = mouse.Listener(on_click=self._on_click)
        self.mouse.start()

    def _on_click(self, x, y, button: mouse.Button, pressed: bool):  # noqa
        if button == mouse.Button.middle and pressed:
            os.system("xclip -out -selection primary | xclip -in -selection clipboard")
            text = self.translator.clean_text(pyperclip.paste())
            trans_text = self.translator.translate(text, "en", "vi")

            self.raw_text_signal.emit(TranslatedText(text, trans_text))
