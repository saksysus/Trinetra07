# TRINETRA – Vision

Camera pipeline for the TRINETRA fog-safety system (Team EdgeX Hyperions, Smart India Hackathon 2026, PS 26007, NMDC Limited).

In dense fog, rain or dust, a dumper driver can barely see what is ahead. The vision module does two jobs:

1. **Dehazing** – restores contrast in the live camera feed so the driver gets a clearer view.
2. **Detection** – a YOLO model identifies mining equipment (especially dumpers) in the frame.

The vision output is fused with radar and LoRa data on the Raspberry Pi to classify the obstacle and guide the driver. The system is **advisory only**: it alerts and guides, it does not control throttle, brake or steering.

## Hardware

- Raspberry Pi 4B
- Logitech USB webcam

## Folder contents

```
vision/
├── README.md     <- this file
└── dehaze.py     <- real-time dehazing (webcam or video file)
```

## Dehazing

`dehaze.py` uses the **Dark Channel Prior** method with a guided filter:

1. Compute the dark channel of the frame (minimum over colour channels and a local patch).
2. Estimate atmospheric light from the haziest pixels, smoothed over time to avoid flicker in video.
3. Estimate a transmission map `t(x)`, refine it with a guided filter (grayscale frame as guide).
4. Recover the scene: `J = (I - A) / max(t, t0) + A`

To keep it usable on the Pi, the maps are computed at reduced resolution (`--scale`) and the transmission map is upscaled before being applied to the full-resolution frame.

### Install

```bash
pip install opencv-python numpy
```

### Run

```bash
# Webcam, side-by-side original vs dehazed
python dehaze.py

# Video file
python dehaze.py --source fog.mp4

# Headless on the Pi, saving the result
python dehaze.py --source 0 --scale 0.35 --no-display --save out.mp4
```

Press `q` or `Esc` to quit.

### Tuning

| Option | Default | Effect |
|---|---|---|
| `--scale` | 0.5 | Processing resolution. Lower is faster on the Pi, slightly softer transmission map. |
| `--patch` | 15 | Dark-channel patch size. Larger gives a more reliable estimate but can cause halos. |
| `--omega` | 0.95 | Amount of haze removed. Lower keeps some haze for a natural look. |
| `--t0` | 0.1 | Minimum transmission. Raise it if noise or over-saturation appears in thick fog. |

### Known limitations

- Dark Channel Prior assumes some dark pixels exist in each patch. Large bright regions (sky, white walls) can be over-corrected.
- Very dense fog or dust with almost no scene contrast limits how much can be recovered.
- Frame rate depends on resolution and `--scale`; measure on the target Pi.

## Detection (YOLO)

- Model: YOLO26n, trained in Google Colab.
- Classes (7): Dragline, drill_machine, Dumper, excavator, grader, jeep, loader.
- The source dataset only had classification-style folders, so training boxes were auto-generated (centered). Real box labels would improve localisation.
- Training data is augmented with synthetic fog, rain and dust variants (Albumentations) to improve robustness in low visibility, and the model is fine-tuned from the earlier `best.pt` on the combined dataset.

## How it fits into TRINETRA

```
Camera -> Dehazing -> YOLO detection --+
                                       +--> Raspberry Pi sensor fusion -> driver alert / guidance
Radar + LoRa -> ESP32-S3 filtering ----+
```

The driver sees the alarm together with the dehazed footage, so the warning is easy to verify.

## Team

EdgeX Hyperions – SIH 2026, PS 26007.
