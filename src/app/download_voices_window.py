from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QTableWidgetItem,
    QProgressDialog,
    QMessageBox,
    QHeaderView,
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

from app.ui.ui_download_voices import Ui_Form
from app.workers import VoiceListFetcherThread, VoiceDownloaderThread
from utils.voice_manager import is_voice_installed


class DownloadVoicesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.voices_data = {}

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(1.0)

        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.ui.exitButton.clicked.connect(self.close)
        self.ui.comboBox.currentIndexChanged.connect(self._filter_table)

        self._fetch_voices_list()

    def _fetch_voices_list(self):
        self.ui.comboBox.addItem("Loading voices...")
        self.ui.comboBox.setEnabled(False)
        self.ui.tableWidget.setEnabled(False)

        self.fetcher_thread = VoiceListFetcherThread()
        self.fetcher_thread.finished_fetch.connect(self._on_fetch_success)
        self.fetcher_thread.error_fetch.connect(self._on_fetch_error)
        self.fetcher_thread.start()

    def _on_fetch_success(self, data: dict):
        self.voices_data = data
        self.ui.comboBox.clear()
        self.ui.comboBox.setEnabled(True)
        self.ui.tableWidget.setEnabled(True)

        languages = set()
        for key, info in data.items():
            lang_name = info["language"]["name_english"]
            languages.add(lang_name)

        self.ui.comboBox.addItem("All Languages")
        for lang in sorted(languages):
            self.ui.comboBox.addItem(lang)

        self._populate_table()

    def _on_fetch_error(self, err: str):
        self.ui.comboBox.clear()
        self.ui.comboBox.addItem("Error loading voices")
        QMessageBox.critical(
            self, "Network Error", f"Failed to load voices list:\n{err}"
        )

    def _filter_table(self):
        self._populate_table()

    def _populate_table(self):
        self.ui.tableWidget.setRowCount(0)
        selected_lang = self.ui.comboBox.currentText()

        row = 0
        for key, info in self.voices_data.items():
            lang_info = info["language"]
            lang_name = lang_info["name_english"]

            if selected_lang != "All Languages" and lang_name != selected_lang:
                continue

            self.ui.tableWidget.insertRow(row)

            self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(lang_name))
            self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(info["name"]))
            self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(info["quality"]))

            family = lang_info.get("family", "")
            code = lang_info.get("code", "")
            name = info.get("name", "")
            quality = info.get("quality", "")

            sample_url = f"https://rhasspy.github.io/piper-samples/samples/{family}/{code}/{name}/{quality}/speaker_0.mp3"

            btn_sample = QPushButton("Play Sample")
            btn_sample.clicked.connect(
                lambda checked, url=sample_url: self._play_sample(url)
            )
            self.ui.tableWidget.setCellWidget(row, 3, btn_sample)

            btn_download = QPushButton()
            if is_voice_installed(key):
                btn_download.setText("Installed")
                btn_download.setEnabled(False)
            else:
                btn_download.setText("Download")
                btn_download.clicked.connect(
                    lambda checked, k=key, f=info["files"]: self._start_download(k, f)
                )

            self.ui.tableWidget.setCellWidget(row, 4, btn_download)
            row += 1

    def _play_sample(self, url: str):
        self.player.setSource(QUrl(url))
        self.player.play()

    def _start_download(self, voice_key: str, files_dict: dict):
        self.progress_dialog = QProgressDialog(
            f"Downloading {voice_key}...", "Cancel", 0, 100, self
        )
        self.progress_dialog.setWindowTitle("Downloading Voice")
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.setAutoReset(True)

        self.downloader_thread = VoiceDownloaderThread(voice_key, files_dict)
        self.downloader_thread.progress_updated.connect(self.progress_dialog.setValue)
        self.downloader_thread.finished_download.connect(self._on_download_success)
        self.downloader_thread.error_download.connect(self._on_download_error)

        self.progress_dialog.canceled.connect(self.downloader_thread.terminate)

        self.downloader_thread.start()
        self.progress_dialog.show()

    def _on_download_success(self, voice_key: str):
        self.progress_dialog.setValue(100)
        QMessageBox.information(
            self, "Success", f"Voice '{voice_key}' downloaded successfully!"
        )
        self._populate_table()

    def _on_download_error(self, err: str):
        self.progress_dialog.cancel()
        QMessageBox.critical(
            self, "Download Error", f"Failed to download voice:\n{err}"
        )
