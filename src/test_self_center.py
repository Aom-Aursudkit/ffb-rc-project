import pygame
import socket
import time
import csv
from sdl2 import (
    SDL_Init, SDL_INIT_JOYSTICK, SDL_INIT_HAPTIC,
    SDL_JoystickOpen, SDL_HapticOpenFromJoystick,
    SDL_HapticEffect, SDL_HapticConstant, SDL_HapticNewEffect, SDL_HapticRunEffect,
    SDL_HAPTIC_CONSTANT, SDL_HAPTIC_INFINITY, SDL_HapticUpdateEffect,
    SDL_HapticClose, SDL_JoystickClose, SDL_HAPTIC_CARTESIAN
)

ESP32_IP = "192.168.4.1"
ESP32_PORT = 4210

OUTPUT_FILE = "data/ffb_tests/stiffness_self_center.csv"

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

velocity = 0.0
loadCell = 0.0

def set_ffb_level(level):
    if haptic:
        haptic_effect.constant.level = int(max(-32767, min(32767, level)))
        SDL_HapticUpdateEffect(haptic, effect_id, haptic_effect)

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

def calculate_self_center_ffb(steer_raw, velocity):
    """
    Self-Centering stiffness: τ = K_center × θ
    K_center = 2000 + speed_factor × 8000
    speed_factor = min(|velocity| × 2, 1.0)
    """
    speed_factor = min(abs(velocity) * 2.0, 1.0)
    K_center = 2000 + (speed_factor * 8000)
    ffb = steer_raw * K_center
    return max(-32767, min(32767, int(ffb)))

print(f"Connected to: {wheel.get_name()}")
print("=" * 50)
print("SELF-CENTERING (STEERING STIFFNESS) TEST")
print("=" * 50)
print("Test: Wheel turned to side, car drives forward")
print("Expected: FFB increases self-centering force with speed")
print()
print("STEERING POSITIONS:")
print("  Left Trigger (LB) + Right Trigger (RB) = steer FULL LEFT")
print("  Right Trigger (RB) + Left Trigger (LB) = steer FULL RIGHT")
print("  Press A button = START recording")
print("  Press B button = STOP and save")
print()
print("Hold trigger to set angle, drive car forward, observe FFB")
print("Press Ctrl+C to exit")
print("=" * 50)

csv_data = []
recording = False
start_time = time.time()
test_duration = 60

try:
    while True:
        pygame.event.pump()

        lb = wheel.get_button(4)  # Left bumper
        rb = wheel.get_button(5)  # Right bumper
        a_btn = wheel.get_button(0)  # A to start
        b_btn = wheel.get_button(1)  # B to stop

        if a_btn and not recording:
            recording = True
            csv_data = []
            start_time = time.time()
            print("\n>>> START RECORDING <<<")

        if b_btn and recording:
            recording = False
            print(">>> STOP RECORDING <<<")

        if lb and not rb:
            steer_val = 0    # Full left
        elif rb and not lb:
            steer_val = 180  # Full right
        else:
            steer_val = 90   # Center

        steer_raw = (steer_val / 90.0) - 1.0

        accX, accY, accZ, gyroX, gyroY, gyroZ, velocity, loadCell = get_telemetry_data()

        ffb_force = calculate_self_center_ffb(steer_raw, velocity)
        set_ffb_level(ffb_force)

        throttle = 10  # Fixed forward speed
        sock.sendto(f"S{steer_val} T{throttle}".encode(), (ESP32_IP, ESP32_PORT))

        if recording:
            elapsed_ms = int((time.time() - start_time) * 1000)
            speed_kmh = velocity * 3.6
            csv_data.append([elapsed_ms, steer_val, steer_raw, velocity, speed_kmh, ffb_force])
            print(f"[{elapsed_ms:5d}] Steer:{steer_val:3d} | Vel:{velocity:+.2f} ({speed_kmh:+.1f} km/h) | FFB:{ffb_force:6d}", end="\r")

        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nExiting...")

if csv_data:
    with open(OUTPUT_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp_ms', 'steer_angle', 'steer_raw', 'velocity', 'speed_kmh', 'ffb_force'])
        writer.writerows(csv_data)
    print(f"\nSaved {len(csv_data)} samples to {OUTPUT_FILE}")

SDL_HapticClose(haptic)
SDL_JoystickClose(sdl_joystick)
pygame.quit()