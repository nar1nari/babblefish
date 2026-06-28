from PySide6.QtCore import QSettings


class AppSettings:
    def __init__(self):
        self._settings = QSettings("BabbleFishOrg", "BabbleFish")

    def get_setting(self, key, default=None):
        return self._settings.value(key, default)

    def set_setting(self, key, value):
        self._settings.setValue(key, value)
