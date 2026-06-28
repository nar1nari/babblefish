from __future__ import annotations

import logging
import os
import queue
from dataclasses import dataclass

import argostranslate.translate
import numpy as np
import requests
import sounddevice as sd
import webrtcvad
from faster_whisper import WhisperModel, download_model
from piper import PiperVoice, SynthesisConfig
from PySide6.QtCore import QThread, Signal

from utils.translation import install_translation
from utils.voice_manager import HUGGINGFACE_BASE_URL, PIPER_VOICES_JSON_URL, VOICES_DIR

logger = logging.getLogger(__name__)

SAMPLE_RATE = 16000
FRAME_MS = 30
FRAME_SAMPLES = int(SAMPLE_RATE * FRAME_MS / 1000)
FRAME_BYTES = FRAME_SAMPLES * 2

# How many consecutive silent frames signal end-of-utterance (~750 ms)
SILENCE_FRAMES_END = 25
# Minimum speech frames required to accept an utterance (~240 ms)
MIN_SPEECH_FRAMES = 8


@dataclass
class AudioChunk:
    data: bytes


class PipelineDownloaderThread(QThread):
    finished_download = Signal()

    def __init__(self, model_size: str, from_lang: str, to_lang: str) -> None:
        super().__init__()
        self.model_size = model_size
        self.from_lang = from_lang
        self.to_lang = to_lang

    def run(self) -> None:
        download_model(self.model_size)
        install_translation(self.from_lang, self.to_lang)
        self.finished_download.emit()


class VoiceListFetcherThread(QThread):
    finished_fetch = Signal(dict)
    error_fetch = Signal(str)

    def run(self) -> None:
        try:
            response = requests.get(PIPER_VOICES_JSON_URL, timeout=10)
            response.raise_for_status()
            self.finished_fetch.emit(response.json())
        except Exception as exc:
            self.error_fetch.emit(str(exc))


class VoiceDownloaderThread(QThread):
    progress_updated = Signal(int)
    finished_download = Signal(str)
    error_download = Signal(str)

    def __init__(self, voice_key: str, files_dict: dict) -> None:
        super().__init__()
        self.voice_key = voice_key
        self.files_dict = files_dict

    def run(self) -> None:
        try:
            target_dir = os.path.join(VOICES_DIR, self.voice_key)
            os.makedirs(target_dir, exist_ok=True)

            total_bytes = sum(f["size_bytes"] for f in self.files_dict.values())
            downloaded_bytes = 0

            for relative_path, file_info in self.files_dict.items():
                url = HUGGINGFACE_BASE_URL + relative_path
                save_path = os.path.join(target_dir, os.path.basename(relative_path))

                response = requests.get(url, stream=True, timeout=15)
                response.raise_for_status()

                with open(save_path, "wb") as fh:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            fh.write(chunk)
                            downloaded_bytes += len(chunk)
                            self.progress_updated.emit(
                                int(downloaded_bytes / total_bytes * 100)
                            )

            self.finished_download.emit(self.voice_key)
        except Exception as exc:
            self.error_download.emit(str(exc))


class AudioCaptureThread(QThread):
    def __init__(
        self,
        device_id: int,
        out_queue: queue.Queue,
        vad_aggressiveness: int = 2,
    ) -> None:
        super().__init__()
        self.device_id = device_id
        self.out_queue = out_queue
        self.vad = webrtcvad.Vad(vad_aggressiveness)
        self.is_running = True
        self._raw_queue: queue.Queue[bytes] = queue.Queue()

    def stop(self) -> None:
        self.is_running = False

    def _audio_callback(self, indata, frames, time_info, status) -> None:
        if self.is_running:
            self._raw_queue.put(bytes(indata))

    def run(self) -> None:
        with sd.RawInputStream(
            device=self.device_id,
            samplerate=SAMPLE_RATE,
            blocksize=FRAME_SAMPLES,
            dtype="int16",
            channels=1,
            callback=self._audio_callback,
        ):
            self._vad_loop()

    def _vad_loop(self) -> None:
        speech_frames: list[bytes] = []
        in_speech = False
        silence_count = 0

        while self.is_running:
            try:
                frame = self._raw_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            if len(frame) != FRAME_BYTES:
                continue

            is_speech = self.vad.is_speech(frame, SAMPLE_RATE)

            if is_speech:
                speech_frames.append(frame)
                in_speech = True
                silence_count = 0
            elif in_speech:
                speech_frames.append(frame)
                silence_count += 1

                if silence_count >= SILENCE_FRAMES_END:
                    speech_len = len(speech_frames) - silence_count
                    if speech_len >= MIN_SPEECH_FRAMES:
                        self.out_queue.put(b"".join(speech_frames))
                    speech_frames = []
                    in_speech = False
                    silence_count = 0


