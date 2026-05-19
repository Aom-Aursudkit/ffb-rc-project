import matplotlib.pyplot as plt
import numpy as np
from ffb_common import read_log_csv

CSV_FILE = "../data/ffb_tests/damping.csv"
TITLE = "Damping Force"

times, steers, velocities, loads, ffb_forces, accX, accY, accZ, gyroX, gyroY, gyroZ = read_log_csv(CSV_FILE)

if len(times) == 0:
    print("No data found!")
    exit()

times_sec = (times - times[0]) / 1000.0
dt = np.diff(times_sec) + 1e-6

steer_velocity_raw = np.diff(steers) / dt

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(TITLE, fontsize=14, fontweight='bold')

axes[0, 0].plot(times_sec, ffb_forces, 'b-', linewidth=1.5)
axes[0, 0].set_xlabel('Time (s)')
axes[0, 0].set_ylabel('FFB Force')
axes[0, 0].set_title('FFB vs Time')
axes[0, 0].grid(True, linestyle='--', alpha=0.5)

axes[0, 1].scatter(np.abs(steer_velocity_raw), np.abs(ffb_forces[1:]), alpha=0.6, s=20)
axes[0, 1].set_xlabel('|Steering Velocity| (raw units/s)')
axes[0, 1].set_ylabel('|FFB Force|')
axes[0, 1].set_title('|FFB| vs |Steering Velocity|')
axes[0, 1].grid(True, linestyle='--', alpha=0.5)

if len(steer_velocity_raw) > 1:
    coef = np.polyfit(np.abs(steer_velocity_raw), np.abs(ffb_forces[1:]), 1)
    x_fit = np.linspace(0, np.max(np.abs(steer_velocity_raw)), 100)
    axes[0, 1].plot(x_fit, coef[0]*x_fit + coef[1], 'r--', label=f'Linear fit: B={coef[0]:.2f}')
    axes[0, 1].legend()

axes[1, 0].plot(times_sec, steers, 'g-', linewidth=1.5)
axes[1, 0].set_xlabel('Time (s)')
axes[1, 0].set_ylabel('Steering Angle (raw)')
axes[1, 0].set_title('Steering Angle vs Time')
axes[1, 0].grid(True, linestyle='--', alpha=0.5)

axes[1, 1].plot(times_sec[1:], steer_velocity_raw, 'm-', linewidth=1.5)
axes[1, 1].set_xlabel('Time (s)')
axes[1, 1].set_ylabel('Steering Velocity (raw/s)')
axes[1, 1].set_title('Steering Velocity vs Time')
axes[1, 1].grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig(CSV_FILE.replace('.csv', '_result.png'), dpi=150)
plt.show()

print(f"\n=== Damping Force Analysis ===")
print(f"Principle: Damping = B x theta_dot (resistance proportional to angular velocity)")
print(f"Average FFB: {np.mean(ffb_forces):.2f}")
print(f"Steering Velocity range: {np.min(steer_velocity_raw):.4f} - {np.max(steer_velocity_raw):.4f}")
print(f"Damping Coefficient (B): {coef[0]:.2f}")
print(f"Expected B: 2000 (in raw units)")
print(f"Interpretation: Faster steering = Higher FFB")