"""CLAHE helper utilities for visibility enhancement experiments."""

from __future__ import annotations

import cv2
import numpy as np


def apply_clahe_bgr(
    image_bgr: np.ndarray,
    clip_limit: float = 2.0,
    tile_grid_size: tuple[int, int] = (8, 8),
) -> np.ndarray:
    """Apply CLAHE in LAB color space and return an enhanced BGR image.

    Args:
        image_bgr: Input image in BGR layout.
        clip_limit: CLAHE clip limit.
        tile_grid_size: Size of CLAHE tiles.

    Returns:
        Enhanced image in BGR layout.
    """
    if image_bgr is None or image_bgr.size == 0:
        raise ValueError("image_bgr must be a non-empty ndarray")

    lab = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    l_enhanced = clahe.apply(l)

    enhanced_lab = cv2.merge((l_enhanced, a, b))
    return cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
