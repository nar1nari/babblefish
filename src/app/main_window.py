from pathlib import Path
import queue

from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QLabel,
    QMainWindow,
    QProgressDialog,
)
from PySide6.QtCore import QTranslator, Qt
from PySide6.QtGui import QActionGroup, QAction

from app.about_window import AboutWindow
from app.download_voices_window import DownloadVoicesWindow
from app.help_window import HelpWindow
from app.settings import AppSettings
from app.ui.ui_main_window import Ui_MainWindow
from utils.audio_utils import get_audio_devices
from utils.languages import SUPPORTED_LANGUAGES
from utils.translation import is_translation_installed
from utils.voice_manager import get_installed_voices, get_voice_model_path
from utils.whisper import WHISPER_MODELS, is_model_downloaded
from app.workers import (
    PipelineDownloaderThread,
    AudioCaptureThread,
    ASRWorkerThread,
    TTSWorkerThread,
    TranslateWorkerThread,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.settings = AppSettings()
        self.translator = QTranslator(self)

        self.audio_queue: queue.Queue = queue.Queue()
        self.text_queue: queue.Queue = queue.Queue()
        self.tts_queue: queue.Queue = queue.Queue()

        self.capture_thread: AudioCaptureThread | None = None
        self.asr_thread: ASRWorkerThread | None = None
        self.translate_thread: TranslateWorkerThread | None = None
        self.tts_thread: TTSWorkerThread | None = None
        self.downloader_thread: PipelineDownloaderThread | None = None
        self.is_recording = False

        self.download_window: DownloadVoicesWindow | None = None
        self.help_window: HelpWindow | None = None
        self.about_window: AboutWindow | None = None
        self.ui.warningLabel.hide()

        self._populate_whisper_models()
        self._populate_audio_devices()
        self._populate_languages()
        self._populate_voices()
        self._setup_translation_menu()

        self._load_preferences()
        self._check_model_status()
        self._connect_signals()

    def _populate_whisper_models(self) -> None:
        self.ui.whisperComboBox.clear()
        for internal_name, display_name in WHISPER_MODELS.items():
            self.ui.whisperComboBox.addItem(display_name, userData=internal_name)

    def _populate_voices(self) -> None:
        self.ui.voiceComboBox.clear()
        installed_voices = get_installed_voices()

        if not installed_voices:
            self.ui.voiceComboBox.addItem("No voices installed", userData=None)
            self.ui.voiceComboBox.setEnabled(False)
        else:
            self.ui.voiceComboBox.setEnabled(True)
            for voice in installed_voices:
                self.ui.voiceComboBox.addItem(voice, userData=voice)

    def _populate_audio_devices(self) -> None:
        inputs, outputs = get_audio_devices()

        for combo in (self.ui.inputComboBox, self.ui.outputComboBox):
            combo.clear()

        for dev in inputs:
            self.ui.inputComboBox.addItem(dev["name"], userData=dev["id"])

        for dev in outputs:
            self.ui.outputComboBox.addItem(dev["name"], userData=dev["id"])

    def _populate_languages(self) -> None:
        self.ui.fromComboBox.clear()
        self.ui.toComboBox.clear()

        for code, name in sorted(SUPPORTED_LANGUAGES.items(), key=lambda item: item[1]):
            self.ui.fromComboBox.addItem(name, userData=code)
            self.ui.toComboBox.addItem(name, userData=code)

    def _setup_translation_menu(self):
        self.language_group = QActionGroup(self)
        self.language_group.setExclusive(True)

        self.actionEnglish = QAction("English", self, checkable=True)
        self.actionRussian = QAction("Русский", self, checkable=True)

        self.language_group.addAction(self.actionEnglish)
        self.language_group.addAction(self.actionRussian)

        self.ui.menuTranslation.addAction(self.actionEnglish)
        self.ui.menuTranslation.addAction(self.actionRussian)

        self.actionEnglish.triggered.connect(lambda: self.set_language("en"))
        self.actionRussian.triggered.connect(lambda: self.set_language("ru"))

    def set_language(self, language: str):
        app = QApplication.instance()

        app.removeTranslator(self.translator)

        if language == "ru":
            ok = self.translator.load(":/translations/babblefish_ru.qm")
            if not ok:
                print("WARNING: Failed to load translation file!")
                return
            app.installTranslator(self.translator)

        self.ui.retranslateUi(self)

        self.settings.set_setting("ui/language", language)

        self.actionEnglish.setChecked(language == "en")
        self.actionRussian.setChecked(language == "ru")

    def _load_preferences(self) -> None:
        self._set_combo_value(
            self.ui.whisperComboBox, self.settings.get_setting("whisper/model")
        )
        self._set_combo_value(
            self.ui.voiceComboBox, self.settings.get_setting("voice/model")
        )
        self._set_combo_value(
            self.ui.inputComboBox, self.settings.get_setting("audio/input_device")
        )
        self._set_combo_value(
            self.ui.outputComboBox, self.settings.get_setting("audio/output_device")
        )
        self._set_combo_value(
            self.ui.fromComboBox,
            self.settings.get_setting("translation/from_lang", "en"),
        )
        self._set_combo_value(
            self.ui.toComboBox, self.settings.get_setting("translation/to_lang", "es")
        )
        self.set_language(self.settings.get_setting("ui/language", "en"))

    def _save_preferences(self) -> None:
        self.settings.set_setting(
            "whisper/model", self.ui.whisperComboBox.currentData()
        )
        self.settings.set_setting("voice/model", self.ui.voiceComboBox.currentData())
        self.settings.set_setting(
            "audio/input_device", self.ui.inputComboBox.currentData()
        )
        self.settings.set_setting(
            "audio/output_device", self.ui.outputComboBox.currentData()
        )
        self.settings.set_setting(
            "translation/from_lang", self.ui.fromComboBox.currentData()
        )
        self.settings.set_setting(
            "translation/to_lang", self.ui.toComboBox.currentData()
        )

    @staticmethod
    def _set_combo_value(combo_box: QComboBox, value: str | None) -> None:
        if value is not None:
            index = combo_box.findData(value)
            if index >= 0:
                combo_box.setCurrentIndex(index)

    def _connect_signals(self) -> None:
        self.ui.whisperComboBox.currentIndexChanged.connect(self._on_model_changed)
        self.ui.fromComboBox.currentIndexChanged.connect(self._on_model_changed)
        self.ui.toComboBox.currentIndexChanged.connect(self._on_model_changed)

        self.ui.inputComboBox.currentIndexChanged.connect(self._save_preferences)
        self.ui.outputComboBox.currentIndexChanged.connect(self._save_preferences)
        self.ui.voiceComboBox.currentIndexChanged.connect(self._save_preferences)

        self.ui.startButton.clicked.connect(self.toggle_recording)
        self.ui.voicesButton.clicked.connect(self.open_download_voices_window)
        self.ui.actionHelp.triggered.connect(self.open_help_window)
        self.ui.actionAbout.triggered.connect(self.open_about_window)

    def _on_model_changed(self) -> None:
        self._save_preferences()
        self._check_model_status()

    def _check_model_status(self) -> None:
        model_size = self.ui.whisperComboBox.currentData()
        from_lang = self.ui.fromComboBox.currentData()
        to_lang = self.ui.toComboBox.currentData()

        missing_model = not is_model_downloaded(model_size)
        missing_translation = not is_translation_installed(from_lang, to_lang)

        if missing_model and missing_translation:
            text = self.tr(
                "Note: The speech recognition model and translation package will be downloaded upon starting."
            )
        elif missing_model:
            text = self.tr(
                "Note: The speech recognition model will be downloaded upon starting."
            )
        elif missing_translation:
            text = self.tr(
                "Note: The translation package will be downloaded upon starting."
            )
        else:
            text = None

        if text:
            self.ui.warningLabel.setText(text)
            self.ui.warningLabel.show()
        else:
            self.ui.warningLabel.hide()

    def toggle_recording(self) -> None:
        if self.is_recording:
            self._stop_pipeline()
        else:
            self._start_pipeline()

    def _start_pipeline(self) -> None:
        model_size = self.ui.whisperComboBox.currentData()
        from_lang = self.ui.fromComboBox.currentData()
        to_lang = self.ui.toComboBox.currentData()

        needs_download = not is_model_downloaded(
            model_size
        ) or not is_translation_installed(from_lang, to_lang)

        if needs_download:
            self._download_then_launch(model_size, from_lang, to_lang)
        else:
            self._launch_workers()

    def _download_then_launch(
        self, model_size: str, from_lang: str, to_lang: str
    ) -> None:
        self.progress_dialog = QProgressDialog(
            self.tr("Downloading required models. This may take a while..."),
            None,
            0,
            0,
            self,
        )
        self.progress_dialog.setWindowTitle("Downloading...")
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setCancelButton(None)
        self.progress_dialog.show()

        self.downloader_thread = PipelineDownloaderThread(
            model_size, from_lang, to_lang
        )
        self.downloader_thread.finished_download.connect(self._on_download_complete)
        self.downloader_thread.start()

    def _on_download_complete(self) -> None:
        self.progress_dialog.accept()
        self._check_model_status()
        self._launch_workers()

    def _set_pipeline_controls_enabled(self, enabled: bool) -> None:
        self.ui.whisperComboBox.setEnabled(enabled)
        self.ui.inputComboBox.setEnabled(enabled)
        self.ui.outputComboBox.setEnabled(enabled)
        self.ui.fromComboBox.setEnabled(enabled)
        self.ui.toComboBox.setEnabled(enabled)

        voice_available = (
            self.ui.voiceComboBox.count() > 0
            and self.ui.voiceComboBox.currentData() is not None
        )
        self.ui.voiceComboBox.setEnabled(enabled and voice_available)

    def _flush_queues(self) -> None:
        for q in (self.audio_queue, self.text_queue, self.tts_queue):
            while not q.empty():
                q.get_nowait()

    def _launch_workers(self) -> None:
        self.is_recording = True
        self.ui.startButton.setText(self.tr("Stop"))
        self._set_pipeline_controls_enabled(False)
        self._flush_queues()

        device_id = self.ui.inputComboBox.currentData()
        output_device_id = self.ui.outputComboBox.currentData()
        src_lang = self.ui.fromComboBox.currentData()
        tgt_lang = self.ui.toComboBox.currentData()
        model_size = self.ui.whisperComboBox.currentData()
        voice_key = self.ui.voiceComboBox.currentData()

        self.capture_thread = AudioCaptureThread(device_id, self.audio_queue)
        self.capture_thread.start()

        self.asr_thread = ASRWorkerThread(
            model_size, self.audio_queue, self.text_queue, src_lang
        )
        self.asr_thread.start()

        self.translate_thread = TranslateWorkerThread(self.text_queue, tgt_lang)
        self.translate_thread.text_ready.connect(self._on_text_ready)
        self.translate_thread.start()

        if voice_key:
            voice_path = get_voice_model_path(voice_key)
            if voice_path:
                self.tts_thread = TTSWorkerThread(
                    self.tts_queue, output_device_id, voice_path
                )
                self.tts_thread.start()

        print("--- Recording Started ---")

    def _stop_pipeline(self) -> None:
        self.is_recording = False
        self.ui.startButton.setText(self.tr("Start"))
        self._set_pipeline_controls_enabled(True)

        print("--- Stopping Threads ---")
        for thread in (
            self.capture_thread,
            self.asr_thread,
            self.translate_thread,
            self.tts_thread,
        ):
            if thread is not None:
                thread.stop()
                thread.wait()

        print("--- Recording Stopped ---")

    def _on_text_ready(
        self, original_text: str, translated_text: str, src_lang: str
    ) -> None:
        tgt_lang = self.ui.toComboBox.currentData()
        print(f"[{src_lang}] {original_text}")
        print(f"[{tgt_lang}] -> {translated_text}")
        self.tts_queue.put(translated_text)

    def open_download_voices_window(self) -> None:
        if self.download_window is None:
            self.download_window = DownloadVoicesWindow()

        self.download_window.show()
        self.download_window.raise_()
        self.download_window.activateWindow()

    def open_help_window(self):
        if self.help_window is None:
            self.help_window = HelpWindow()

        self.help_window.show()
        self.help_window.raise_()
        self.help_window.activateWindow()

    def open_about_window(self):
        if self.about_window is None:
            self.about_window = AboutWindow()

        self.about_window.show()
        self.about_window.raise_()
        self.about_window.activateWindow()
