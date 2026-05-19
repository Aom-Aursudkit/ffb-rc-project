import matplotlib.pyplot as plt
import numpy as np
from ffb_common import read_log_csv

CSV_FILE = "../data/ffb_tests/loadcell.csv"
TITLE = "Load Cell"

times, steers, velocities, loads, ffb_forces, accX, accY, accZ, gyroX, gyroY, gyroZ = read_log_csv(CSV_FILE)

if len(times) == 0:
    print("No data found!")
    exit()

times_sec = (times - times[0]) / 1000.0

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle(TITLE, fontsize=14, fontweight='bold')

axes[0].plot(times_sec, loads, 'b-', linewidth=1.5)
axes[0].set_xlabel('Time (s)')
axes[0].set_ylabel('Load Cell (g)')
axes[0].set_title('Load Cell vs Time')
axes[0].grid(True, linestyle='--', alpha=0.5)

axes[1].scatter(np.abs(steers), np.abs(loads), alpha=0.6, s=20)
axes[1].set_xlabel('|Steering Angle|')
axes[1].set_ylabel('|Load Cell (g)|')
axes[1].set_title('|Load| vs |Steering|')
axes[1].grid(True, linestyle='--', alpha=0.5)

if len(steers) > 1:
    coef = np.polyfit(np.abs(steers), np.abs(loads), 1)
    x_fit = np.linspace(0, np.max(np.abs(steers)), 100)
    axes[1].plot(x_fit, coef[0]*x_fit + coef[1], 'r--', label=f'Scale={coef[0]:.1f}')
    axes[1].legend()

axes[2].scatter(loads, ffb_forces, alpha=0.6, s=20)
axes[2].set_xlabel('Load Cell (g)')
axes[2].set_ylabel('FFB Force')
axes[2].set_title('FFB vs Load')
axes[2].grid(True, linestyle='--', alpha=0.5)

if len(loads) > 1:
    coef2 = np.polyfit(loads, ffb_forces, 1)
    x_fit = np.linspace(np.min(loads), np.max(loads), 100)
    axes[2].plot(x_fit, coef2[0]*x_fit + coef2[1], 'r--', label=f'K={coef2[0]:.0f}')
    axes[2].legend()

plt.tight_layout()
plt.savefig(CSV_FILE.replace('.csv', '_result.png'), dpi=150)
plt.show()

print(f"\n=== Load Cell Analysis ===")
print(f"Formula: Load Resistance = loadCell x GAIN_LOAD")
print(f"GAIN_LOAD = 2000")
print(f"Direction: opposes motion (sgn theta_dot)")
print(f"NOT dependent on car velocity")
print(f"Load range: {np.min(loads):.1f} to {np.max(loads):.1f} g")
print(f"FFB range: {np.min(ffb_forces):.0f} to {np.max(ffb_forces):.0f}")
print(f"K (slope): {coef2[0]:.0f} (expected ~2000)")
print(f"Scale Factor (|Load|/|Steer|): {coef[0]:.1f}")