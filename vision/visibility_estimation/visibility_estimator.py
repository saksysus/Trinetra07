"""Visibility estimation helpers for quick prototyping."""

from __future__ import annotations

import cv2
import numpy as np


def estimate_visibility_score(image_bgr: np.ndarray) -> float:
    """Estimate relative visibility score in [0, 1] from edge density + contrast.

    Higher values indicate clearer scenes in this baseline heuristic.
    """
    if image_bgr is None or image_bgr.size == 0:
        raise ValueError("image_bgr must be a non-empty ndarray")

    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)

    edge_density = float(np.mean(edges > 0))
    contrast = float(np.std(gray) / 128.0)

    score = 0.6 * edge_density + 0.4 * min(contrast, 1.0)
    return float(np.clip(score, 0.0, 1.0))
