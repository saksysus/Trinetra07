# TRINETRA Firmware

## Overview

The `firmware/` directory contains the embedded software that runs on the microcontrollers used in **TRINETRA**, a prototype intelligent vehicle-safety and roadside monitoring system designed for low-visibility environments such as fog-affected roads and mining routes.

The firmware enables the hardware units to perform their assigned operations and provides the foundation for communication between moving vehicles, stationary vehicles, and track-side infrastructure.

These Arduino sketches are intended to be uploaded to their respective microcontroller boards. Each sketch represents a separate hardware unit in the TRINETRA prototype.

## Directory Contents

| File                     | Description                                                                                                                                                 |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Track_node.ino`         | **Track-side node firmware.** Intended for the infrastructure node positioned along the track or route to support roadside monitoring and communication.    |
| `moving_vehicle.ino`     | **Moving vehicle firmware.** Intended for the vehicle unit that moves along the route and participates in the TRINETRA monitoring and communication system. |
| `stationary_vehicle.ino` | **Stationary vehicle firmware.** Intended for the vehicle-side unit operating in a fixed position during prototype testing and system integration.          |

## Role in TRINETRA

The firmware forms the embedded layer of the system:

- **Vehicle unit:** Runs the control and communication logic assigned to the moving vehicle.
- **Stationary unit:** Provides a fixed vehicle-side endpoint for communication and controlled testing.
- **Track-side unit:** Provides an infrastructure endpoint for roadside monitoring and vehicle communication.

Together, these modules provide the embedded foundation for testing the interaction between vehicles and infrastructure in low-visibility conditions.

The exact sensors, communication protocols, pin assignments, and implemented functions are defined in the individual source files.

## Requirements

- Arduino IDE.
- Compatible microcontroller boards specified by the individual sketches.
- Appropriate board support packages.
- Required Arduino libraries.
- USB data cable for programming.
- Hardware peripherals and wiring specified in each sketch.

## How to Upload the Firmware

1. Clone or download the TRINETRA repository.
2. Open Arduino IDE.
3. Open the `.ino` file for the hardware unit you want to program.
4. Check the source code for its board type, pin assignments, and library dependencies.
5. Connect the corresponding microcontroller to your computer.
6. Select the appropriate board and port under **Tools**.
7. Install any required libraries.
8. Compile and upload the sketch.
9. Repeat for the other hardware units.
10. Test the units independently before testing the integrated system.

## Verification and Testing

After uploading, verify that each unit starts correctly and performs its intended functions. Where implemented, use Serial Monitor to inspect debugging messages and communication status.

Test node-to-node communication and the complete prototype under controlled conditions before conducting field trials.

## Safety and Limitations

TRINETRA is a prototype system. Its firmware and communication functions must be validated before operational deployment. It should not be treated as a certified collision-avoidance system or as the sole safety mechanism in a mining or road environment.

##

