import pygame
import socket
import time

# --- CONFIGURATION ---
ESP32_IP = "192.168.4.1"  # <--- REPLACE WITH THE IP FROM SERIAL MONITOR
ESP32_PORT = 4210

# Setup UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Setup Pygame for Controller
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No controller found!")
    exit()

controller = pygame.joystick.Joystick(0)
controller.init()

print(f"Connected to: {controller.get_name()}")
print("Sending data... Press Ctrl+C to stop.")

vibrated_at_limit = False

def vibrate(duration_ms=100, intensity=0.8):
    """Triggers the controller rumble."""
    # rumble(low_frequency, high_frequency, duration_ms)
    controller.rumble(intensity, intensity, duration_ms)

try:
    while True:
        pygame.event.pump()

        steer = controller.get_axis(0) 
        throttle = controller.get_axis(5)
        throttle_rev = controller.get_axis(4)

        # Map
        steer_val = float((steer + 1) * 90)
        throttle_val = float((throttle + 1) * 50)
        throttle_val = float(throttle_val - ((throttle_rev + 1) * 50))

        if steer_val > 178: steer_val = 180
        elif steer_val < 2: steer_val = 0
        if throttle_val > 98: throttle_val = 100
        elif throttle_val < 2 and throttle_val > -2: throttle_val = 0
        elif throttle_val < -98: throttle_val = -100
        
        # --- VIBRATION LOGIC ---
        if (steer_val <= 2 or steer_val >= 178):
            if not vibrated_at_limit:
                vibrate(150, 0.6) # Short 150ms buzz
                vibrated_at_limit = True
        else:
            vibrated_at_limit = False

        message = f"S{steer_val} T{throttle_val}"
        
        # Send via UDP
        sock.sendto(message.encode(), (ESP32_IP, ESP32_PORT))

        print(f"Steer: {steer_val:3} | Throttle: {throttle_val:3}", end="\n")
        time.sleep(0.001)

except KeyboardInterrupt:
    print("\nStopping...")
    pygame.quit()