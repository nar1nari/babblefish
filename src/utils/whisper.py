import os
from huggingface_hub import constants

WHISPER_MODELS = {
    "tiny": "tiny (~1 GB VRAM, ~10x speed)",
    "base": "base (~1 GB VRAM, ~7x speed)",
    "small": "small (~2 GB VRAM, ~4x speed)",
    "medium": "medium (~5 GB VRAM, ~2x speed)",
    "large-v3": "large (~10 GB VRAM, 1x speed)",
}


def is_model_downloaded(model_size: str) -> bool:
    repo_id = f"Systran/faster-whisper-{model_size}"
    repo_folder = repo_id.replace("/", "--")
    cache_path = os.path.join(constants.HF_HUB_CACHE, f"models--{repo_folder}")

    return os.path.exists(cache_path)
