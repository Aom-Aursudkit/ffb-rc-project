import numpy as np
import os

np.random.seed(42)

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, '..', 'data', 'ffb_tests', 'friction.csv')

num_samples = 500
times = np.arange(0, num_samples * 10, 10)

steer_history = [0.0]
steer_current = 0.0
velocity = 0.0

lines = []

GAIN_FRICTION = 2000

for i, t in enumerate(times):
    if t < 1000:
        steer_target = 0.0
        velocity = 0.0
    elif t < 2000:
        steer_target = 0.5
        velocity = 0.05
    elif t < 3000:
        steer_target = 0.8
        velocity = 0.15
    elif t < 4000:
        steer_target = 0.3
        velocity = 0.2
    else:
        steer_target = 0.0
        velocity = 0.1

    prev_steer = steer_current
    steer_current = steer_current * 0.9 + steer_target * 0.1
    steer_velocity = (steer_current - prev_steer) / 0.01

    speed_factor = min(abs(velocity) * 2.0, 1.0)
    friction_mag = GAIN_FRICTION * (1.0 - speed_factor)

    if steer_velocity > 0.01:
        friction = -friction_mag
    elif steer_velocity < -0.01:
        friction = friction_mag
    else:
        friction = 0.0

    friction += np.random.randn() * 100

    accX = 0.0
    accY = 0.0
    accZ = 0.0
    gyroX = 0.0
    gyroY = 0.0
    gyroZ = 0.0

    line = f"Steer: {steer_current:.2f} | FFB: {friction:.0f} | Vel: {velocity:.1f} | Load: {np.random.randn()*5:.1f}g | AccXYZ: {accX:.2f},{accY:.2f},{accZ:.2f} | GyroXYZ: {gyroX:.2f},{gyroY:.2f},{gyroZ:.2f}"
    lines.append(line)

with open(csv_path, 'w') as f:
    f.write('\n'.join(lines))

print(f"friction.csv created with {num_samples} samples")
print("steer_velocity = d(steer)/dt, friction opposes motion (sgn opposite to steer_vel)")