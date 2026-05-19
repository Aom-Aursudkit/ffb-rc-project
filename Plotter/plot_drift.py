import matplotlib.pyplot as plt
import numpy as np
import os
from ffb_common import read_log_csv

script_dir = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(script_dir, '..', 'data', 'ffb_tests', 'drift.csv')
TITLE = "Drift Detection"

times, steers, velocities, loads, ffb_forces, accX, accY, accZ, gyroX, gyroY, gyroZ = read_log_csv(CSV_FILE)

if len(times) == 0:
    print("No data found!")
    exit()

times_sec = (times - times[0]) / 1000.0

threshold_multiplier = 3.0
thresholds = threshold_multiplier * (1 + np.abs(velocities))
in_drift = np.abs(accY) > thresholds

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle(TITLE, fontsize=14, fontweight='bold')

axes[0, 0].plot(times_sec, ffb_forces, 'b-', linewidth=1)
axes[0, 0].set_xlabel('Time (s)')
axes[0, 0].set_ylabel('FFB Force')
axes[0, 0].set_title('FFB Force vs Time')
axes[0, 0].grid(True, linestyle='--', alpha=0.5)

axes[0, 1].plot(times_sec, accY, 'r-', linewidth=1, label='accY')
axes[0, 1].plot(times_sec, thresholds, 'g--', linewidth=1, label='Threshold')
axes[0, 1].plot(times_sec, -thresholds, 'g--', linewidth=1)
axes[0, 1].fill_between(times_sec, -thresholds, thresholds, alpha=0.2, color='green', label='Safe zone')
axes[0, 1].set_xlabel('Time (s)')
axes[0, 1].set_ylabel('accY (m/s^2)')
axes[0, 1].set_title('accY vs Threshold (Safe Zone)')
axes[0, 1].legend()
axes[0, 1].grid(True, linestyle='--', alpha=0.5)

axes[1, 0].scatter(velocities[in_drift], ffb_forces[in_drift], c='red', alpha=0.6, s=20, label='Drift')
axes[1, 0].scatter(velocities[~in_drift], ffb_forces[~in_drift], c='green', alpha=0.4, s=20, label='Normal')
axes[1, 0].set_xlabel('Car Velocity (m/s)')
axes[1, 0].set_ylabel('FFB Force')
axes[1, 0].set_title('FFB vs Velocity (Drift vs Normal)')
axes[1, 0].legend()
axes[1, 0].grid(True, linestyle='--', alpha=0.5)

drift_normalized = np.where(in_drift, ffb_forces / (np.abs(steers) * np.abs(velocities) * 20000 + 1e-6), np.nan)
mask = ~np.isnan(drift_normalized)
axes[1, 1].plot(times_sec[mask], drift_normalized[mask], 'purple', linewidth=1)
axes[1, 1].set_xlabel('Time (s)')
axes[1, 1].set_ylabel('FFB / (Steer x Vel x 20000)')
axes[1, 1].set_title('FFB Ratio (should drop to ~0.2 during drift)')
axes[1, 1].grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
out_path = CSV_FILE.replace('.csv', '_result.png')
plt.savefig(out_path, dpi=150)
print(f"Saved: {out_path}")

print(f"\n=== Drift Detection Analysis ===")
print(f"Formula: if |accY| > 3.0 x (1 + |v|) then FFB x 0.2")
print(f"Normal points: {np.sum(~in_drift)}")
print(f"Drift points: {np.sum(in_drift)}")
print(f"FFB normal mean: {np.mean(np.abs(ffb_forces[~in_drift])):.0f}")
print(f"FFB drift mean: {np.mean(np.abs(ffb_forces[in_drift])):.0f}")
if np.mean(np.abs(ffb_forces[~in_drift])) > 0:
    print(f"Reduction ratio: {np.mean(np.abs(ffb_forces[in_drift])) / np.mean(np.abs(ffb_forces[~in_drift])):.2f}")