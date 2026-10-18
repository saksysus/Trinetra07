# TRINETRA

**Block signalling for mine haul roads in fog.**

Team EdgeX Hyperions · Smart India Hackathon 2026 · Problem Statement 26007 (NMDC Limited)
*Safe and Efficient Operation of Mine Vehicles in Fog and Low-Visibility Conditions in Open Cast Iron Ore Mines*

---

## What this is

In the monsoon, the Bailadila iron ore mines sit inside cloud. On the haul roads a driver can see about 3 to 5 metres.

A loaded dumper at the 30 km/h DGMS limit needs about 30 metres to stop (DGMS stopping-distance rule, 6.25% grade). No sensor on the truck can close that gap, so the usual answer is to slow down or stop.

TRINETRA takes a different approach. It does not try to make the dumper see further. The **haul road** tells the dumper what is ahead, using the same idea railways use: split the road into blocks, know which blocks are occupied, and give the next driver a safe speed.

> Most systems answer "is something in my way?"
> TRINETRA answers "how fast may I go?"

## Why not just better cameras

- A published CSIR-CIMFR system tested at Bacheli, Bailadila raised visibility from about 5 m to 30–40 m using IR cameras and illuminators. That helps, but at 30 km/h it leaves little margin and says nothing about a truck around the bend.
- Systems where vehicles share their own positions only see vehicles that carry the radio. A contractor jeep, a person, or a dumper with dead electronics stays invisible.
- On the same hardware, the same paper reports that standard CLAHE and dark-channel-prior dehazing reached only 15–20 m. We implemented both, so the limit can be shown rather than just claimed.

## How it works

1. A roadside node detects a vehicle passing.
2. If the vehicle is not carrying our radio tag, it is logged as an **UNIDENTIFIED VEHICLE** and tracked anyway.
3. The node tells every dumper over radio that the block is occupied.
4. A safe speed is worked out from the DGMS stopping-distance rule:

```
safe speed = sqrt( gap × (46 − 2.6 × slope) )      capped at 30 km/h
```

5. The driver is shown the advisory. If a link or node fails, the system shows a **degraded** state and lowers the advised speed instead of going quiet.

**Two independent safety layers**

| Layer | Where | Job | Needs network? |
|---|---|---|---|
| Road | Roadside nodes | Looks ahead beyond what a truck sensor can see | Yes (radio mesh) |
| Dumper | On the truck | Last-100 m proximity sensing, road-edge distance, tilt | No |

Either layer alone still protects the driver.

## Current status

This repository holds the **proof of concept** (a scaled model). The full prototype is a design, described at the bottom.

### Working

| Part | Detail |
|---|---|
| Fog measurement | Camera looks at a fixed 8×8 checkerboard; visibility in metres from Koschmieder's law. Reading falls when the lens is fogged and recovers. |
| Dehazing | CLAHE and Dark Channel Prior, running on the Raspberry Pi |
| Four-panel viewer | Raw / CLAHE / DCP / live visibility reading |
| Data logging | SQLite, plus auto-labelled images for a fog classifier |
| Bridge | Reads the car's state, applies the DGMS formula, publishes an advisory |
| Track node | ESP32 + HC-SR04 ultrasonic sensor, ESP-NOW to the car |
| Moving car | ESP32, web page, L298N 4-wheel drive, ESP-NOW receiver |
| Stationary dumper | ESP32 + TF-Luna style LiDAR + ILI9341 TFT, sends "MOVE LEFT" |

### In progress or not built yet

| Part | Status |
|---|---|
| Track node "BLOCK OCCUPIED / UNIDENTIFIED VEHICLE" messages | Updated firmware written; confirm it is flashed |
| Driver and control-room web pages | Designed; generation in progress |
| Fog-level classifier (random forest) | Data collection running; not trained |
| Object classifier | Exists separately; not wired into this pipeline |
| 24 GHz radar (HLK-LD2452) | Ordered; not integrated |
| LoRa | Modules in hand; the PoC currently runs on ESP-NOW |
| Radar target classifier, simulator, shift planner | Not built |

## Honest limits of the PoC

- Uses an **ultrasonic sensor** at the track node and a **LiDAR** at the stationary dumper as stand-ins for radar.
- Radio is **ESP-NOW**, not LoRa.
- "Tagged or untagged" is judged from the car's signal strength (RSSI). That is a proxy: if the tagged car is also close to the node, it can be misjudged.
- The gap values the bridge uses (0 m, 5 m, 250 m) are demo stand-ins, not measured distances.
- Safe speed is calculated on the Raspberry Pi here. In the intended design it runs on the dumper unit so it works with no network.
- The camera-based visibility reading only means something while the camera and target are fixed in place.
- Only one real car is present. Any other vehicles shown on a dashboard are not real.

## Hardware used in the PoC

| Item | Role |
|---|---|
| ESP32 DevKit (3) | Track node, moving car, stationary dumper |
| Raspberry Pi 4B (8 GB) | Fog measurement, dehazing, MQTT broker, bridge, web server |
| USB webcam | Visibility measurement and dehazing input |
| HC-SR04 ultrasonic | Track node obstacle sensor |
| TF-Luna style LiDAR | Stationary dumper range sensor |
| ILI9341 TFT | Stationary dumper display |
| L298N driver, 4-wheel chassis | Moving car |
| MLX90640 thermal camera | Available for sensor comparison |
| HLK-LD2452 24 GHz radar | Ordered |
| Ultrasonic fogger | Fog box |

