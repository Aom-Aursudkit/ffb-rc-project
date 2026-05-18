import matplotlib.pyplot as plt
import numpy as np
from ffb_common import read_log_csv

CSV_FILE = "data/ffb_tests/drift.csv"
TITLE = "Drift Detection"

times, steers, velocities, loads, ffb_forces, accX, accY, accZ, gyroX, gyroY, gyroZ = read_log_csv(CSV_FILE)

if len(times) == 0:
    print("No data found!")
    exit()

times = (times - times[0]) / 1000.0

threshold_multiplier = 3.0
thresholds = threshold_multiplier * (1 + np.abs(velocities))
in_drift = np.abs(accY) > thresholds

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(TITLE, fontsize=14, fontweight='bold')

axes[0, 0].plot(times, ffb_forces, 'b-', linewidth=1.5, label='FFB')
axes[0, 0].set_xlabel('Time (s)')
axes[0, 0].set_ylabel('FFB Force')
axes[0, 0].set_title('FFB vs Time')
axes[0, 0].grid(True, linestyle='--', alpha=0.5)
axes[0, 0].legend()

axes[0, 1].plot(times, accY, 'r-', linewidth=1.5, label='accY')
axes[0, 1].plot(times, thresholds, 'g--', linewidth=1, label='Threshold')
axes[0, 1].plot(times, -thresholds, 'g--', linewidth=1)
axes[0, 1].set_xlabel('Time (s)')
axes[0, 1].set_ylabel('accY (m/s^2)')
axes[0, 1].set_title('accY vs Threshold')
axes[0, 1].legend()
axes[0, 1].grid(True, linestyle='--', alpha=0.5)

axes[1, 0].scatter(np.abs(accY), ffb_forces, c=velocities, cmap='viridis', alpha=0.6, s=20)
axes[1, 0].set_xlabel('|accY| (m/s^2)')
axes[1, 0].set_ylabel('FFB Force')
axes[1, 0].set_title('FFB vs |accY| (color = velocity)')
axes[1, 0].grid(True, linestyle='--', alpha=0.5)
plt.colorbar(axes[1, 0].collections[0], ax=axes[1, 0], label='Velocity (m/s)')

normal_idx = ~in_drift
drift_idx = in_drift
ffb_normal = ffb_forces[normal_idx]
ffb_drift = ffb_forces[drift_idx]

axes[1, 1].bar(['Normal\n(|accY| < threshold)', 'Drift\n(|accY| > threshold)'],
               [np.mean(np.abs(ffb_normal)), np.mean(np.abs(ffb_drift))],
               color=['green', 'red'], alpha=0.7)
axes[1, 1].set_ylabel('Mean |FFB Force|')
axes[1, 1].set_title('FFB Normal vs Drift')
axes[1, 1].grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig(CSV_FILE.replace('.csv', '_result.png'), dpi=150)
plt.show()

ffb_reduction = (1 - np.mean(np.abs(ffb_drift)) / (np.mean(np.abs(ffb_normal)) + 1e-6)) * 100

print(f"\n=== Drift Detection Analysis ===")
print(f"Principle: if |accY| > 3.0 x (1 + |velocity|) then FFB reduces 80%")
print(f"Normal data points: {len(ffb_normal)}")
print(f"Drift data points: {len(ffb_drift)}")
print(f"FFB normal (mean): {np.mean(np.abs(ffb_normal)):.2f}")
print(f"FFB during drift (mean): {np.mean(np.abs(ffb_drift)):.2f}")
print(f"FFB reduction: {ffb_reduction:.1f}%")
print(f"Expected: FFB reduces ~80% during drift")
print(f"Interpretation: When lateral slip detected, reduce active FFB")