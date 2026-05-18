import matplotlib.pyplot as plt
import numpy as np
from ffb_common import read_log_csv

CSV_FILE = "data/ffb_tests/sat.csv"
TITLE = "Self Aligning Torque"

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
axes[0, 0].set_title('FFB vs Time (SAT Self-Centering)')
axes[0, 0].grid(True, linestyle='--', alpha=0.5)

axes[0, 1].scatter(np.abs(steers), np.abs(ffb_forces), c=np.abs(velocities), cmap='viridis', alpha=0.6, s=20)
axes[0, 1].set_xlabel('|Steering Angle|')
axes[0, 1].set_ylabel('|FFB Force|')
axes[0, 1].set_title('|FFB| vs |Steering| (color = velocity)')
axes[0, 1].grid(True, linestyle='--', alpha=0.5)
plt.colorbar(axes[0, 1].collections[0], ax=axes[0, 1], label='Velocity (m/s)')

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

low_vel = velocities < 0.1
high_vel = velocities > 0.3
sat_low = np.mean(np.abs(ffb_forces[low_vel]))
sat_high = np.mean(np.abs(ffb_forces[high_vel]))

axes[1, 1].bar(['Low Speed\n(<0.1 m/s)', 'High Speed\n(>0.3 m/s)'],
               [sat_low, sat_high], color=['blue', 'red'], alpha=0.7)
axes[1, 1].set_ylabel('|FFB Force|')
axes[1, 1].set_title('SAT at Different Speeds')
axes[1, 1].grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig(CSV_FILE.replace('.csv', '_result.png'), dpi=150)
plt.show()

print(f"\n=== Self Aligning Torque Analysis ===")
print(f"Principle: SAT = K_center x theta (self-centering force)")
print(f"Steering range: {np.min(steers):.2f} - {np.max(steers):.2f}")
print(f"Velocity range: {np.min(velocities):.3f} - {np.max(velocities):.3f}")
print(f"SAT at low speed: {sat_low:.2f}")
print(f"SAT at high speed: {sat_high:.2f}")
print(f"SAT increased: {((sat_high - sat_low) / (sat_low + 1e-6) * 100):.1f}%")
print(f"Expected: SAT increases when speed_factor increases")
print(f"Interpretation: Self-centering effect stronger at higher speed")