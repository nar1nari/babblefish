from PySide6.QtWidgets import QWidget
from app.ui.ui_about import Ui_AboutForm


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AboutForm()
        self.ui.setupUi(self)
