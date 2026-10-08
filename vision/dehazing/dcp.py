"""Lightweight Dark Channel Prior (DCP)-style utilities.

This module provides starter-quality dehazing primitives intended for extension.
"""

from __future__ import annotations

import cv2
import numpy as np


def dark_channel(image_bgr: np.ndarray, patch_size: int = 15) -> np.ndarray:
    """Compute dark channel map for an image."""
    if patch_size <= 0 or patch_size % 2 == 0:
        raise ValueError("patch_size must be a positive odd integer")

    min_per_pixel = np.min(image_bgr.astype(np.float32), axis=2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (patch_size, patch_size))
    return cv2.erode(min_per_pixel, kernel)


def estimate_atmospheric_light(
    image_bgr: np.ndarray,
    dark: np.ndarray,
    top_percent: float = 0.001,
) -> np.ndarray:
    """Estimate atmospheric light from brightest dark-channel pixels."""
    if not (0.0 < top_percent <= 1.0):
        raise ValueError("top_percent must be in the interval (0, 1]")

    flat_dark = dark.reshape(-1)
    flat_image = image_bgr.reshape(-1, 3).astype(np.float32)

    count = max(1, int(flat_dark.size * top_percent))
    indices = np.argpartition(flat_dark, -count)[-count:]
    return np.max(flat_image[indices], axis=0)


def recover_scene_radiance(
    image_bgr: np.ndarray,
    transmission: np.ndarray,
    atmospheric_light: np.ndarray,
    t0: float = 0.1,
) -> np.ndarray:
    """Recover scene radiance with bounded transmission floor."""
    transmission = np.clip(transmission, t0, 1.0)[:, :, None]
    image = image_bgr.astype(np.float32)
    atmospheric = atmospheric_light.reshape(1, 1, 3)

    radiance = (image - atmospheric) / transmission + atmospheric
    return np.clip(radiance, 0, 255).astype(np.uint8)
