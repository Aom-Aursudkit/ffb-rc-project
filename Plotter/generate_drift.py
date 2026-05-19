import numpy as np
import os

np.random.seed(42)

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, '..', 'data', 'ffb_tests', 'drift.csv')

num_samples = 600
times = np.arange(0, num_samples * 10, 10)

steer_current = 0.0
velocity = 0.2
accY_signal = 0.0
drift_threshold = 3.0

lines = []

for i, t in enumerate(times):
    if t < 1500:
        steer_target = 0.0
        velocity = 0.2
        accY_signal = 0.3 + np.random.randn() * 0.2
    elif t < 3000:
        steer_target = 0.7
        velocity = 0.25
        accY_signal = 4.5 + np.random.randn() * 0.5
    elif t < 4500:
        steer_target = -0.5
        velocity = 0.15
        accY_signal = 0.5 + np.random.randn() * 0.2
    else:
        steer_target = 0.0
        velocity = 0.1
        accY_signal = 0.2 + np.random.randn() * 0.1

    steer_current = steer_current * 0.85 + steer_target * 0.15

    threshold = drift_threshold * (1 + abs(velocity))
    in_drift = abs(accY_signal) > threshold

    ffb_base = steer_current * velocity * 20000
    if in_drift:
        ffb_force = ffb_base * 0.2
    else:
        ffb_force = ffb_base

    ffb_force += np.random.randn() * 200
    ffb_force = max(-32767, min(32767, ffb_force))

    accX = np.random.randn() * 0.1
    accZ = np.random.randn() * 0.1
    gyroX = np.random.randn() * 0.5
    gyroY = np.random.randn() * 0.5
    gyroZ = np.random.randn() * 0.5

    line = f"Steer: {steer_current:.2f} | FFB: {ffb_force:.0f} | Vel: {velocity:.1f} | Load: {np.random.randn()*5:.1f}g | AccXYZ: {accX:.2f},{accY_signal:.2f},{accZ:.2f} | GyroXYZ: {gyroX:.2f},{gyroY:.2f},{gyroZ:.2f}"
    lines.append(line)

with open(csv_path, 'w') as f:
    f.write('\n'.join(lines))

print(f"drift.csv created with {num_samples} samples")
print("Drift window: t=1.5s-3.0s (samples 150-300)")
print("accY ~4.5 during drift, threshold ~3.75 -> FFB x 0.2")