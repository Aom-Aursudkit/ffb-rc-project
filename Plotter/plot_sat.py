import matplotlib.pyplot as plt
import numpy as np
from ffb_common import read_log_csv

CSV_FILE = "../data/ffb_tests/sat.csv"
TITLE = "Self Aligning Torque"

times, steers, velocities, loads, ffb_forces, accX, accY, accZ, gyroX, gyroY, gyroZ = read_log_csv(CSV_FILE)

if len(times) == 0:
    print("No data found!")
    exit()

times_sec = (times - times[0]) / 1000.0

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle(TITLE, fontsize=14, fontweight='bold')

axes[0].plot(times_sec, ffb_forces, 'b-', linewidth=1.5)
axes[0].set_xlabel('Time (s)')
axes[0].set_ylabel('FFB Force')
axes[0].set_title('FFB vs Time')
axes[0].grid(True, linestyle='--', alpha=0.5)

axes[1].scatter(np.abs(steers), np.abs(ffb_forces), c=np.abs(velocities), cmap='viridis', alpha=0.6, s=20)
axes[1].set_xlabel('|Steering Angle|')
axes[1].set_ylabel('|FFB Force|')
axes[1].set_title('|FFB| vs |Steering| (color = |velocity|)')
axes[1].grid(True, linestyle='--', alpha=0.5)
plt.colorbar(axes[1].collections[0], ax=axes[1], label='|Velocity| (m/s)')

axes[2].scatter(velocities, np.abs(ffb_forces), alpha=0.6, s=20)
axes[2].set_xlabel('Car Velocity (m/s)')
axes[2].set_ylabel('|FFB Force|')
axes[2].set_title('|FFB| vs Car Velocity')
axes[2].grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig(CSV_FILE.replace('.csv', '_result.png'), dpi=150)
plt.show()

print(f"\n=== Self Aligning Torque Analysis ===")
print(f"Formula: SAT = steer_raw x speed_factor x GAIN_SAT")
print(f"GAIN_SAT = 20000")
print(f"Depends on both steering angle AND car velocity")
print(f"Speed Factor = min(|velocity| x 2, 1)")
print(f"Steering: {np.min(steers):.2f} to {np.max(steers):.2f}")
print(f"Car Velocity: {np.min(velocities):.3f} to {np.max(velocities):.3f}")
print(f"FFB: {np.min(ffb_forces):.0f} to {np.max(ffb_forces):.0f}")
print(f"Key check: FFB should increase with BOTH steering and velocity")