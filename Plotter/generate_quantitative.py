import numpy as np
import os

np.random.seed(42)

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, '..', 'data', 'ffb_tests', 'quantitative_test.csv')

num_samples = 800
times = np.arange(0, num_samples * 10, 10)

steer_current = 0.0
velocity = 0.0
accX, accY, accZ = 0.0, 0.0, 0.0
gyroX, gyroY, gyroZ = 0.0, 0.0, 0.0
loadCell = 0.0

steer_target = 0.0
target_v = 0.0

GAIN_DAMPING = 2000
GAIN_FRICTION = 2000
GAIN_STIFFNESS = 1000
GAIN_LOAD = 500
GAIN_SAT = 20000
GAIN_GRAVITY = 1500
GAIN_SURFACE_JOLT = 500
DRIFT_THRESHOLD = 3.0

lines = []

steer_pattern = [
    (0, 1000, 0.0, 0.0),
    (1000, 2500, 0.6, 0.15),
    (2500, 4000, -0.4, 0.2),
    (4000, 5500, 0.8, 0.25),
    (5500, 6500, 0.0, 0.1),
    (6500, 8000, -0.7, 0.2),
]

road_events = [
    (1800, 1850, 'bump'),
    (3200, 3220, 'bump'),
    (4500, 4520, 'bump'),
    (5900, 5920, 'bump'),
]

drift_events = [
    (2600, 2800),
    (4800, 5100),
]

for i, t in enumerate(times):
    for start, end, target, v in steer_pattern:
        if start <= t < end:
            target_v = v * (0.9 + np.random.rand() * 0.2)
            steer_target = target + np.random.uniform(-0.02, 0.02)
            break
    else:
        target_v = 0.1
        steer_target = 0.0

    velocity = velocity * 0.98 + target_v * 0.02
    speed_factor = min(abs(velocity) * 2.0, 1.0)

    lag_prob = 0.02
    if np.random.rand() < lag_prob:
        pass
    else:
        steer_current = steer_current * 0.9 + steer_target * 0.1

    steer_current += np.random.randn() * 0.001 * (0.2 + abs(steer_current) * 3)

    prev_steer = steer_current
    steer_velocity = (steer_current - prev_steer) / 0.01

    accX = np.random.randn() * 0.15
    accY = np.random.randn() * 0.2
    accZ = np.random.randn() * 0.15
    gyroX = np.random.randn() * 0.5
    gyroY = np.random.randn() * 0.5
    gyroZ = np.random.randn() * 0.5

    for event_t, event_end, event_type in road_events:
        if event_t <= t < event_end:
            if event_type == 'bump':
                accZ += np.random.uniform(8, 15)
                accX += np.random.randn() * 2
                steer_current += np.random.uniform(-0.03, 0.03)
                steer_current = max(-1.0, min(1.0, steer_current))

    in_drift_override = False
    for event_t, event_end in drift_events:
        if event_t <= t < event_end:
            in_drift_override = True
            break

    if in_drift_override:
        accY = np.random.uniform(4.5, 6.0)

    threshold = DRIFT_THRESHOLD * (1 + abs(velocity))
    in_drift = abs(accY) > threshold
    drift_factor = 0.2 if in_drift else 1.0

    damping = steer_velocity * GAIN_DAMPING

    friction_mag = GAIN_FRICTION * (1.0 - speed_factor)
    if steer_velocity > 0.01:
        friction = friction_mag
    elif steer_velocity < -0.01:
        friction = -friction_mag
    else:
        friction = 0.0

    stiffness_mag = abs(steer_current) * GAIN_STIFFNESS
    if steer_velocity > 0:
        stiffness = stiffness_mag
    elif steer_velocity < 0:
        stiffness = -stiffness_mag
    else:
        stiffness = 0.0

    load_resistance = loadCell * GAIN_LOAD * (1 if steer_velocity > 0 else (-1 if steer_velocity < 0 else 0))

    sat = steer_current * speed_factor * GAIN_SAT

    gravity_torque = -accX * GAIN_GRAVITY

    surface_jolt = accZ * GAIN_SURFACE_JOLT

    ffb_passive = damping + friction + stiffness + load_resistance
    ffb_active = (sat + gravity_torque + surface_jolt) * drift_factor

    ffb_total = ffb_passive + ffb_active

    ffb_total += np.random.randn() * 200
    ffb_total = max(-32767, min(32767, ffb_total))

    accX += np.random.randn() * 0.1
    accY += np.random.randn() * 0.1
    accZ += np.random.randn() * 0.1
    gyroX += np.random.randn() * 0.3
    gyroY += np.random.randn() * 0.3
    gyroZ += np.random.randn() * 0.3

    line = f"Steer: {steer_current:.2f} | FFB: {ffb_total:.0f} | Vel: {velocity:.1f} | Load: {loadCell:.1f}g | AccXYZ: {accX:.2f},{accY:.2f},{accZ:.2f} | GyroXYZ: {gyroX:.2f},{gyroY:.2f},{gyroZ:.2f}"
    lines.append(line)

with open(csv_path, 'w') as f:
    f.write('\n'.join(lines))

print(f"quantitative_test.csv created with {num_samples} samples")
print("Human-like steering: lag, small tremor, smooth following")