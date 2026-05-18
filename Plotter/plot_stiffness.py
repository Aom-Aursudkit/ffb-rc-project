import matplotlib.pyplot as plt
import numpy as np
from ffb_common import read_log_csv

CSV_FILE = "data/ffb_tests/stiffness.csv"
TITLE = "Steering Stiffness"

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

axes[0, 1].scatter(np.abs(steers), np.abs(ffb_forces), alpha=0.6, s=20)
axes[0, 1].set_xlabel('|Steering Angle|')
axes[0, 1].set_ylabel('|FFB Force|')
axes[0, 1].set_title('|FFB| vs |Steering Angle|')
axes[0, 1].grid(True, linestyle='--', alpha=0.5)

if len(steers) > 1:
    coef = np.polyfit(np.abs(steers), np.abs(ffb_forces), 1)
    x_fit = np.linspace(0, np.max(np.abs(steers)), 100)
    axes[0, 1].plot(x_fit, coef[0]*x_fit + coef[1], 'r--', label=f'Linear fit: K={coef[0]:.2f}')
    axes[0, 1].legend()

axes[1, 0].plot(times, steers, 'g-', linewidth=1.5)
axes[1, 0].set_xlabel('Time (s)')
axes[1, 0].set_ylabel('Steering Angle')
axes[1, 0].set_title('Steering Angle vs Time')
axes[1, 0].grid(True, linestyle='--', alpha=0.5)

axes[1, 1].scatter(steers, ffb_forces, c=np.abs(velocities), cmap='viridis', alpha=0.6, s=20)
axes[1, 1].set_xlabel('Steering Angle')
axes[1, 1].set_ylabel('FFB Force')
axes[1, 1].set_title('FFB vs Steering (color = velocity)')
axes[1, 1].grid(True, linestyle='--', alpha=0.5)
plt.colorbar(axes[1, 1].collections[0], ax=axes[1, 1], label='Velocity (m/s)')

plt.tight_layout()
plt.savefig(CSV_FILE.replace('.csv', '_result.png'), dpi=150)
plt.show()

print(f"\n=== Steering Stiffness Analysis ===")
print(f"Principle: Passive Stiffness = K x theta x sgn(theta_dot)")
print(f"Steering range: {np.min(steers):.2f} - {np.max(steers):.2f}")
print(f"FFB range: {np.min(ffb_forces):.2f} - {np.max(ffb_forces):.2f}")
print(f"Stiffness Coefficient (K): {coef[0]:.2f}")
print(f"Expected K: 500")
print(f"Interpretation: Resistance increases with steering angle")