## Repository layout (Pi side)

```
calibrate.py     one-time camera calibration (gives C0 and the target box)
vision.py        fog in metres, dehazing, saves frames, publishes to MQTT
dehaze_dcp.py    Dark Channel Prior dehazing
panel.py         four-panel viewer
bridge.py        reads car state, computes advisory, publishes to MQTT
ui_server.py     serves the web pages, data and camera streams
fogfeat.py       image features for the fog classifier
train_fog.py     trains the fog classifier
data/            auto-saved training images: clear / light / dense
ui/              driver.html and control.html
```

The three ESP32 sketches (track node, moving car, stationary dumper) are separate Arduino sketches.

## Setup (Raspberry Pi)

```bash
sudo apt update
sudo apt install -y python3-opencv mosquitto mosquitto-clients python3-pip
pip3 install paho-mqtt numpy scikit-learn joblib requests flask --break-system-packages

echo -e "listener 1883\nallow_anonymous true" | sudo tee /etc/mosquitto/conf.d/local.conf
sudo systemctl enable --now mosquitto
```

Join the car's Wi-Fi network (name and password are set in the car firmware), then check the link:

```bash
curl http://192.168.4.1/state
```

### Calibrate the camera (once, and again if the camera or target moves)

1. Print an 8×8 black and white checkerboard and fix it in place.
2. Fix the camera in place and measure the distance in metres.
3. Run `python3 calibrate.py`, move the green box fully inside the checkerboard, press `q`.
4. Copy the printed `C0`, `ROI` and your measured distance into the top of `vision.py`.

Current values in the repo: `D = 2.7`, `C0 = 0.7234`, `ROI = (110, 10, 240, 180)`.

## Run

Use one terminal per program.

| Terminal 1 | Terminal 2 | Terminal 3 |
|---|---|---|
| `python3 vision.py` | `python3 bridge.py` | `python3 ui_server.py` |

Stop a program with `Ctrl+C` in its own terminal. If the camera reports busy, stop leftovers with `pkill -f vision.py`.

| Address | Shows |
|---|---|
| `http://192.168.4.1` | Moving car's own page (alerts, drive controls) |
| `http://localhost:8000/driver` | Driver dashboard on the Pi |
| `http://192.168.4.50:8000/control` | Control-room page (Pi set to a fixed address) |

## Data flow

**Radio message (ESP-NOW, shared by all three boards), 65 bytes:**

```c
typedef struct {
  uint8_t messageType;
  char    message[64];
} AlertPacket;
```

| Type | Meaning |
|---|---|
| 1 | Block occupied (track node) |
| 2 | Block clear (track node) |
| 3 | Command from the stationary dumper ("MOVE LEFT") |
| 4 | Car heartbeat |
| 5 | Node heartbeat |

**MQTT topics on the Pi:**

| Topic | Content |
|---|---|
| `trinetra/vision/visibility` | Visibility in metres, contrast, fog level |
| `trinetra/vision/fog_ml` | Fog level from the classifier (only if trained) |
| `trinetra/car/state` | Car state copied from its web page data |
| `trinetra/advisory` | Aspect (GREEN / AMBER / RED / DEGRADED), safe speed, reason |

**Advisory rules in `bridge.py`:**

| Condition | Aspect |
|---|---|
| Stationary dumper command active | RED |
| Track node block occupied | AMBER |
| Nothing active | GREEN |
| Car link lost | DEGRADED (8 km/h) |

## Planned prototype (design only, not built)

| Part | Plan |
|---|---|
| Dumper unit | ESP32-S3, 77 GHz front radar, 24 GHz side radar, LoRa, GNSS, IMU, barometer, SD log, display, voice |
| Standard node | ESP32-S3, 24 GHz radar, LoRa, GNSS timing, corner reflectors |
| Sentinel node | Standard node plus 77 GHz radar, camera with reference target, thermal |
| Radio | LoRa SX1262 at 866.1 MHz (licence-exempt in India under GSR 564(E)) |
| Positioning | Distance measured along a surveyed road map; position resets at every node |
| Offline tools | A simulator running the same block logic, and a shift planner |

Cost figures from the plan are component estimates only (about ₹18,000 per dumper unit, ₹8,000 per standard node, ₹25,000 per sentinel node). They exclude integration, installation and certification.

**Not claimed:** detecting a rockfall that lands between nodes; telling the driver the road is clear; controlling brakes, throttle or steering. The system is advisory only. Radio range over real hill terrain and node maintenance still need field testing.

## References

- Chaulya et al., *Smart driving assistance system for mining operations in foggy environments*, Discover Electronics 2:13 (2025). DOI 10.1007/s44291-025-00054-1
- Chaulya et al., *V2X, GNSS, radar, and camera-based intelligent system for adaptive control of heavy mining vehicles during foggy weather*, Journal of Quality Technology 56(4), 2024
- He, Sun and Tang, *Single Image Haze Removal Using Dark Channel Prior*, IEEE TPAMI, 2011
- DGMS (Tech) Circular 06 of 2020 and Circular 09 of 2008
- EMESRT proximity detection levels, ISO 21815
