import pygame
import socket
import time
import ctypes
from sdl2 import (
    SDL_Init, SDL_INIT_JOYSTICK, SDL_INIT_HAPTIC, 
    SDL_JoystickOpen, SDL_HapticOpenFromJoystick,
    SDL_HapticEffect, SDL_HapticConstant, SDL_HapticNewEffect, SDL_HapticRunEffect,
    SDL_HAPTIC_CONSTANT, SDL_HAPTIC_INFINITY, SDL_HapticUpdateEffect,
    SDL_HapticClose, SDL_JoystickClose, SDL_HAPTIC_CARTESIAN
)

# --- CONFIGURATION ---
ESP32_IP = "192.168.4.1" 
ESP32_PORT = 4210

# Setup UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.02) 

# Initialize SDL/Pygame
SDL_Init(SDL_INIT_JOYSTICK | SDL_INIT_HAPTIC)
pygame.init()
wheel = pygame.joystick.Joystick(0)
wheel.init()
sdl_joystick = SDL_JoystickOpen(0)
haptic = SDL_HapticOpenFromJoystick(sdl_joystick)

# FFB Effect Setup
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

# --- CALCULATIONS ---
velocity = 0.0
prev_steer = 0.0
prev_time = time.time()
drift_threshold_accel = 3.0

# FFB GAINS
GAIN_DAMPING = 2000     # Damping: resists turning faster
GAIN_FRICTION = 2000    # Friction: resists motion, stronger at low speeds
GAIN_LOAD = 2000        # Load Resistance: direct force from load cell (real-world resistance)
GAIN_STIFFNESS = 500    # Passive stiffness: resists being turned away from center
GAIN_SAT = 20000        # Self-Aligning Torque (active self-centering)
GAIN_GRAVITY = 1500        # Gravity Torque: simulates weight of steering wheel
GAIN_SURFACE_JOLT = 500    # Surface Jolt: simulates bumps/road

def get_telemetry_data():
    global velocity, linAccX, linAccY, linAccZ, gyroX, gyroY, gyroZ, loadCell
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
            
            velocity = (velocity * 0.99) + (linAccX * -0.01)
            return linAccX, linAccY, linAccZ, gyroX, gyroY, gyroZ, velocity, loadCell
    except socket.timeout:
        pass
    return 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, velocity, 0.0

def calculate_forces(steer_raw, accX, accY, accZ, gyroX, gyroY, gyroZ, velocity, loadCell):
    global prev_steer, prev_time
    
    current_time = time.time()
    dt = max(current_time - prev_time, 0.001)
    
    # 1. RESISTIVE FORCES (Passive - Damping, Friction, Load Resistance)
    steer_velocity = (steer_raw - prev_steer) / dt
    damping = (steer_velocity * GAIN_DAMPING)

    speed_factor = min(abs(velocity) * 2.0, 1.0)
    friction_mag = GAIN_FRICTION * (1.0 - speed_factor)
    friction = friction_mag if steer_velocity > 0 else (-friction_mag if steer_velocity < 0 else 0)
    stiffness_mag = steer_raw * GAIN_STIFFNESS
    stiffness = stiffness_mag if steer_velocity > 0 else (-stiffness_mag if steer_velocity < 0 else 0)


    # Load Cell adds real-world steering resistance as Passive force (direct measurement, not scaled by angle)
    load_resistance_mag = (loadCell) * GAIN_LOAD
    load_resistance = load_resistance_mag if steer_velocity > 0 else (-load_resistance_mag if steer_velocity < 0 else 0)

    resistive_torque = damping + friction + load_resistance + stiffness

    # 2. ACTIVE FORCES (Restorative - SAT, Gravity, Surface Jolt)
    sat = steer_raw * (speed_factor * GAIN_SAT)
    gravity_torque = accX * GAIN_GRAVITY # Gravity tilt
    surface_jolt = accZ * GAIN_SURFACE_JOLT

    active_torque = sat + gravity_torque + surface_jolt

    if abs(accY) > (drift_threshold_accel * (1 + abs(velocity))):
        active_torque *= 0.2

    # Total FFB
    ffb_force = resistive_torque + active_torque
    # Test
    # ffb_force = load_resistance
    
    prev_steer = steer_raw
    prev_time = current_time
    return max(-32767, min(32767, int(ffb_force)))

# --- MAIN LOOP ---
print(f"Connected to: {wheel.get_name()}")
try:
    while True:
        pygame.event.pump()
        steer_raw = wheel.get_axis(0)
        
        # Get Data
        accX, accY, accZ, gyroX, gyroY, gyroZ, velocity, loadCell = get_telemetry_data()
        
        # Apply FFB Calculation
        ffb_force = calculate_forces(steer_raw, accX, accY, accZ, gyroX, gyroY, gyroZ, velocity, loadCell)
        set_ffb_level(ffb_force)
        
        # Throttle/Brake
        gas = (1 - wheel.get_axis(5)) / 2
        brake = (1 - wheel.get_axis(1)) / 2
        throttle_val = int((gas * 100) - (brake * 100))
        
        # Send Steering/Throttle command
        steer_val_to_send = int((steer_raw + 1) * 90) 
        sock.sendto(f"S{steer_val_to_send} T{throttle_val}".encode(), (ESP32_IP, ESP32_PORT))

        print(f"Steer: {steer_raw:.2f} | FFB: {ffb_force:6} | Vel: {velocity:.1f} | Load: {loadCell:.1f}g | AccXYZ: {accX:.2f},{accY:.2f},{accZ:.2f} | GyroXYZ: {gyroX:.2f},{gyroY:.2f},{gyroZ:.2f}", end="\n")
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nStopping...")
    SDL_HapticClose(haptic)
    SDL_JoystickClose(sdl_joystick)
    pygame.quit()
