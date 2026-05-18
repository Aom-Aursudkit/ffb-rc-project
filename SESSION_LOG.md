# FFB RC Project - Session Log

> **INSTRUCTION:** Read this file at the start of every session. Update "Last Updated" and add any new notes/changes to "Session Notes" section.

## Last Updated: 2026-05-17

## Project Structure
```
ffb-rc-project/
├── src/
│   ├── main.cpp           # ESP32 firmware
│   ├── main_origin.cpp    # Original firmware backup
│   ├── main_test_imu.cpp  # IMU test firmware
│   ├── main_test_signal.cpp
│   ├── test_loadcell.cpp  # Load cell calibration firmware
│   ├── pc_controller.py   # Game controller input
│   ├── pc_keyboard.py     # Keyboard input
│   └── pc_wheel.py        # Racing wheel FFB support (Thrustmaster T248)
├── Plotter/
│   ├── plot_latency.py    # Latency result plotter
│   └── plot_result/       # Latency test plots (from new test)
├── Backup/
│   ├── main.cpp           # Firmware backup
│   ├── test_loadcell.cpp
│   └── main_test_imu.cpp
├── platformio.ini         # ESP32-C6 build config
├── data/
│   ├── latency_results.csv  # Latency test data (100 packets, new test)
│   └── range_results.csv    # Range test data (simulated)
├── latency_results.csv    # Latency test data (200 packets)
├── Note.md                # Project context reference
├── REPORT.md              # Final report (Thai, fully structured)
├── AGENTS.md              # Agent instructions
└── SESSION_LOG.md         # This file
```

## RC Car Specifications
- **Chassis:** Unnamed 1/10 scale chassis
- **Motor:** Sensored BLDC 10.5T (Rocket RC)
- **ESC:** Rocket RC 130A (sensor wires integrated)
- **Servo:** 9IMod 20 kg high-torque servo
- **Power:** 2S LiPo 5200mAh

## Hardware
- **Board:** ESP32-C6 DevKitC-1
- **Servo Pin:** GPIO 15
- **ESC Pin:** GPIO 23
- **RGB LED:** GPIO 8
- **Current Sensor:** GPIO 4 (ACS712 5A)
- **IMU:** BNO086 V2 at I2C address 0x4A
- **Load Cell:** HX711 1kg, SCALE factor 103.5
  - DOUT: GPIO 5, SCK: GPIO 18
  - Left pull: +102000, Right pull: -105000

## Communication Protocol
- **Mode:** WiFi Access Point (AP)
- **SSID:** ESP32-RC-CAR
- **Password:** 12345678
- **Protocol:** UDP
- **Port:** 4210
- **Format (PC → ESP32):** `S{steering 0-180} T{throttle -100 to 100}`
- **Format (ESP32 → PC):** `A{accX},{accY},{accZ}G{gyroX},{gyroY},{gyroZ}L{loadCell}`
- **Telemetry received:** accX, accY, accZ, gyroX, gyroY, gyroZ, velocity (integrated from accX), loadCell

## FFB Algorithm (on PC, in pc_wheel.py)
- **Resistive (Passive):** Damping (steer_velocity × 500) + Friction (2000 × (1 - speed_factor)) + Load Resistance ((abs(loadCell)/1000) × 5000 × steer_raw)
- **Active (Restorative):** Stiffness (steer × (2000 + speed_factor × 8000)) + Gravity (accX × 1500) + Lateral (accY × 500) + Yaw (gyroZ × 200)
- **Surface Jolt:** accZ × 500
- **Drift Detection:** If |accY| > threshold × (1 + velocity), active_torque × 0.2

## System Architecture Clarification
- **ESP32-C6:** Sensor telemetry + Servo/ESC control only (NO FFB computation)
- **PC (pc_wheel.py):** FFB algorithm computation + Thrustmaster T248 FFB output

## Session Notes
2026-05-17:
- Fixed REPORT.md Section 1.3: Changed from "วัตถุประสงค์" to "ผลผลิตและผลลัพธ์ (Outputs and Outcomes)" with proper outputs/outcomes lists
- Fixed REPORT.md Section 3.1: Corrected system architecture - ESP32 handles sensor I/O + motor control, FFB algorithm runs on PC (pc_wheel.py)
- Updated SESSION_LOG.md to reflect FFB computation is on PC, not ESP32

2026-05-16:
- Added latency plot script (Plotter/plot_latency.py) generating 4 charts: timeseries, histogram, boxplot, CDF
- Ran plot script successfully: Mean=4.13ms, Median=2.37ms, Min=0.51ms, Max=41.85ms, P95=11.91ms, P99=23.84ms (200 packets)
- Read Note.md and found discrepancies with REPORT.md (latency numbers, missing JTEKT reference, formula mismatches)
- User requested full rewrite of REPORT.md with proper sourced formulas
- Rewrote REPORT.md completely with:
  - FFB formula sourced from Balachandran et al. 2014 (ASME DSCC, "Virtual Wheel Concept")
  - Clean Passive/Active force split with sensor-to-formula mapping table
  - 11 properly cited references (all from real papers, not made up)
  - Testing methodology backed by: Shakeri 2016 (ACM CHI), Böhle 2024 (IEEE IV), Wang 2018 (SAE), Katzourakis 2010 (IEEE Trans Haptics), IEEE 9568828, Mehdizadeh 2011 (CDC)
- Updated SESSION_LOG.md to reflect current state

2026-05-10:
- Integrated HX711 Load Cell support into main.cpp. Using Scale Factor: 103.5.
- Fixed Guru Meditation Error (crash) by adding a safety check if IMU fails to initialize.
- IMU Test Successful: BNO086 V2 communicating correctly at address 0x4A.
- Created IMU test firmware (src/main.cpp) for BNO086 V2.
- Renamed original main.cpp to src/main_origin.cpp.
- Added BNO086 V2 IMU sensor to hardware configuration for orientation tracking.
- Updated REPORT.md Chapter 3 to include BNO086 V2.
- Updated REPORT.md Chapter 4 with latency test results (0% loss, Avg: 3.84ms).
- Rewrote REPORT.md Chapter 2 sections 2.1 and 2.2 with detailed information from the research papers.
- Updated hardware configuration: Now using 1 kg load cell alongside the ACS712 current sensor for improved force measurement.
- Updated REPORT.md Chapter 3 to reflect the load cell integration.
- Restructured REPORT.md Chapter 3 to follow the requested numbering hierarchy (3, 3.1, 3.1.1, 1., 2.).
- Cleaned up global platformio/littlefs installations (Python 3.12 incompatibility).
- Created AGENTS.md for repo context.
- Generated REPORT.md structure based on user template and project state.

2026-04-25:
- Verified all Python files syntax valid
- PlatformIO has compatibility issues with Python 3.12
- Recommended: Use VS Code PlatformIO extension to build
- Dependencies needed: pygame, pysdl2

## Pending Tasks
- [ ] Build and upload firmware to ESP32-C6
- [ ] Physical Range Test (5m-50m)
- [ ] FFB Component Validation (Stiffness, Damping, Friction, Load Cell, Drift, Jolt)
- [ ] Subjective Self-Assessment (Likert 1-5)
- [ ] Quantitative Telemetry Test (log and plot)
- [ ] Chapter 5 Conclusion (after all tests)
- [ ] Copy REPORT.md into Word template