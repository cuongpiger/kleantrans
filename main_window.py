from PyQt6.QtWidgets import \
    QMainWindow, QCheckBox, QToolBar, QLabel, QStatusBar, QVBoxLayout, QHBoxLayout, \
    QPlainTextEdit, QPushButton, QSpacerItem, QSizePolicy, QWidget, QDialog
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QKeySequence

from config import Config
from mouse_listener import MouseListener
from keyboard_listener import KeyboardListener
from dialog import Dialog, CustomDialog
from translator import Translator, TranslatedText


class MainWindow(QMainWindow):
    def __init__(self, config: Config, translator: Translator):
        super().__init__()
        self.config = config
        self.translator = translator
        self.raw_text = None
        self.for_text = None
        self.window_pos = (self.pos().x(), self.pos().y())

        self._setup_listeners(self.translator)

        self.setWindowIcon(self.config.images['icon'])
        self.setWindowTitle("KleanTrans")
        self.setGeometry(660, 340, 600, 400)
        self._toolbar_setup()
        self._widgets_setup()
        self._setup_dialogs()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)  # Always on top
        self._setup_hotkeys()

        self._set_post_show()

    def _toolbar_setup(self):
        btn_config = QAction(self.config.images['notebook'], 'Configure', self)
        btn_config.setStatusTip('Configure the characters used to clean text.')
        # btn_config.triggered.connect(self.show_config_window)

        self.chb_active = QCheckBox('Active')
        self.chb_active.setStatusTip('Press Ctrl+T to switch text translation from clipboard on or off.')

        chb_hide = QCheckBox('Hide')
        chb_hide.setStatusTip('Hide the top text box.')
        chb_hide.clicked.connect(self._checkbox_hide_clicked)
        chb_hide.setChecked(self.config.config["hide"])

        toolbar = QToolBar()
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        # toolbar.addSeparator()
        # toolbar.addWidget(self.chb_active)
        toolbar.addSeparator()
        toolbar.addWidget(chb_hide)
        toolbar.addSeparator()
        toolbar.addSeparator()
        toolbar.addWidget(QLabel("Copyright © by Cuong. Duong Manh"))

        self.addToolBar(toolbar)
        self.setStatusBar(QStatusBar(self))

    def _setup_listeners(self, translator: Translator):
        self.mouse_listener = MouseListener(translator)
        self.mouse_listener.raw_text_signal.connect(self._set_raw_text)

        self.keyboard_listener = KeyboardListener(translator)
        self.keyboard_listener.raw_text_signal.connect(self._set_raw_text)
        self.keyboard_listener.hide_window_signal.connect(self._hide_window)

    def _setup_hotkeys(self):
        pass

    def _checkbox_hide_clicked(self, checked):
        self._hide_raw_text(checked)
        self.config.config["hide"] = not self.config.config["hide"]
        self.config.save_config()

    def _widgets_setup(self):
        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()

        self.raw_text = QPlainTextEdit()
        layout.addWidget(self.raw_text)

        self.for_text = QPlainTextEdit()
        layout.addWidget(self.for_text)

        btn_trans = QPushButton('Translate')
        btn_trans.setIcon(self.config.images['arrow'])
        btn_trans.setStyleSheet('background-color: green')
        btn_trans.setStatusTip('Press combination key Ctrl+Enter to translate.')
        btn_clear = QPushButton('Clear')
        btn_clear.setIcon(self.config.images['cross'])
        btn_clear.setStyleSheet('background-color: red')
        btn_clear.setStatusTip('Press combination key Ctrl+D to clear.')

        btn_layout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        btn_layout.addWidget(btn_trans)
        btn_layout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        btn_layout.addWidget(btn_clear)
        btn_layout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # layout.addLayout(btn_layout) l
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def _set_raw_text(self, translated_text: TranslatedText):
        if self.raw_text is not None:
            self.raw_text.setPlainText(translated_text.raw_text)

        if self.for_text is not None:
            self.for_text.setPlainText(translated_text.translated_text)

    def _hide_window(self, show: bool):
        if show:
            self.move(self.window_pos[0], self.window_pos[1])
            self.show()
        else:
            self.window_pos = (self.pos().x(), self.pos().y())
            self.hide()

    def _setup_dialogs(self):
        self.dialog = CustomDialog()
        self.translator.dialog_signal.connect(self._show_dialog)

    def _show_dialog(self, dialog: Dialog):
        print(dialog.text)
        self.dialog.set_message(dialog)
        self.dialog.setFixedSize(250, 70)
        self.dialog.exec()

    def _hide_raw_text(self, checked: bool):
        if self.raw_text is not None:
            if checked:
                self.resize(600, 250)
                self.raw_text.hide()
            else:
                self.resize(600, 400)
                self.raw_text.show()

    def _set_post_show(self):
        self._hide_raw_text(self.config.config["hide"])
