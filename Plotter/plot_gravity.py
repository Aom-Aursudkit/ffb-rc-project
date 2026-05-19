import matplotlib.pyplot as plt
import numpy as np
from ffb_common import read_log_csv

CSV_FILE = "../data/ffb_tests/gravity.csv"
TITLE = "Gravity Torque"

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

axes[0, 1].scatter(accX, ffb_forces, alpha=0.6, s=20)
axes[0, 1].set_xlabel('accX (m/s^2)')
axes[0, 1].set_ylabel('FFB Force')
axes[0, 1].set_title('FFB vs accX')
axes[0, 1].grid(True, linestyle='--', alpha=0.5)

if len(accX) > 1:
    coef = np.polyfit(accX, ffb_forces, 1)
    x_fit = np.linspace(np.min(accX), np.max(accX), 100)
    axes[0, 1].plot(x_fit, coef[0]*x_fit + coef[1], 'r--', label=f'Linear fit: G={coef[0]:.2f}')
    axes[0, 1].legend()

axes[1, 0].plot(times, accX, 'g-', linewidth=1.5)
axes[1, 0].set_xlabel('Time (s)')
axes[1, 0].set_ylabel('accX (m/s^2)')
axes[1, 0].set_title('accX vs Time')
axes[1, 0].grid(True, linestyle='--', alpha=0.5)

axes[1, 1].plot(times, steers, 'm-', linewidth=1.5)
axes[1, 1].set_xlabel('Time (s)')
axes[1, 1].set_ylabel('Steering Angle')
axes[1, 1].set_title('Steering Angle vs Time')
axes[1, 1].grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig(CSV_FILE.replace('.csv', '_result.png'), dpi=150)
plt.show()

print(f"\n=== Gravity Torque Analysis ===")
print(f"Principle: Gravity = accX x G_x (compensates for vehicle tilt)")
print(f"accX range: {np.min(accX):.2f} - {np.max(accX):.2f} m/s^2")
print(f"FFB range: {np.min(ffb_forces):.2f} - {np.max(ffb_forces):.2f}")
print(f"Gravity Gain (G): {coef[0]:.2f}")
print(f"Expected G: 1500")
print(f"Interpretation: FFB compensates for steering wheel weight on slopes")