"""End-to-end starter dehazing pipeline for Trinetra07 vision experiments."""

from __future__ import annotations

import numpy as np

from .clahe import apply_clahe_bgr
from .dcp import dark_channel, estimate_atmospheric_light, recover_scene_radiance


def dehaze_image(image_bgr: np.ndarray, omega: float = 0.95, patch_size: int = 15) -> np.ndarray:
    """Run a lightweight DCP + CLAHE dehazing pipeline.

    This is a conservative baseline intended for iterative tuning against field data.
    """
    if image_bgr is None or image_bgr.size == 0:
        raise ValueError("image_bgr must be a non-empty ndarray")

    dark = dark_channel(image_bgr, patch_size=patch_size)
    atmospheric = estimate_atmospheric_light(image_bgr, dark)

    norm_image = image_bgr.astype(np.float32) / np.maximum(atmospheric, 1.0)
    transmission = 1.0 - omega * dark_channel(norm_image.astype(np.float32), patch_size=patch_size)

    dehazed = recover_scene_radiance(image_bgr, transmission, atmospheric)
    return apply_clahe_bgr(dehazed)