class ASRWorkerThread(QThread):
    def __init__(
        self,
        model_size: str,
        in_queue: queue.Queue,
        out_queue: queue.Queue,
        src_lang: str,
    ) -> None:
        super().__init__()
        self.model_size = model_size
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.src_lang: str | None = src_lang if src_lang != "auto" else None
        self.is_running = True

    def stop(self) -> None:
        self.is_running = False

    def run(self) -> None:
        model = WhisperModel(self.model_size, device="cpu", compute_type="int8")

        while self.is_running:
            try:
                audio_bytes = self.in_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            audio_np = (
                np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
            )
            segments, info = model.transcribe(
                audio_np,
                language=self.src_lang,
                beam_size=5,
                vad_filter=False,
            )
            text = " ".join(seg.text.strip() for seg in segments).strip()
            if text:
                self.out_queue.put((text, info.language))


class TranslateWorkerThread(QThread):
    # (original_text, translated_text, detected_src_lang)
    text_ready = Signal(str, str, str)

    def __init__(self, in_queue: queue.Queue, tgt_lang: str) -> None:
        super().__init__()
        self.in_queue = in_queue
        self.tgt_lang = tgt_lang
        self.is_running = True

    def stop(self) -> None:
        self.is_running = False

    def run(self) -> None:
        while self.is_running:
            try:
                text, src_lang = self.in_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            translated = self._translate(text, src_lang)
            self.text_ready.emit(text, translated, src_lang)

    def _translate(self, text: str, src_lang: str) -> str:
        if src_lang == self.tgt_lang:
            return text

        installed = argostranslate.translate.get_installed_languages()
        from_obj = next((l for l in installed if l.code == src_lang), None)
        to_obj = next((l for l in installed if l.code == self.tgt_lang), None)

        if from_obj is None or to_obj is None:
            logger.warning("Translation missing for %s -> %s", src_lang, self.tgt_lang)
            return text

        translation = from_obj.get_translation(to_obj)
        if translation is None:
            return text

        try:
            return translation.translate(text)
        except Exception:
            logger.exception("Translation failed for text: %r", text)
            return text


class TTSWorkerThread(QThread):
    def __init__(self, in_queue: queue.Queue, device_id: int, voice_path: str) -> None:
        super().__init__()
        self.in_queue = in_queue
        self.device_id = device_id
        self.voice_path = voice_path
        self.is_running = True
        self._voice: PiperVoice | None = None

    def stop(self) -> None:
        self.is_running = False

    def run(self) -> None:
        self._voice = PiperVoice.load(self.voice_path, use_cuda=False)
        syn_config = SynthesisConfig(
            volume=1.0,
            length_scale=1.0,
            noise_scale=0.667,
            noise_w_scale=0.8,
        )

        while self.is_running:
            try:
                text = self.in_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            if text.strip():
                try:
                    self._speak(text, syn_config)
                except Exception:
                    logger.exception("[TTS] Failed to synthesise: %r", text)

    def _speak(self, text: str, syn_config: SynthesisConfig) -> None:
        stream: sd.OutputStream | None = None
        try:
            for chunk in self._voice.synthesize(text, syn_config=syn_config):
                if not self.is_running:
                    break

                audio = np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16)
                if chunk.sample_channels > 1:
                    audio = audio.reshape(-1, chunk.sample_channels)

                if stream is None:
                    stream = sd.OutputStream(
                        device=self.device_id,
                        samplerate=chunk.sample_rate,
                        channels=chunk.sample_channels,
                        dtype="int16",
                    )
                    stream.start()

                stream.write(audio)
        finally:
            if stream is not None:
                stream.stop()
                stream.close()
