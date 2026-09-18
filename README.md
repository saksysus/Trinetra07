# TRINETRA - Visibility & Safe-Speed Assistant for Open-Cast Mines

TRINETRA is a safety and operational-assistance system designed for
**open-cast iron ore mines operating in fog and low-visibility
conditions**. It combines onboard sensing, roadside infrastructure,
sensor fusion, computer vision, positioning, and real-time decision
support to help mine vehicles operate more safely without depending
entirely on network connectivity.

## Problem

During severe monsoon and fog conditions, visibility in open-cast mines
can fall to only a few metres. This makes it difficult for haul-truck
drivers to detect:

-   Other mine vehicles
-   Obstacles and rocks
-   Road boundaries and turns
-   Safe following distances
-   Changing road and environmental conditions

Conventional camera-only systems can become unreliable when visibility
deteriorates. TRINETRA addresses this limitation through **multi-layer
perception and local safety logic**.

## Proposed Solution

TRINETRA follows an end-to-end pipeline:

**Detection → Processing → Decision → Driver Alert**

The system combines:

-   **77 GHz mmWave radar** for object detection in low visibility
-   **Camera + dehazing** for enhanced visual awareness
-   **GPS** for vehicle positioning
-   **LoRa** for vehicle-to-roadside/control communication
-   **Sensor fusion** for more reliable situational awareness
-   **Safe-speed calculation** using stopping distance, vehicle
    separation, and road gradient
-   **Roadside nodes** for infrastructure-assisted awareness and
    positioning
-   **Driver dashboard** for real-time alerts and guidance

## Key Features

### 1. Dual-Layer Protection

Onboard sensors provide immediate hazard detection, while roadside nodes
provide wider-area traffic awareness.

### 2. Local Onboard Safety

Critical hazard detection and alerts can operate locally, reducing
dependence on continuous network connectivity.

### 3. Fog-Aware Perception

The camera feed can use dehazing during poor visibility, while mmWave
radar provides an additional sensing layer.

### 4. Safe-Speed Assistance

Instead of only warning the driver about an obstacle, TRINETRA can
calculate a recommended safe speed using relevant vehicle and road
conditions.

### 5. Position & Route Awareness

GPS and roadside infrastructure support vehicle localization, route
awareness, and positioning correction.

### 6. Fail-Restrictive Operation

If communication or infrastructure becomes unavailable, the system is
designed to move toward a more restrictive operating state rather than
assuming normal conditions.

### 7. Advisory-First Deployment

The initial implementation is advisory, allowing field validation and
operator feedback before considering higher levels of intervention.

## System Architecture

``` text
                    ┌─────────────────────┐
                    │   Mine Environment  │
                    │ Fog / Rain / Dust   │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
        ┌───────▼───────┐             ┌───────▼────────┐
        │ Onboard Unit  │             │ Roadside Node  │
        │               │             │                │
        │ Camera        │             │ LoRa           │
        │ 77 GHz Radar  │             │ GPS/Position   │
        │ GPS           │             │ Local sensing  │
        │ Processing    │             │                │
        └───────┬───────┘             └───────┬────────┘
                │                             │
                └──────────────┬──────────────┘
                               │
                       ┌───────▼────────┐
                       │  Sensor Fusion │
                       │ + AI Processing│
                       └───────┬────────┘
                               │
                       ┌───────▼────────┐
                       │ Decision Engine│
                       │                │
                       │ Safe Speed     │
                       │ Hazard Status  │
                       │ Alerts         │
                       └───────┬────────┘
                               │
                       ┌───────▼─────────┐
                       │ Driver / Control│
                       │ Room Dashboard  │
                       └─────────────────┘
```

## Hardware

The prototype architecture can include:

-   ESP32-S3-based vehicle controller
-   77 GHz mmWave radar
-   Camera module
-   GPS/GNSS receiver
-   LoRa communication module
-   Raspberry Pi for edge processing where required
-   Roadside communication/positioning nodes
-   Power supply and rugged enclosures

The architecture is modular so individual sensing or communication
components can be upgraded without redesigning the complete system.

