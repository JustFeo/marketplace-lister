from __future__ import annotations

import os
from pathlib import Path

from PIL import Image

from ..config import settings


def ensure_dir(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)


def save_image_variants(
    owner_id: str | None, item_id: str, image_id: str, src_path: str
) -> dict:
    base_dir = os.path.join(settings.MEDIA_ROOT, owner_id or "anon", item_id)
    ensure_dir(base_dir)
    orig_path = os.path.join(base_dir, f"{image_id}_orig.jpg")
    thumb_path = os.path.join(base_dir, f"{image_id}_thumb.jpg")
    medium_path = os.path.join(base_dir, f"{image_id}_medium.jpg")

    with Image.open(src_path) as im:
        im.convert("RGB").save(orig_path, format="JPEG", quality=90)
        thumb = im.copy()
        thumb.thumbnail((200, 200))
        thumb.convert("RGB").save(thumb_path, format="JPEG", quality=85)
        med = im.copy()
        med.thumbnail((800, 800))
        med.convert("RGB").save(medium_path, format="JPEG", quality=85)

    return {
        "orig": orig_path,
        "thumb": thumb_path,
        "medium": medium_path,
    }
