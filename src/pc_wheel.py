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

# Initialize SDL for FFB
SDL_Init(SDL_INIT_JOYSTICK | SDL_INIT_HAPTIC)

# Setup Pygame
pygame.init()
wheel_index = 0

if pygame.joystick.get_count() == 0:
    print("No wheel detected!")
    exit()
    
wheel = pygame.joystick.Joystick(wheel_index)
wheel.init()

# --- INITIALIZE REAL FFB ---
# BRIDGE TO SDL2 HAPTIC
# Open the same joystick index using SDL2's internal function
sdl_joystick = SDL_JoystickOpen(wheel_index)
haptic = SDL_HapticOpenFromJoystick(sdl_joystick)

if not haptic:
    print("Wheel found, but Haptic (FFB) could not be initialized.")
    exit()

# Define the Constant Force Effect using the correct SDL2 Structure
haptic_effect = SDL_HapticEffect()
haptic_effect.type = SDL_HAPTIC_CONSTANT
haptic_effect.constant.direction.type = SDL_HAPTIC_CARTESIAN
haptic_effect.constant.direction.dir[0] = 0
haptic_effect.constant.length = SDL_HAPTIC_INFINITY
haptic_effect.constant.level = 0 

effect_id = SDL_HapticNewEffect(haptic, haptic_effect)
SDL_HapticRunEffect(haptic, effect_id, 1)

def set_ffb_level(level):
    """Level range: -32768 to 32767"""
    if haptic:
        # We update the 'constant' property inside the effect union
        haptic_effect.constant.level = int(level)
        SDL_HapticUpdateEffect(haptic, effect_id, haptic_effect)

print(f"Connected to: {wheel.get_name()}")
print("Sending data... Press Ctrl+C to stop.")

try:
    while True:
        pygame.event.pump()

        # STEERING (Axis 0)
        # Range: -1.0 to 1.0 -> Map to 0 to 180
        steer_raw = wheel.get_axis(0)
        steer_val = int((steer_raw + 1) * 90)
        
        # REAL FFB CALCULATION
        force_strength = 12000 # Max is 32767
        ffb_center = 0.0
        distance_from_center = steer_raw - ffb_center
        ffb_force = distance_from_center * force_strength
        set_ffb_level(ffb_force)
        
        # PEDALS (T248 uses Axis 5 for Gas, Axis 1 for Brake)
        gas_raw = wheel.get_axis(5)   
        brake_raw = wheel.get_axis(1) 

        gas_normalized = (1 - gas_raw) / 2
        brake_normalized = (1 - brake_raw) / 2

        # Combine: Gas is positive, Brake is negative
        throttle_val = int((gas_normalized * 100) - (brake_normalized * 100))

        # --- CONSTRAINTS ---
        # Clamp Steering
        if steer_val > 180: steer_val = 180
        elif steer_val < 0: steer_val = 0
        
        # Deadzone for pedals
        if abs(throttle_val) < 3: 
            throttle_val = 0 
        elif throttle_val >= 99:
            throttle_val = 100
        elif throttle_val <= -99:
            throttle_val = -100

        # --- SEND DATA ---
        message = f"S{steer_val} T{throttle_val}"
        sock.sendto(message.encode(), (ESP32_IP, ESP32_PORT))

        # Using \r to update the same line in the console
        print(f"Steer: {steer_val:3} | Throttle: {throttle_val:4} | FFB Force: {int(ffb_force):6}", end="\n")
        
        # 10ms delay (100Hz) is very responsive for ESP32 without flooding the chip
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nStopping...")
    if haptic:
        SDL_HapticClose(haptic)
    if sdl_joystick:
        SDL_JoystickClose(sdl_joystick)
    pygame.quit()