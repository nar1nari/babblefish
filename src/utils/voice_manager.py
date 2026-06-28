import os
import json

USER_HOME = os.path.expanduser("~")
VOICES_DIR = os.path.join(USER_HOME, ".babblefish", "voices")
os.makedirs(VOICES_DIR, exist_ok=True)

PIPER_VOICES_JSON_URL = (
    "https://huggingface.co/rhasspy/piper-voices/resolve/main/voices.json"
)
HUGGINGFACE_BASE_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/main/"


def is_voice_installed(voice_key: str) -> bool:
    voice_path = os.path.join(VOICES_DIR, voice_key)
    if not os.path.exists(voice_path):
        return False

    for file in os.listdir(voice_path):
        if file.endswith(".onnx"):
            return True
    return False


def get_installed_voices():
    if not os.path.exists(VOICES_DIR):
        return []
    installed = []
    for item in os.listdir(VOICES_DIR):
        if os.path.isdir(os.path.join(VOICES_DIR, item)) and is_voice_installed(item):
            installed.append(item)
    return sorted(installed)


def get_voice_model_path(voice_key: str) -> str | None:
    voice_path = os.path.join(VOICES_DIR, voice_key)
    if not os.path.exists(voice_path):
        return None

    for file in os.listdir(voice_path):
        if file.endswith(".onnx"):
            return os.path.join(voice_path, file)
    return None
