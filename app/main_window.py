from PyQt6.QtWidgets import \
    QMainWindow, QCheckBox, QToolBar, QLabel, QStatusBar, QVBoxLayout, \
    QPlainTextEdit, QWidget, QMenu, QSystemTrayIcon, QApplication
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QKeySequence, QShortcut

from .config import Config
from .mouse_listener import MouseListener
from .keyboard_listener import KeyboardListener
from .dialog import Dialog, CustomDialog
from .translator import Translator, TranslatedText


class MainWindow(QMainWindow):
    def __init__(self, app: QApplication, config: Config, translator: Translator):
        super().__init__()
        self.app = app
        self.config = config
        self.translator = translator
        self.raw_text = None
        self.for_text = None
        self.window_pos = (self.pos().x(), self.pos().y())

        self.setWindowIcon(self.images['icon'])
        self.setWindowTitle("KleanTrans")
        self.setGeometry(660, 340, 600, 400)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)  # Always on top

        self._setup_listeners()
        self._setup_toolbar()
        self._setup_widgets()
        self._setup_dialogs()
        self._setup_hotkeys()
        self._setup_tray()

        self._setup_post_main_window()

    def _setup_listeners(self):
        def set_raw_text(translated_text: TranslatedText):
            if self.raw_text is not None:
                self.raw_text.setPlainText(translated_text.raw_text)

            if self.for_text is not None:
                self.for_text.setPlainText(translated_text.translated_text)

        def hide_window(show: bool):
            if show:
                self.move(self.window_pos[0], self.window_pos[1])
                self.show()
            else:
                self.window_pos = (self.pos().x(), self.pos().y())
                self.hide()

        self.mouse_listener = MouseListener(self.translator, self.config)
        self.mouse_listener.raw_text_signal.connect(set_raw_text)

        self.keyboard_listener = KeyboardListener(self.translator, self.config)
        self.keyboard_listener.raw_text_signal.connect(set_raw_text)
        self.keyboard_listener.hide_window_signal.connect(hide_window)

    def _setup_toolbar(self):
        btn_config = QAction(self.images['notebook'], 'Configure', self)
        btn_config.setStatusTip('Configure the characters used to clean text.')
        # btn_config.triggered.connect(self.show_config_window)

        toolbar = QToolBar()
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        toolbar.setIconSize(QSize(16, 16))

        self._configure_capture_checkbox(toolbar)
        self._configure_swap_button(toolbar)
        self._configure_checkbox_hide(toolbar)
        toolbar.addWidget(QLabel("Copyright © by Cuong. Duong Manh"))

        self.addToolBar(toolbar)
        self.setStatusBar(QStatusBar(self))

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
        def connect_swap_button():
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
        self.btn_swap.triggered.connect(connect_swap_button)  # noqa

        # Add this widget into the toolbar layout
        toolbar.addAction(self.btn_swap)
        toolbar.addSeparator()

    def _configure_checkbox_hide(self, toolbar: QToolBar):
        def connect_hide_checkbox(checked):
            self._hide_raw_text(checked)
            self._main_window_switch()
            self.config.save_config()

        self.chb_hide = QCheckBox('Hide')
        self.chb_hide.setStatusTip('Hide the top text box.')
        self.chb_hide.clicked.connect(connect_hide_checkbox)  # noqa
        self.chb_hide.setChecked(self._main_window_appear())

        toolbar.addWidget(self.chb_hide)
        toolbar.addSeparator()

    def _setup_hotkeys(self):
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
            self._switch_capture_feature()
            self.chb_active.setChecked(self._capture_text_appear())

        btn_trans_shortcut = QShortcut(QKeySequence('Ctrl+Return'), self)
        btn_trans_shortcut.activated.connect(translate)  # noqa

        btn_clear_shortcut = QShortcut(QKeySequence('Ctrl+d'), self)
        btn_clear_shortcut.activated.connect(clear)  # noqa

        chb_active_shortcut = QShortcut(QKeySequence('Ctrl+t'), self)
        chb_active_shortcut.activated.connect(active)  # noqa

    def _setup_tray(self):
        def connect_capture_checkbox():
            self._switch_capture_feature()

            capture_text_inside = "Enable Capture"
            if self.config.active_capture_text:
                capture_text_inside = "Disable Capture"

            self.capture_action.setText(capture_text_inside)
            self.chb_active.setChecked(self._capture_text_appear())
            self.config.save_config()

        capture_text = "Enable Capture"
        if self.config.active_capture_text:
            capture_text = "Disable Capture"

        self.show_action = QAction(self.images['window'], 'Show')
        self.show_action.triggered.connect(self.show)  # noqa
        self.quit_action = QAction(self.images['exit'], 'Quit')
        self.quit_action.triggered.connect(self.app.quit)  # noqa
        self.capture_action = QAction(self.images['highlight'], capture_text)
        self.capture_action.triggered.connect(connect_capture_checkbox)  # noqa

        self.menu = QMenu()
        self.menu.addAction(self.show_action)
        self.menu.addAction(self.capture_action)
        self.menu.addAction(self.quit_action)

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.images['icon'])
        self.tray.setVisible(True)
        self.tray.setContextMenu(self.menu)
        self.tray.show()

    def _setup_widgets(self):
        layout = QVBoxLayout()

        self.raw_text = QPlainTextEdit()
        layout.addWidget(self.raw_text)

        self.for_text = QPlainTextEdit()
        layout.addWidget(self.for_text)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def _setup_dialogs(self):
        def show_dialog(dialog: Dialog):
            self.dialog.set_message(dialog)
            self.dialog.setFixedSize(250, 70)
            self.dialog.exec()

        self.dialog = CustomDialog()
        self.translator.dialog_signal.connect(show_dialog)

    def _setup_post_main_window(self):
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

    def _hide_raw_text(self, checked: bool):
        if self.raw_text is not None:
            if checked:
                self.resize(600, 250)
                self.raw_text.hide()
            else:
                self.resize(600, 400)
                self.raw_text.show()
