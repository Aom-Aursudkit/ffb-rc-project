import matplotlib.pyplot as plt
import numpy as np
from ffb_common import read_log_csv

CSV_FILE = "data/ffb_tests/loadcell.csv"
TITLE = "Load Cell"

times, steers, velocities, loads, ffb_forces, accX, accY, accZ, gyroX, gyroY, gyroZ = read_log_csv(CSV_FILE)

if len(times) == 0:
    print("No data found!")
    exit()

times = (times - times[0]) / 1000.0

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(TITLE, fontsize=14, fontweight='bold')

axes[0, 0].plot(times, loads, 'b-', linewidth=1.5)
axes[0, 0].set_xlabel('Time (s)')
axes[0, 0].set_ylabel('Load Cell (g)')
axes[0, 0].set_title('Load Cell vs Time')
axes[0, 0].grid(True, linestyle='--', alpha=0.5)

axes[0, 1].scatter(np.abs(steers), np.abs(loads), alpha=0.6, s=20)
axes[0, 1].set_xlabel('|Steering Angle|')
axes[0, 1].set_ylabel('|Load Cell (g)|')
axes[0, 1].set_title('|Load| vs |Steering Angle|')
axes[0, 1].grid(True, linestyle='--', alpha=0.5)

if len(steers) > 1:
    coef = np.polyfit(np.abs(steers), np.abs(loads), 1)
    x_fit = np.linspace(0, np.max(np.abs(steers)), 100)
    axes[0, 1].plot(x_fit, coef[0]*x_fit + coef[1], 'r--', label=f'Linear fit: {coef[0]:.2f}')
    axes[0, 1].legend()

axes[1, 0].plot(times, steers, 'g-', linewidth=1.5)
axes[1, 0].set_xlabel('Time (s)')
axes[1, 0].set_ylabel('Steering Angle')
axes[1, 0].set_title('Steering Angle vs Time')
axes[1, 0].grid(True, linestyle='--', alpha=0.5)

axes[1, 1].scatter(loads, ffb_forces, alpha=0.6, s=20)
axes[1, 1].set_xlabel('Load Cell (g)')
axes[1, 1].set_ylabel('FFB Force')
axes[1, 1].set_title('FFB vs Load Cell')
axes[1, 1].grid(True, linestyle='--', alpha=0.5)

if len(loads) > 1:
    coef2 = np.polyfit(loads, ffb_forces, 1)
    x_fit = np.linspace(np.min(loads), np.max(loads), 100)
    axes[1, 1].plot(x_fit, coef2[0]*x_fit + coef2[1], 'r--', label=f'Linear fit: K={coef2[0]:.2f}')
    axes[1, 1].legend()

plt.tight_layout()
plt.savefig(CSV_FILE.replace('.csv', '_result.png'), dpi=150)
plt.show()

print(f"\n=== Load Cell Analysis ===")
print(f"Principle: Load Resistance = K_load x L")
print(f"Load range: {np.min(loads):.2f} - {np.max(loads):.2f} g")
print(f"FFB range: {np.min(ffb_forces):.2f} - {np.max(ffb_forces):.2f}")
print(f"Load Coefficient (K): {coef2[0]:.2f}")
print(f"Expected K: 2000")
print(f"Interpretation: Load cell measures steering resistance directly")