# FFB RC Project - Agent Instructions

## Build Commands

```bash
# DO NOT use `pio run` directly - PlatformIO has Python 3.12 compatibility issues
# Instead use VS Code extension:
# - Press Ctrl+Shift+P → "PlatformIO: Build"
# - Or click the Build button in the status bar
```

## Project Structure

- `src/main.cpp` - ESP32-C6 firmware
- `src/pc_*.py` - PC controller inputs (controller/keyboard/wheel)
- `platformio.ini` - Build config for ESP32-C6-DevKitC-1

## Dependencies

```bash
pip install pygame pysdl2  # For Python controller scripts
```

## Hardware

- Board: ESP32-C6-DevKitC-1
- Servo: GPIO 15, ESC: GPIO 23, LED: GPIO 8, Current: GPIO 4

## Key Files

- `SESSION_LOG.md` - Contains detailed project history and notes
- Read this file at session start to understand current state