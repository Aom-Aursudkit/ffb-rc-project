import pygame
import socket
import time
import csv
from sdl2 import (
    SDL_Init, SDL_INIT_JOYSTICK, SDL_INIT_HAPTIC,
    SDL_JoystickOpen, SDL_HapticOpenFromJoystick,
    SDL_HapticEffect, SDL_HapticConstant, SDL_HapticNewEffect, SDL_HapticRunEffect,
    SDL_HapticConstant, SDL_HAPTIC_CONSTANT, SDL_HAPTIC_INFINITY, SDL_HapticUpdateEffect,
    SDL_HapticClose, SDL_JoystickClose, SDL_HAPTIC_CARTESIAN
)

# --- CONFIGURATION ---
ESP32_IP = "192.168.4.1"
ESP32_PORT = 4210

TEST_COMPONENT = "stiffness"  # stiffness, damping, friction, load, gravity, jolt
OUTPUT_FILE = f"data/ffb_tests/{TEST_COMPONENT}_real.csv"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.02)

SDL_Init(SDL_INIT_JOYSTICK | SDL_INIT_HAPTIC)
pygame.init()
wheel = pygame.joystick.Joystick(0)
wheel.init()
sdl_joystick = SDL_JoystickOpen(0)
haptic = SDL_HapticOpenFromJoystick(sdl_joystick)

haptic_effect = SDL_HapticEffect()
haptic_effect.type = SDL_HAPTIC_CONSTANT
haptic_effect.constant.direction.type = SDL_HAPTIC_CARTESIAN
haptic_effect.constant.direction.dir[0] = 0
haptic_effect.constant.length = SDL_HAPTIC_INFINITY
effect_id = SDL_HapticNewEffect(haptic, haptic_effect)
SDL_HapticRunEffect(haptic, effect_id, 1)

def set_ffb_level(level):
    if haptic:
        haptic_effect.constant.level = int(max(-32767, min(32767, level)))
        SDL_HapticUpdateEffect(haptic, effect_id, haptic_effect)

velocity = 0.0
loadCell = 0.0

def get_telemetry_data():
    global velocity, loadCell
    try:
        response, addr = sock.recvfrom(1024)
        res = response.decode()
        if 'A' in res and 'G' in res and 'L' in res:
            data = res.split('G')
            accel = data[0].replace('A', '').split(',')
            gyro_load = data[1].split('L')
            gyro = gyro_load[0].split(',')
            loadCell = float(gyro_load[1])
            linAccX, linAccY, linAccZ = float(accel[0]), float(accel[1]), float(accel[2])
            gyroX, gyroY, gyroZ = float(gyro[0]), float(gyro[1]), float(gyro[2])
            velocity = (velocity * 0.99) + (linAccX * 0.01)
            return linAccX, linAccY, linAccZ, gyroX, gyroY, gyroZ, velocity, loadCell
    except socket.timeout:
        pass
    return 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, velocity, 0.0

def calculate_component_ffb(steer_raw, steer_velocity, accX, accY, accZ, gyroX, gyroY, gyroZ, velocity, loadCell):
    speed_factor = min(abs(velocity) * 2.0, 1.0)

    if TEST_COMPONENT == "stiffness":
        ffb = steer_raw * (2000 + (speed_factor * 8000))

    elif TEST_COMPONENT == "damping":
        ffb = steer_velocity * 500

    elif TEST_COMPONENT == "friction":
        friction_mag = 2000 * (1.0 - speed_factor)
        ffb = friction_mag if steer_velocity > 0 else (-friction_mag if steer_velocity < 0 else 0)

    elif TEST_COMPONENT == "load":
        ffb = (abs(loadCell) / 1000.0) * 5000

    elif TEST_COMPONENT == "gravity":
        ffb = accX * 1500

    elif TEST_COMPONENT == "jolt":
        ffb = accZ * 500

    else:
        ffb = 0

    return max(-32767, min(32767, int(ffb)))

print(f"Connected to: {wheel.get_name()}")
print(f"Testing: {TEST_COMPONENT}")
print(f"Recording to: {OUTPUT_FILE}")
print("Move steering wheel slowly. Press Ctrl+C to stop.")

csv_data = []
start_time = time.time()
prev_steer = 0.0
prev_time = time.time()

try:
    while True:
        pygame.event.pump()
        steer_raw = wheel.get_axis(0)

        current_time = time.time()
        dt = max(current_time - prev_time, 0.001)
        steer_velocity = (steer_raw - prev_steer) / dt

        accX, accY, accZ, gyroX, gyroY, gyroZ, velocity, loadCell = get_telemetry_data()

        ffb_force = calculate_component_ffb(steer_raw, steer_velocity, accX, accY, accZ, gyroX, gyroY, gyroZ, velocity, loadCell)
        set_ffb_level(ffb_force)

        steer_val_to_send = int((steer_raw + 1) * 90)
        sock.sendto(f"S{steer_val_to_send} T0".encode(), (ESP32_IP, ESP32_PORT))

        elapsed_ms = int((current_time - start_time) * 1000)
        csv_data.append([elapsed_ms, steer_raw, steer_velocity, velocity, loadCell, ffb_force])

        print(f"[{elapsed_ms:6d}] Steer: {steer_raw:+.2f} | Vel: {steer_velocity:+.2f} | FFB: {ffb_force:6d}   ", end="\r")

        prev_steer = steer_raw
        prev_time = current_time
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nStopping...")

with open(OUTPUT_FILE, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp_ms', 'steer_raw', 'steer_velocity', 'velocity', 'load_g', 'ffb_force'])
    writer.writerows(csv_data)

print(f"\nSaved {len(csv_data)} samples to {OUTPUT_FILE}")

SDL_HapticClose(haptic)
SDL_JoystickClose(sdl_joystick)
pygame.quit()