from PySide6.QtWidgets import QWidget
from app.ui.ui_help import Ui_HelpWindow


class HelpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_HelpWindow()
        self.ui.setupUi(self)
