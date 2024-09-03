from PyQt6.QtWidgets import \
    QMainWindow, QCheckBox, QToolBar, QLabel, QStatusBar, QVBoxLayout, QHBoxLayout, \
    QPlainTextEdit, QPushButton, QSpacerItem, QSizePolicy, QWidget
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QKeySequence, QShortcut

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

        self._setup_listeners()

        self.setWindowIcon(self.images['icon'])
        self.setWindowTitle("KleanTrans")
        self.setGeometry(660, 340, 600, 400)

        self._setup_toolbar()
        self._widgets_setup()
        self._setup_dialogs()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)  # Always on top
        self._configure_hotkeys()

        self._set_post_show()

    def _setup_toolbar(self):
        btn_config = QAction(self.images['notebook'], 'Configure', self)
        btn_config.setStatusTip('Configure the characters used to clean text.')
        # btn_config.triggered.connect(self.show_config_window)

        toolbar = QToolBar()
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        toolbar.setIconSize(QSize(16, 16))

        self._configure_capture_checkbox(toolbar)

        chb_hide = QCheckBox('Hide')
        chb_hide.setStatusTip('Hide the top text box.')
        chb_hide.clicked.connect(self._checkbox_hide_clicked)  # noqa
        chb_hide.setChecked(self._main_window_appear())

        self._configure_swap_button(toolbar)

        # toolbar.addSeparator()
        # toolbar.addWidget(self.chb_active)
        toolbar.addWidget(chb_hide)
        toolbar.addSeparator()
        toolbar.addSeparator()
        toolbar.addWidget(QLabel("Copyright © by Cuong. Duong Manh"))

        self.addToolBar(toolbar)
        self.setStatusBar(QStatusBar(self))

    def _setup_listeners(self):
        def set_raw_text(translated_text: TranslatedText):
            if self.raw_text is not None:
                self.raw_text.setPlainText(translated_text.raw_text)

            if self.for_text is not None:
                self.for_text.setPlainText(translated_text.translated_text)

        self.mouse_listener = MouseListener(self.translator, self.config)
        self.mouse_listener.raw_text_signal.connect(set_raw_text)

        self.keyboard_listener = KeyboardListener(self.translator, self.config)
        self.keyboard_listener.raw_text_signal.connect(set_raw_text)
        self.keyboard_listener.hide_window_signal.connect(self._hide_window)

    def _configure_capture_checkbox(self, toolbar: QToolBar):
        def connect_capture_checkbox(checked: bool):
            self._switch_capture_feature()
            self.config.save_config()

        self.chb_active = QCheckBox('Capture')
        self.chb_active.setStatusTip('Press Ctrl+T to turn ON/OFF translating from text capture.')
        self.chb_active.clicked.connect(connect_capture_checkbox)  # noqa
        self.chb_active.setChecked(self._capture_text_appear())

        # Add this widget into the toolbar layout
        toolbar.addWidget(self.chb_active)
        toolbar.addSeparator()

    def _configure_swap_button(self, toolbar: QToolBar):
        def _connect_swap_button():
            self.system_config['swap'] = [self.system_config['swap'][1], self.system_config['swap'][0]]
            self.btn_swap.setText(f"{self.system_config['swap'][0]} ➜ {self.system_config['swap'][1]}")
            self.raw_text.setPlainText("")
            self.config.save_config()

        self.btn_swap = QAction(
            self.images['swap'],
            f"{self.system_config['swap'][0]} ➜ {self.system_config['swap'][1]}", self)

        self.btn_swap.setStatusTip('Press Ctrl+W to swap two languages.')
        self.btn_swap.setShortcut(QKeySequence('Ctrl+w'))

        # Setup trigger
        self.btn_swap.triggered.connect(_connect_swap_button)  # noqa

        # Add this widget into the toolbar layout
        toolbar.addAction(self.btn_swap)
        toolbar.addSeparator()

    def _configure_hotkeys(self):
        def translate():
            clean_text = self.raw_text.toPlainText().strip()
            if not self.translator.ignore_clean_this_lang(self.config.source_lang):
                clean_text = self.translator.clean_text(clean_text)

            translated_text = self.translator.translate(clean_text, self.config.source_lang,
                                                        self.config.target_lang)
            self.raw_text.setPlainText(clean_text)
            self.for_text.setPlainText(translated_text)

        def clear():
            self.raw_text.setPlainText('')
            self.for_text.setPlainText('')

        def active():
            pass

        btn_trans_shortcut = QShortcut(QKeySequence('Ctrl+Return'), self)
        btn_trans_shortcut.activated.connect(translate)  # noqa

        btn_clear_shortcut = QShortcut(QKeySequence('Ctrl+d'), self)
        btn_clear_shortcut.activated.connect(clear)  # noqa

        chb_active_shortcut = QShortcut(QKeySequence('Ctrl+t'), self)
        chb_active_shortcut.activated.connect(active)  # noqa

    def _checkbox_hide_clicked(self, checked):
        self._hide_raw_text(checked)
        self._main_window_switch()
        self.config.save_config()

    def _widgets_setup(self):
        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()

        self.raw_text = QPlainTextEdit()
        layout.addWidget(self.raw_text)

        self.for_text = QPlainTextEdit()
        layout.addWidget(self.for_text)

        btn_trans = QPushButton('Translate')
        btn_trans.setIcon(self.images['arrow'])
        btn_trans.setStyleSheet('background-color: green')
        btn_trans.setStatusTip('Press combination key Ctrl+Enter to translate.')
        btn_clear = QPushButton('Clear')
        btn_clear.setIcon(self.images['cross'])
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
        self._hide_raw_text(self.system_config["hide"])

    @property
    def images(self):
        return self.config.images

    @property
    def system_config(self):
        return self.config.system_config

    def _main_window_appear(self) -> bool:
        return self.system_config["hide"]

    def _main_window_switch(self):
        self.system_config["hide"] = not self.system_config["hide"]

    def _capture_text_appear(self) -> bool:
        return self.system_config["active"]

    def _switch_capture_feature(self):
        self.system_config["active"] = not self.system_config["active"]
