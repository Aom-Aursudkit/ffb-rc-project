import pygame
import socket
import time

# --- CONFIGURATION ---
ESP32_IP = "192.168.4.1"
ESP32_PORT = 4210

# Setup UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Setup Pygame for Keyboard
pygame.init()
# Create a small window so it can "see" keyboard events
screen = pygame.display.set_mode((200, 200))
pygame.display.set_caption("RC Keyboard")

print("Keyboard Control Active!")
print("W/S or Up/Down: Throttle")
print("A/D or Left/Right: Steering")
print("Press ESC to quit.")

try:
    while True:
        pygame.event.pump()
        keys = pygame.key.get_pressed()

        # --- STEERING LOGIC ---
        # Default center (90)
        steer_val = 90.0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            steer_val = 0.0
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            steer_val = 180.0

        # --- THROTTLE LOGIC ---
        # Default stop (0)
        throttle_val = 0.0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            throttle_val = 10.0
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            # This is full "Reverse" if your ESC supports it
            throttle_val = -10.0 # Or 0 if you just want it to stop

        # --- SEND DATA ---
        message = f"S{steer_val} T{throttle_val}"
        sock.sendto(message.encode(), (ESP32_IP, ESP32_PORT))

        print(f"Steer: {steer_val:5} | Throttle: {throttle_val:5}", end="\n")

        # Exit on ESC
        if keys[pygame.K_ESCAPE]:
            break

        time.sleep(0.05) # 20Hz is plenty for keyboard

except KeyboardInterrupt:
    pass

print("\nStopping...")
pygame.quit()