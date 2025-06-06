import logging
import requests
from io import BytesIO
from PIL import Image
import torch
import numpy as np
from transformers import CLIPProcessor, CLIPModel
import torch.nn.functional as F
from typing import Annotated
from .helper.helpers import _score_thumbnail
from llama_index.core.tools import FunctionTool

# ─── Logging setup ─────────────────────────────────────────────────────────────
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# Initialize CLIP model and processor globally
# CLIP_MODEL_NAME = "openai/clip-vit-large-patch14"
# logger.info(f"Loading CLIP model {CLIP_MODEL_NAME}…")
# model = CLIPModel.from_pretrained(CLIP_MODEL_NAME)
# processor = CLIPProcessor.from_pretrained(CLIP_MODEL_NAME)

# Global parameters
TEMPERATURE = 0.07
SCALE = 5.0

# Prompts covering design, clarity, emotion, composition
POSITIVE_PROMPTS = [
    "eye-catching thumbnail",
    "bold, vibrant colors",
    "clear, readable text",
    "prominent faces",
    "professional design",
]
NEGATIVE_PROMPTS = [
    "blurry or out of focus",
    "dark or underexposed",
    "dull colors",
    "small or unreadable text",
    "cluttered layout",
]


def _download_image(url: str) -> Image.Image:
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    return Image.open(BytesIO(resp.content)).convert("RGB")


def score_thumbnail(
    thumbnail_url: str,
) -> float:
    """
    Compute a 0–1 score for how "attractive" a thumbnail is.
    """
    return _score_thumbnail(thumbnail_url)

score_thumbnail_tool = FunctionTool.from_defaults(score_thumbnail)