## Software & Processing

The software pipeline is designed around real-time perception and
decision support:

1.  Capture camera and sensor data
2.  Estimate visibility and environmental conditions
3.  Apply camera enhancement/dehazing when required
4.  Detect vehicles and obstacles
5.  Fuse radar, camera, and positioning information
6.  Estimate relative distance and vehicle state
7.  Calculate safe operating speed
8.  Generate driver warnings and guidance
9.  Communicate relevant information to roadside/control infrastructure

## Safe-Speed Concept

TRINETRA extends conventional hazard detection by connecting perception
to an operating-speed recommendation.

The decision considers factors such as:

-   Vehicle separation
-   Vehicle speed
-   Stopping distance
-   Road gradient
-   Visibility conditions
-   Detected hazards

The implementation should be validated against applicable mine-safety
requirements and operating procedures before deployment.

## Communication Strategy

TRINETRA uses a layered communication approach:

-   **Onboard processing:** immediate safety decisions
-   **LoRa:** low-bandwidth long-range coordination with roadside
    infrastructure
-   **GPS/GNSS:** positioning and route awareness
-   **Roadside nodes:** infrastructure-assisted communication and
    localization

This allows the vehicle to retain critical local safety functionality
even when communication is temporarily unavailable.

## Feasibility

### Technical Feasibility

The system uses commercially available sensing, processing, positioning,
and communication technologies in a modular architecture.

### Economic Viability

The proposed architecture uses relatively low-cost roadside and vehicle
units and avoids requiring every safety function to be implemented
through expensive per-truck infrastructure.

### Operational Viability

Roadside nodes can support mixed fleets, while digital route information
can be updated as mine layouts change.

### Safety & Implementation Feasibility

The architecture includes local safety logic, fail-restrictive
behaviour, positioning checks, and an advisory-first deployment strategy
to support gradual field validation.

## Challenges & Mitigations

  -----------------------------------------------------------------------
  Challenge                           Mitigation
  ----------------------------------- -----------------------------------
  Dense fog reduces camera visibility 77 GHz radar + camera dehazing

  GPS uncertainty in mine terrain     Roadside correction + sensor fusion

  Communication loss                  Local onboard safety logic

  Harsh mining environment            Modular and ruggedized hardware

  Mixed fleet and driver adoption     Advisory-first deployment
  -----------------------------------------------------------------------

## Dashboard

The TRINETRA dashboard provides a centralized view of:

-   Current vehicle speed
-   Recommended safe speed
-   Visibility level
-   Detected vehicles/obstacles
-   Relative distance and speed
-   Route and GPS status
-   Sensor health
-   Environmental conditions
-   System status
-   Driver alerts

## Deployment Roadmap

``` text
Prototype
   ↓
Laboratory Validation
   ↓
Controlled Mine Trial
   ↓
Advisory Deployment
   ↓
Performance Validation
   ↓
Scaled Mine Deployment
```

## Expected Impact

TRINETRA aims to:

-   Improve driver awareness during low visibility
-   Reduce collision risk between mine vehicles
-   Provide speed guidance based on actual road conditions
-   Maintain local safety functionality during communication loss
-   Support continuous and safer haulage operations
-   Provide a scalable architecture for different mine routes and fleets

## Project Status

**Stage:** Prototype / Concept Validation

The system architecture, dashboard, sensing strategy, communication
approach, and safety logic are designed for prototype development and
controlled validation. Real-world deployment would require site-specific
testing, calibration, ruggedization, and compliance validation.

## Team

**TRINETRA --- Safe Haulage. Continuous Operations.**

Developed as a solution for the Smart India Hackathon problem statement:

**"Safe and Efficient Operation of Mine Vehicles in Fog and
Low-Visibility Conditions in Open Cast Iron Ore Mines."**

## Disclaimer

TRINETRA is a proposed safety-assistance system. The prototype and
algorithms must be validated with actual mine data, vehicle
characteristics, site geometry, environmental conditions, and applicable
mine-safety requirements before operational deployment.
