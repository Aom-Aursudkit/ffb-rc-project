import matplotlib.pyplot as plt
import numpy as np
import os
from ffb_common import read_log_csv

script_dir = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(script_dir, '..', 'data', 'ffb_tests', 'sat.csv')
TITLE = "Self Aligning Torque"

times, steers, velocities, loads, ffb_forces, accX, accY, accZ, gyroX, gyroY, gyroZ = read_log_csv(CSV_FILE)

if len(times) == 0:
    print("No data found!")
    exit()

times_sec = (times - times[0]) / 1000.0

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle(TITLE, fontsize=14, fontweight='bold')

axes[0, 0].plot(times_sec, steers, 'b-', linewidth=1)
axes[0, 0].set_xlabel('Time (s)')
axes[0, 0].set_ylabel('Steering Angle')
axes[0, 0].set_title('Steering Angle vs Time')
axes[0, 0].grid(True, linestyle='--', alpha=0.5)

axes[0, 1].plot(times_sec, ffb_forces, 'r-', linewidth=1)
axes[0, 1].set_xlabel('Time (s)')
axes[0, 1].set_ylabel('FFB Force')
axes[0, 1].set_title('FFB vs Time')
axes[0, 1].grid(True, linestyle='--', alpha=0.5)

axes[1, 0].plot(times_sec, velocities, 'g-', linewidth=1)
axes[1, 0].set_xlabel('Time (s)')
axes[1, 0].set_ylabel('Car Velocity (m/s)')
axes[1, 0].set_title('Car Velocity vs Time')
axes[1, 0].grid(True, linestyle='--', alpha=0.5)

axes[1, 1].scatter(velocities, np.abs(ffb_forces), alpha=0.6, s=20)
axes[1, 1].set_xlabel('Car Velocity (m/s)')
axes[1, 1].set_ylabel('|FFB Force|')
axes[1, 1].set_title('|FFB| vs Car Velocity')
axes[1, 1].grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
out_path = CSV_FILE.replace('.csv', '_result.png')
plt.savefig(out_path, dpi=150)
print(f"Saved: {out_path}")

print(f"\n=== Self Aligning Torque Analysis ===")
print(f"Formula: SAT = steer_raw x speed_factor x GAIN_SAT")
print(f"GAIN_SAT = 20000")
print(f"Depends on both steering angle AND car velocity")
print(f"Speed Factor = min(|velocity| x 2, 1)")
print(f"Steering: {np.min(steers):.2f} to {np.max(steers):.2f}")
print(f"Car Velocity: {np.min(velocities):.3f} to {np.max(velocities):.3f}")
print(f"FFB: {np.min(ffb_forces):.0f} to {np.max(ffb_forces):.0f}")
print(f"Key check: FFB should increase with BOTH steering and velocity")