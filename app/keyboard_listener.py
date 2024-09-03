import os
import pyperclip

from PyQt6.QtCore import pyqtSignal, QObject
from pynput import keyboard

from .translator import Translator, TranslatedText
from .config import Config


class KeyboardListener(QObject):
    raw_text_signal = pyqtSignal(TranslatedText)
    hide_window_signal = pyqtSignal(bool)

    def __init__(self, translator: Translator, system_config: Config):
        super().__init__()
        self.translator = translator
        self.system_config = system_config
        self.switch = True

        self.window_combination = keyboard.HotKey(
            keyboard.HotKey.parse("<shift>+<cmd>"),
            self._on_active)
        self.translate_combination = keyboard.HotKey(
            keyboard.HotKey.parse("<ctrl>+<cmd>"),
            self._on_translate)

        self.window_combination_listener = keyboard.Listener(
            on_press=self._for_canonical(self.window_combination.press),
            on_release=self._for_canonical(self.window_combination.release))
        self.window_combination_listener.start()

        self.translate_combination_listener = keyboard.Listener(
            on_press=self._for_canonical(self.translate_combination.press),
            on_release=self._for_canonical(self.translate_combination.release))
        self.translate_combination_listener.start()

    def _on_active(self):
        if self.switch:
            self.hide_window_signal.emit(True)
        else:
            self.hide_window_signal.emit(False)

        self.switch = not self.switch

    def _on_translate(self):
        # If the screen is show and user turn on translating from capture text fearure
        if self.switch and self.system_config.active_capture_text:
            os.system("xclip -out -selection primary | xclip -in -selection clipboard")

            text = self.translator.clean_text(pyperclip.paste())
            trans_text = self.translator.translate(text, self.system_config.source_lang, self.system_config.target_lang)

            # Send signal to main_window.py
            self.raw_text_signal.emit(TranslatedText(text, trans_text))

    def _for_canonical(self, f):
        return lambda k: f(self.window_combination_listener.canonical(k))
