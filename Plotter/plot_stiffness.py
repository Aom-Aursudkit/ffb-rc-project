import matplotlib.pyplot as plt
import numpy as np
from ffb_common import read_log_csv

CSV_FILE = "../data/ffb_tests/stiffness.csv"
TITLE = "Steering Stiffness"

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

axes[1].scatter(np.abs(steers), np.abs(ffb_forces), alpha=0.6, s=20)
axes[1].set_xlabel('|Steering Angle|')
axes[1].set_ylabel('|FFB Force|')
axes[1].set_title('|FFB| vs |Steering Angle|')
axes[1].grid(True, linestyle='--', alpha=0.5)

if len(steers) > 1:
    coef = np.polyfit(np.abs(steers), np.abs(ffb_forces), 1)
    x_fit = np.linspace(0, np.max(np.abs(steers)), 100)
    axes[1].plot(x_fit, coef[0]*x_fit + coef[1], 'r--', label=f'K={coef[0]:.0f}')
    axes[1].legend()

axes[2].plot(times_sec, steers, 'g-', linewidth=1.5)
axes[2].set_xlabel('Time (s)')
axes[2].set_ylabel('Steering Angle')
axes[2].set_title('Steering Angle vs Time')
axes[2].grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig(CSV_FILE.replace('.csv', '_result.png'), dpi=150)
plt.show()

print(f"\n=== Steering Stiffness Analysis ===")
print(f"Formula: |steer_raw| x GAIN_STIFFNESS (NOT velocity dependent)")
print(f"GAIN_STIFFNESS = 1000")
print(f"Steering: {np.min(steers):.2f} to {np.max(steers):.2f}")
print(f"FFB: {np.min(ffb_forces):.0f} to {np.max(ffb_forces):.0f}")
print(f"K (slope): {coef[0]:.0f} (expected ~1000)")