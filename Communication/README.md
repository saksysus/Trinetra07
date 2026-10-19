# TRINETRA – Communication

Communication layer for the TRINETRA fog-safety system (Team EdgeX Hyperions, Smart India Hackathon 2026, PS 26007, NMDC Limited).

In fog, line of sight fails, so vehicles and roadside nodes need to share position and warnings over radio. This folder holds the two links we built and tested.

## Links

| Link | Used for | Hardware |
|---|---|---|
| **LoRa** | Long-range V2V / V2I messaging; each dumper shares its GPS coordinates with nearby dumpers and nodes, which compare coordinates to work out relative position | ESP32 + LoRa module (SX1278 tested; SX1262 in the deck) |
| **ESP-NOW** | Short-range roadside beacons and hazard messages to a moving vehicle (curve, slope, "MOVE LEFT") | ESP32 / ESP32-C3 |

UWB was removed from the design because its range was too low. The mesh also lets each node work independently of the others.

## Folder contents

```
communication/
├── README.md
├── lora_pingpong/
│   └── lora_pingpong.ino      <- LoRa range test, logs RSSI and SNR
└── espnow/
    ├── beacon/                <- trackside beacon sketch (same code on every node, change NODE_NAME)
    ├── car_node/              <- moving car receiver (RSSI-based distance/ETA, web dashboard)
    ├── track_node/            <- fixed ultrasonic node ("Curve 17 Ahead. SLOW DOWN", "Slope Ahead")
    └── stationary_dumper/     <- TF-Luna ToF + ILI9341 TFT, sends "MOVE LEFT" to the car
```

Put your working `.ino` files into the `espnow/` subfolders above. Each Arduino sketch must sit in a folder with the same name as the `.ino` file.

## LoRa range test

`lora_pingpong/lora_pingpong.ino` runs on two boards. Set `IS_INITIATOR` to `true` on one and `false` on the other. The initiator sends `PING n`, the other replies `PONG n`, and both print RSSI and SNR over Serial.

Library: **LoRa** by Sandeep Mistry (Arduino Library Manager).

Check before flashing:
- Pin defines match your wiring.
- `LORA_FREQ` matches your module and local regulations. SX1278 modules are usually 433 MHz; the India sub-GHz ISM band is 865-867 MHz.
- Antenna is attached before powering the module.

## ESP-NOW beacons

- Two trackside boards broadcast their node name once a second on WiFi channel 1.
- The car reads the RSSI of each incoming packet to estimate distance and time to each node.
- The same beacon sketch is flashed to every trackside board; only `NODE_NAME` changes.
- Fixed nodes and the stationary dumper send messages directly to the moving car's MAC address. The car shows them on its web dashboard.
- The stationary dumper uses a TF-Luna ToF sensor; when it detects the vehicle nearby it sends `MOVE LEFT`, shown on the car's dashboard and on the dumper's TFT.

## How it fits into TRINETRA

```
Dumper A --LoRa (GPS)--> Dumper B / roadside node
Roadside node --ESP-NOW--> moving vehicle --> driver alert
```

Messages are advisory only. The system warns and guides the driver; it does not control throttle, brake or steering.

## Team

EdgeX Hyperions – SIH 2026, PS 26007.
