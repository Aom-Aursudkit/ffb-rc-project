# FFB RC Project - Session Log

> **INSTRUCTION:** Read this file at the start of every session. Update "Last Updated" and add any new notes/changes to "Session Notes" section.

## Last Updated: 2026-05-10

## Project Structure
```
ffb-rc-project/
├── src/
│   ├── main.cpp          # ESP32 firmware
│   ├── pc_controller.py # Game controller input
│   ├── pc_keyboard.py   # Keyboard input
│   └── pc_wheel.py     # Racing wheel FFB support
├── platformio.ini      # ESP32-C6 build config
└── .pio/               # Build artifacts
```

## Hardware
- **Board:** ESP32-C6 DevKitC-1
- **Servo Pin:** GPIO 15
- **ESC Pin:** GPIO 23
- **RGB LED:** GPIO 8
- **Current Sensor:** GPIO 4 (ACS712 5A)

## Communication Protocol
- **Mode:** WiFi Access Point (AP)
- **SSID:** ESP32-RC-CAR
- **Password:** 12345678
- **Protocol:** UDP
- **Port:** 4210
- **Format:** `S{steering} T{throttle}`
  - Steering: 0-180 (90 = center)
  - Throttle: -100 to +100

## Session Notes
2026-05-10:
- Rewrote REPORT.md Chapter 2 sections 2.1 and 2.2 with detailed information from the research papers.
- Updated hardware configuration: Now using 1 kg load cell alongside the ACS712 current sensor for improved force measurement.
- Updated REPORT.md Chapter 3 to reflect the load cell integration.
- Restructured REPORT.md Chapter 3 to follow the requested numbering hierarchy (3, 3.1, 3.1.1, 1., 2.).
- Updated REPORT.md Chapter 2 with summaries of reviewed research papers on Force Feedback Steering.
- Reviewed research PDF "Open Topic 2025 - Force Feedback Steering RC".
- Updated REPORT.md Chapter 3 with detailed technical methodology (Hardware, Communication, and FFB Algorithm).
- Cleaned up global platformio/littlefs installations (Python 3.12 incompatibility).
- Created AGENTS.md for repo context.
- Generated REPORT.md structure based on user template and project state.

2026-04-25:
- Verified all Python files syntax valid
- PlatformIO has compatibility issues with Python 3.12
- Recommended: Use VS Code PlatformIO extension to build
- Dependencies needed: pygame, pysdl2

## Pending Tasks
- [ ] Build and upload firmware
- [ ] Test WiFi connection
- [ ] Test servo/ESC
- [ ] Test controller input