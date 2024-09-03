from PyQt6.QtWidgets import \
    QDialog, QDialogButtonBox, QVBoxLayout, QLabel


class Dialog:
    def __init__(self, title, text):
        self._title = title
        self._text = text

    @property
    def title(self):
        return self._title

    @property
    def text(self):
        return self._text


class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.dialog = None

        self.setWindowTitle("")
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.layout = QVBoxLayout()
        self.message = QLabel("")
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def set_message(self, dialog: Dialog):
        self.setWindowTitle(dialog.title)
        self.message.setText(dialog.text)
