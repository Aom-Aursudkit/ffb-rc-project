import matplotlib.pyplot as plt
import numpy as np
from ffb_common import read_log_csv

CSV_FILE = "data/ffb_tests/friction.csv"
TITLE = "Friction Force"

times, steers, velocities, loads, ffb_forces, accX, accY, accZ, gyroX, gyroY, gyroZ = read_log_csv(CSV_FILE)

if len(times) == 0:
    print("No data found!")
    exit()

times = (times - times[0]) / 1000.0

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(TITLE, fontsize=14, fontweight='bold')

axes[0, 0].plot(times, ffb_forces, 'b-', linewidth=1.5)
axes[0, 0].set_xlabel('Time (s)')
axes[0, 0].set_ylabel('FFB Force')
axes[0, 0].set_title('FFB vs Time')
axes[0, 0].grid(True, linestyle='--', alpha=0.5)

axes[0, 1].scatter(np.abs(velocities), np.abs(ffb_forces), alpha=0.6, s=20)
axes[0, 1].set_xlabel('Velocity (m/s)')
axes[0, 1].set_ylabel('|FFB Force|')
axes[0, 1].set_title('|FFB| vs Velocity (should decrease with speed)')
axes[0, 1].grid(True, linestyle='--', alpha=0.5)

axes[1, 0].plot(times, steers, 'g-', linewidth=1.5)
axes[1, 0].set_xlabel('Time (s)')
axes[1, 0].set_ylabel('Steering Angle')
axes[1, 0].set_title('Steering Angle vs Time')
axes[1, 0].grid(True, linestyle='--', alpha=0.5)

friction_at_low_speed = np.mean(np.abs(ffb_forces[velocities < 0.1]))
friction_at_high_speed = np.mean(np.abs(ffb_forces[velocities > 0.3]))

axes[1, 1].bar(['Low Speed\n(<0.1 m/s)', 'High Speed\n(>0.3 m/s)'],
               [friction_at_low_speed, friction_at_high_speed], color=['blue', 'red'], alpha=0.7)
axes[1, 1].set_ylabel('|FFB Force|')
axes[1, 1].set_title('Friction at Different Speeds')
axes[1, 1].grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig(CSV_FILE.replace('.csv', '_result.png'), dpi=150)
plt.show()

print(f"\n=== Friction Force Analysis ===")
print(f"Principle: Friction = T_fric x sgn(theta_dot)")
print(f"Friction at low speed: {friction_at_low_speed:.2f}")
print(f"Friction at high speed: {friction_at_high_speed:.2f}")
print(f"Friction decreased: {((friction_at_low_speed - friction_at_high_speed) / friction_at_low_speed * 100):.1f}%")
print(f"Expected: Friction decreases when speed_factor increases")
print(f"Interpretation: At high speed, friction should be lower")