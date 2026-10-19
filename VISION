"""
TRINETRA - Vision: real-time dehazing (Dark Channel Prior + guided filter)

Runs on a Raspberry Pi 4B with a USB webcam, or on any PC for testing.
Processing is done at reduced resolution and the transmission map is
upscaled, which keeps it usable on the Pi.

Usage:
    python dehaze.py                       # webcam 0, side-by-side view
    python dehaze.py --source fog.mp4      # video file
    python dehaze.py --source 0 --scale 0.35 --no-display --save out.mp4
"""

import argparse
import time

import cv2
import numpy as np


def dark_channel(img, size):
    """Per-pixel minimum over colour channels, then minimum over a patch."""
    min_c = np.min(img, axis=2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
    return cv2.erode(min_c, kernel)


def estimate_atmosphere(img, dark, top_percent=0.1):
    """Atmospheric light = mean colour of the haziest (brightest dark-channel) pixels."""
    h, w = dark.shape
    n = max(int(h * w * top_percent / 100), 1)
    idx = np.argpartition(dark.ravel(), -n)[-n:]
    return img.reshape(-1, 3)[idx].mean(axis=0)


def guided_filter(guide, src, radius, eps):
    """Single-channel guided filter built from box filters (no ximgproc needed)."""
    k = (2 * radius + 1, 2 * radius + 1)
    mean_i = cv2.boxFilter(guide, -1, k)
    mean_p = cv2.boxFilter(src, -1, k)
    cov_ip = cv2.boxFilter(guide * src, -1, k) - mean_i * mean_p
    var_i = cv2.boxFilter(guide * guide, -1, k) - mean_i * mean_i
    a = cov_ip / (var_i + eps)
    b = mean_p - a * mean_i
    return cv2.boxFilter(a, -1, k) * guide + cv2.boxFilter(b, -1, k)


class Dehazer:
    def __init__(self, patch=15, omega=0.95, t0=0.1, scale=0.5,
                 gf_radius=30, gf_eps=1e-3, a_smooth=0.9):
        self.patch = patch          # dark-channel patch size (px, at processed res)
        self.omega = omega          # how much haze to remove (0-1); <1 keeps some depth cue
        self.t0 = t0                # minimum transmission, limits noise amplification
        self.scale = scale          # processing scale (lower = faster)
        self.gf_radius = gf_radius
        self.gf_eps = gf_eps
        self.a_smooth = a_smooth    # temporal smoothing of atmospheric light (video flicker)
        self._A = None

    def __call__(self, frame_bgr):
        h, w = frame_bgr.shape[:2]
        if self.scale < 1.0:
            small = cv2.resize(frame_bgr, None, fx=self.scale, fy=self.scale,
                               interpolation=cv2.INTER_AREA)
        else:
            small = frame_bgr

        I = small.astype(np.float32) / 255.0
        dark = dark_channel(I, self.patch)

        A = estimate_atmosphere(I, dark)
        self._A = A if self._A is None else self.a_smooth * self._A + (1 - self.a_smooth) * A
        A = np.maximum(self._A, 1e-3)

        # Transmission estimate, refined with the grayscale frame as guide
        t = 1.0 - self.omega * dark_channel(I / A, self.patch)
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
        t = guided_filter(gray, t, self.gf_radius, self.gf_eps)
        t = np.clip(t, self.t0, 1.0)

        if self.scale < 1.0:
            t = cv2.resize(t, (w, h), interpolation=cv2.INTER_LINEAR)

        # Recover scene radiance on the full-resolution frame
        J = (frame_bgr.astype(np.float32) / 255.0 - A) / t[..., None] + A
        return (np.clip(J, 0, 1) * 255).astype(np.uint8)


def main():
    ap = argparse.ArgumentParser(description="TRINETRA dehazing")
    ap.add_argument("--source", default="0", help="camera index or video path")
    ap.add_argument("--scale", type=float, default=0.5, help="processing scale (0.25-1.0)")
    ap.add_argument("--patch", type=int, default=15)
    ap.add_argument("--omega", type=float, default=0.95)
    ap.add_argument("--t0", type=float, default=0.1)
    ap.add_argument("--width", type=int, default=640)
    ap.add_argument("--height", type=int, default=480)
    ap.add_argument("--save", default=None, help="write side-by-side output video here")
    ap.add_argument("--no-display", action="store_true", help="headless (no window)")
    args = ap.parse_args()

    src = int(args.source) if args.source.isdigit() else args.source
    cap = cv2.VideoCapture(src)
    if isinstance(src, int):
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
    if not cap.isOpened():
        raise SystemExit(f"Could not open source: {args.source}")

    dehazer = Dehazer(patch=args.patch, omega=args.omega, t0=args.t0, scale=args.scale)
    writer = None
    fps, last = 0.0, time.time()

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        out = dehazer(frame)
        combined = np.hstack([frame, out])

        now = time.time()
        fps = 0.9 * fps + 0.1 * (1.0 / max(now - last, 1e-6))
        last = now
        cv2.putText(combined, f"{fps:.1f} FPS", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(combined, "original", (10, combined.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(combined, "dehazed", (frame.shape[1] + 10, combined.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        if args.save:
            if writer is None:
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                writer = cv2.VideoWriter(args.save, fourcc, 20.0,
                                         (combined.shape[1], combined.shape[0]))
            writer.write(combined)

        if not args.no_display:
            cv2.imshow("TRINETRA dehaze", combined)
            if cv2.waitKey(1) & 0xFF in (ord("q"), 27):
                break

    cap.release()
    if writer:
        writer.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
