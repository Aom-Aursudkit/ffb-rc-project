import numpy as np
import os

np.random.seed(42)

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, '..', 'data', 'ffb_tests', 'quantitative_test.csv')

num_samples = 800
times = np.arange(0, num_samples * 10, 10)

steer_current = 0.0
steer_prev = 0.0
velocity = 0.3
loadCell = 0.0

accX_smooth = 0.0
accY_smooth = 0.0
accZ_smooth = 0.0
gyroX_smooth = 0.0
gyroY_smooth = 0.0
gyroZ_smooth = 0.0

GAIN_DAMPING = 2000
GAIN_FRICTION = 2000
GAIN_STIFFNESS = 1000
GAIN_LOAD = 500
GAIN_SAT = 20000
GAIN_GRAVITY = 1500
GAIN_SURFACE_JOLT = 500
DRIFT_THRESHOLD = 3.0

lines = []

speed_profile = [
    (0, 500, 0.32),
    (500, 1200, 0.28),
    (1200, 1800, 0.35),
    (1800, 2400, 0.22),
    (2400, 3000, 0.15),
    (3000, 3600, 0.30),
    (3600, 4200, 0.25),
    (4200, 4800, 0.18),
    (4800, 5400, 0.33),
    (5400, 6000, 0.20),
    (6000, 6600, 0.28),
    (6600, 7200, 0.15),
    (7200, 8000, 0.30),
]

steer_profile = [
    (0, 500, 0.0),
    (500, 1000, 0.4),
    (1000, 1500, -0.3),
    (1500, 1800, 0.0),
    (1800, 2200, 0.6),
    (2200, 2600, -0.5),
    (2600, 3000, 0.0),
    (3000, 3500, 0.7),
    (3500, 4000, -0.6),
    (4000, 4500, 0.0),
    (4500, 5000, 0.5),
    (5000, 5500, -0.4),
    (5500, 6000, 0.0),
    (6000, 6500, 0.6),
    (6500, 7000, -0.3),
    (7000, 8000, 0.0),
]

road_events = [
    (800, 840, 'bump'),
    (2000, 2030, 'bump'),
    (3400, 3440, 'bump'),
    (4600, 4630, 'bump'),
    (5200, 5220, 'rough'),
]

drift_events = [
    (2100, 2400),
    (3800, 4100),
]

for i, t in enumerate(times):
    target_speed = 0.3
    for start, end, v in speed_profile:
        if start <= t < end:
            target_speed = v
            break

    velocity = velocity * 0.95 + target_speed * 0.05
    velocity += np.random.randn() * 0.005
    velocity = max(0.1, min(0.35, velocity))

    steer_target = 0.0
    for start, end, s in steer_profile:
        if start <= t < end:
            ramp = min((t - start) / 150.0, 1.0)
            steer_target = s * ramp
            break

    steer_target += np.random.uniform(-0.02, 0.02)

    steer_prev = steer_current

    if np.random.rand() < 0.02:
        pass
    else:
        steer_current = steer_current * 0.90 + steer_target * 0.10

    tremor = np.random.randn() * 0.001 * (0.2 + abs(steer_current) * 2)
    steer_current += tremor
    steer_current = max(-1.0, min(1.0, steer_current))

    steer_velocity = (steer_current - steer_prev) / 0.01

    speed_factor = min(abs(velocity) * 2.0, 1.0)

    lateral_acc = steer_current * velocity * 2.0
    accX_base = lateral_acc
    accY_base = 0.0
    accZ_base = 0.0

    gyroX_base = 0.0
    gyroY_base = velocity * 0.05
    gyroZ_base = steer_current * 0.1

    in_drift_override = False
    drift_intensity = 0.0
    for event_t, event_end in drift_events:
        if event_t <= t < event_end:
            in_drift_override = True
            ramp_in = min((t - event_t) / 60.0, 1.0)
            ramp_out = max(1.0 - (t - event_end + 60) / 60.0, 0.0) if t > event_end - 60 else 1.0
            drift_intensity = min(ramp_in, ramp_out) if t > event_end - 60 else ramp_in
            break

    if in_drift_override:
        accY_base = 6.0 * drift_intensity + np.random.uniform(-0.3, 0.3) * drift_intensity
        accX_base = 0.8 + np.sin(t * 0.01) * 0.5 + np.random.randn() * 0.1
        gyroZ_base += np.sin(t * 0.012) * 0.04 * drift_intensity
        velocity = velocity * 0.93 + 0.12 * 0.07

    for event_t, event_end, event_type in road_events:
        if event_t <= t < event_end:
            if event_type == 'bump':
                accZ_base += np.random.uniform(4, 8)
                accX_base += np.random.randn() * 0.3
            elif event_type == 'rough':
                accZ_base += np.random.uniform(1, 3)

    accX_smooth = accX_smooth * 0.92 + accX_base * 0.08 + np.random.randn() * 0.015
    accY_smooth = accY_smooth * 0.92 + accY_base * 0.08 + np.random.randn() * 0.02
    accZ_smooth = accZ_smooth * 0.95 + accZ_base * 0.05 + np.random.randn() * 0.015
    gyroX_smooth = gyroX_smooth * 0.95 + gyroX_base * 0.05 + np.random.randn() * 0.005
    gyroY_smooth = gyroY_smooth * 0.95 + gyroY_base * 0.05 + np.random.randn() * 0.005
    gyroZ_smooth = gyroZ_smooth * 0.95 + gyroZ_base * 0.05 + np.random.randn() * 0.005

    threshold = DRIFT_THRESHOLD * (1 + abs(velocity))
    in_drift = abs(accY_smooth) > threshold
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

    loadCell = steer_current * 12.0 + np.random.randn() * 1.0
    load_resistance = loadCell * GAIN_LOAD * (1 if steer_velocity > 0 else (-1 if steer_velocity < 0 else 0))

    sat = steer_current * speed_factor * GAIN_SAT

    gravity_torque = -accX_smooth * GAIN_GRAVITY

    surface_jolt = accZ_smooth * GAIN_SURFACE_JOLT

    ffb_passive = damping + friction + stiffness + load_resistance
    ffb_active = (sat + gravity_torque + surface_jolt) * drift_factor

    ffb_total = ffb_passive + ffb_active

    ffb_total += np.random.randn() * 50
    ffb_total = max(-32767, min(32767, ffb_total))

    line = f"Steer: {steer_current:.2f} | FFB: {ffb_total:.0f} | Vel: {velocity:.1f} | Load: {loadCell:.1f}g | AccXYZ: {accX_smooth:.2f},{accY_smooth:.2f},{accZ_smooth:.2f} | GyroXYZ: {gyroX_smooth:.2f},{gyroY_smooth:.2f},{gyroZ_smooth:.2f}"
    lines.append(line)

with open(csv_path, 'w') as f:
    f.write('\n'.join(lines))

print(f"quantitative_test.csv created with {num_samples} samples")
print("Velocity range: 0.1-0.35 m/s with natural variation")
print("Drift events at t=2.1-2.4s and t=3.8-4.1s with buildup")
