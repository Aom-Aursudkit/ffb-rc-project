import matplotlib.pyplot as plt
import numpy as np
from ffb_common import read_log_csv

CSV_FILE = "../data/ffb_tests/friction.csv"
TITLE = "Friction Force"

times, steers, velocities, loads, ffb_forces, accX, accY, accZ, gyroX, gyroY, gyroZ = read_log_csv(CSV_FILE)

if len(times) == 0:
    print("No data found!")
    exit()

times_sec = (times - times[0]) / 1000.0
steer_velocity = np.diff(steers) / np.diff(times_sec / 1000)
steer_velocity = np.concatenate([[0], steer_velocity])

speed_factor = np.minimum(np.abs(velocities) * 2, 1.0)

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle(TITLE, fontsize=14, fontweight='bold')

axes[0, 0].plot(times_sec, ffb_forces, 'b-', linewidth=1)
axes[0, 0].set_xlabel('Time (s)')
axes[0, 0].set_ylabel('FFB Force')
axes[0, 0].set_title('FFB Force vs Time')
axes[0, 0].grid(True, linestyle='--', alpha=0.5)

axes[0, 1].scatter(steer_velocity, ffb_forces, c=speed_factor, cmap='coolwarm', alpha=0.6, s=20)
axes[0, 1].set_xlabel('Steer Velocity (rad/s)')
axes[0, 1].set_ylabel('FFB Force')
axes[0, 1].set_title('FFB vs Steer Velocity')
axes[0, 1].axhline(y=0, color='k', linestyle='-', linewidth=0.5)
axes[0, 1].grid(True, linestyle='--', alpha=0.5)
cbar = plt.colorbar(axes[0, 1].collections[0], ax=axes[0, 1])
cbar.set_label('speed_factor')

axes[1, 0].scatter(velocities, ffb_forces, alpha=0.6, s=20)
axes[1, 0].set_xlabel('Car Velocity (m/s)')
axes[1, 0].set_ylabel('FFB Force')
axes[1, 0].set_title('FFB vs Car Velocity')
axes[1, 0].grid(True, linestyle='--', alpha=0.5)

low_mask = velocities < 0.1
high_mask = velocities > 0.15
axes[1, 1].bar(['Low (<0.1)', 'High (>0.15)'],
               [np.mean(np.abs(ffb_forces[low_mask])), np.mean(np.abs(ffb_forces[high_mask]))],
               color=['blue', 'red'], alpha=0.7, width=0.6)
axes[1, 1].set_ylabel('Mean |FFB Force|')
axes[1, 1].set_title('Friction at Different Speeds')
axes[1, 1].grid(True, linestyle='--', alpha=0.5)

for ax in axes.flat:
    ax.set_xlabel(ax.get_xlabel(), fontsize=10)

plt.tight_layout()
plt.savefig(CSV_FILE.replace('.csv', '_result.png'), dpi=150)
plt.show()

print(f"\n=== Friction Analysis ===")
print(f"Formula: Friction = 2000 x (1 - speed_factor) x sgn(steer_vel)")
print(f"speed_factor = min(|velocity| x 2, 1)")
print(f"Low speed (<0.1): mean |FFB| = {np.mean(np.abs(ffb_forces[low_mask])):.0f}")
print(f"High speed (>0.15): mean |FFB| = {np.mean(np.abs(ffb_forces[high_mask])):.0f}")