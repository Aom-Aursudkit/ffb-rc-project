import numpy as np
import os

np.random.seed(42)

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, '..', 'data', 'ffb_tests', 'drift.csv')

num_samples = 600
times = np.arange(0, num_samples * 10, 10)

steer_current = 0.0
velocity = 0.3

accX_smooth = 0.0
accY_smooth = 0.0
accZ_smooth = 0.0
gyroX_smooth = 0.0
gyroY_smooth = 0.0
gyroZ_smooth = 0.0

lines = []

for i, t in enumerate(times):
    if t < 800:
        steer_target = 0.0
        velocity = velocity * 0.98 + 0.30 * 0.02
        accX_base = 0.0
        accY_base = 0.0

    elif t < 1300:
        ramp = (t - 800) / 500.0
        steer_target = 0.6 * ramp
        velocity = velocity * 0.98 + 0.28 * 0.02
        accX_base = ramp * 1.2
        accY_base = 0.0

    elif t < 1600:
        ramp = (t - 1300) / 300.0
        steer_target = 0.6 + 0.25 * ramp
        velocity = velocity * 0.96 + 0.20 * 0.04
        accX_base = 1.2 + np.sin(t * 0.02) * 0.3 * ramp
        accY_base = ramp * 6.0

    elif t < 3200:
        steer_target = 0.7 + np.sin(t * 0.004) * 0.2 + np.random.uniform(-0.05, 0.05)
        velocity = velocity * 0.96 + 0.12 * 0.04
        accX_base = 0.8 + np.sin(t * 0.01) * 0.5 + np.random.randn() * 0.1
        accY_base = 6.0 + np.sin(t * 0.008) * 0.5 + np.random.uniform(-0.3, 0.3)

    elif t < 3500:
        ramp = (t - 3200) / 300.0
        steer_target = 0.5 * (1 - ramp)
        velocity = velocity * 0.95 + 0.25 * 0.05
        accX_base = 0.8 * (1 - ramp) + np.sin(t * 0.01) * 0.3 * (1 - ramp)
        accY_base = 6.0 * (1 - ramp)

    else:
        steer_target = steer_target * 0.92
        velocity = velocity * 0.98 + 0.28 * 0.02
        accX_base = 0.0
        accY_base = 0.0

    steer_current = steer_current * 0.88 + steer_target * 0.12

    gyroZ_base = steer_current * 0.12
    if 1600 <= t < 3200:
        gyroZ_base += np.sin(t * 0.01) * 0.04

    accX_smooth = accX_smooth * 0.92 + accX_base * 0.08 + np.random.randn() * 0.015
    accY_smooth = accY_smooth * 0.92 + accY_base * 0.08 + np.random.randn() * 0.02
    accZ_smooth = accZ_smooth * 0.95 + np.random.randn() * 0.015
    gyroX_smooth = gyroX_smooth * 0.95 + np.random.randn() * 0.005
    gyroY_smooth = gyroY_smooth * 0.95 + np.random.randn() * 0.005
    gyroZ_smooth = gyroZ_smooth * 0.95 + gyroZ_base * 0.05 + np.random.randn() * 0.005

    threshold = 3.0 * (1 + abs(velocity))
    in_drift = abs(accY_smooth) > threshold

    ffb_base = steer_current * velocity * 20000
    ffb_force = ffb_base * (0.2 if in_drift else 1.0)
    ffb_force += np.random.randn() * 50
    ffb_force = max(-32767, min(32767, ffb_force))

    load_val = steer_current * 15.0 + np.random.randn() * 1.0

    line = f"Steer: {steer_current:.2f} | FFB: {ffb_force:.0f} | Vel: {velocity:.1f} | Load: {load_val:.1f}g | AccXYZ: {accX_smooth:.2f},{accY_smooth:.2f},{accZ_smooth:.2f} | GyroXYZ: {gyroX_smooth:.2f},{gyroY_smooth:.2f},{gyroZ_smooth:.2f}"
    lines.append(line)

with open(csv_path, 'w') as f:
    f.write('\n'.join(lines))

print(f"drift.csv created with {num_samples} samples")
print("Phase 1 (t=0-0.8s): straight, vel~0.30")
print("Phase 2 (t=0.8-1.3s): entering curve, steer ramps, accX builds to 1.2")
print("Phase 3 (t=1.3-1.6s): tires break loose, accY spikes to 6, vel drops")
print("Phase 4 (t=1.6-3.2s): full drift, accY~6, accX oscillates, vel~0.12")
print("Phase 5 (t=3.2-3.5s): recovery, accX/accY decay, vel recovers")
print("Phase 6 (t=3.5s+): straight again, vel~0.28")
