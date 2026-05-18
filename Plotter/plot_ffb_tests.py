import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

data_dir = Path(__file__).parent.parent / "data" / "ffb_tests"
output_dir = Path(__file__).parent / "ffb_plots"
output_dir.mkdir(parents=True, exist_ok=True)

plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10

# 1. Steering Stiffness Test
# X: Steering Angle (deg), Y: FFB Force
# Expected: FFB proportional to |theta|, FFB -> 0 when theta -> 0
df_stiff = pd.read_csv(data_dir / "steering_stiffness.csv")
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(df_stiff['Steering_Angle_deg'], df_stiff['FFB_Force']/1000, 'b.-', linewidth=1.5, markersize=6)
ax.axhline(y=0, color='k', linewidth=0.5)
ax.axvline(x=0, color='k', linewidth=0.5)
ax.set_xlabel("Steering Angle (°)")
ax.set_ylabel("FFB Force (kN)")
ax.set_title("Steering Stiffness Test: FFB vs Steering Angle")
ax.grid(True, alpha=0.3)

# Add trend line and equation
mask = df_stiff['Steering_Angle_deg'] > 0
slope_pos = np.polyfit(df_stiff.loc[mask, 'Steering_Angle_deg'], df_stiff.loc[mask, 'FFB_Force'], 1)
x_trend = np.linspace(0, 90, 50)
ax.plot(x_trend, np.polyval(slope_pos, x_trend)/1000, 'r--', alpha=0.7, label=f'Slope = {slope_pos[0]:.0f}')
ax.legend()
ax.annotate(f"Stiffness = {slope_pos[0]:.0f}\n(Expected: 2000-10000)", xy=(60, 100), fontsize=9)

plt.tight_layout()
plt.savefig(output_dir / "steering_stiffness.png", dpi=150)
plt.close()
print("Saved: steering_stiffness.png")

# 2. Damping Test
# X: Steering Velocity (deg/s), Y: FFB Force
# Expected: FFB proportional to |velocity|, B ~ 500
df_damp = pd.read_csv(data_dir / "damping.csv")
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(df_damp['Steering_Velocity_deg_s'], df_damp['FFB_Force']/1000, 'g.-', linewidth=1.5, markersize=6)
ax.axhline(y=0, color='k', linewidth=0.5)
ax.axvline(x=0, color='k', linewidth=0.5)
ax.set_xlabel("Steering Velocity (°/s)")
ax.set_ylabel("FFB Force (kN)")
ax.set_title("Damping Test: FFB vs Steering Velocity")
ax.grid(True, alpha=0.3)

# Fit and annotate
mask = df_damp['Steering_Velocity_deg_s'] > 0
slope_d, _ = np.polyfit(df_damp.loc[mask, 'Steering_Velocity_deg_s'], df_damp.loc[mask, 'FFB_Force'], 1)
x_trend = np.linspace(0, 200, 50)
ax.plot(x_trend, np.polyval([slope_d, 0], x_trend)/1000, 'r--', alpha=0.7, label=f'B = {slope_d:.1f}')
ax.legend()
ax.annotate(f"Damping Coefficient B = {slope_d:.1f}\n(Expected: ~500)", xy=(100, 80), fontsize=9)

plt.tight_layout()
plt.savefig(output_dir / "damping.png", dpi=150)
plt.close()
print("Saved: damping.png")

# 3. Friction Test
# X: Time (s), Y: FFB Force
# Expected: Peak at breakaway, then constant
df_fric = pd.read_csv(data_dir / "friction.csv")
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(df_fric['Time_s'], df_fric['FFB_Force']/1000, 'm.-', linewidth=1.5, markersize=6)
ax.axhline(y=2.0, color='r', linewidth=1, linestyle='--', alpha=0.7, label='Friction Level (~2k)')
ax.set_xlabel("Time (s)")
ax.set_ylabel("FFB Force (kN)")
ax.set_title("Friction Test: FFB vs Time (Breakaway)")
ax.grid(True, alpha=0.3)

peak_idx = df_fric['FFB_Force'].idxmax()
peak_val = df_fric.loc[peak_idx, 'FFB_Force']
peak_time = df_fric.loc[peak_idx, 'Time_s']
ax.annotate(f"Breakaway Peak\n{peak_val:.0f} at {peak_time:.1f}s", xy=(peak_time, peak_val/1000),
            xytext=(peak_time+0.5, peak_val/1000+2), fontsize=9,
            arrowprops=dict(arrowstyle='->', color='red'))

avg_fric = df_fric.loc[3:, 'FFB_Force'].mean()
ax.annotate(f"Friction T_fric = {avg_fric:.0f}\n(Expected: ~2000)", xy=(2, 3), fontsize=9)

ax.legend()
plt.tight_layout()
plt.savefig(output_dir / "friction.png", dpi=150)
plt.close()
print("Saved: friction.png")

# 4. Load Cell Test - Weight vs Load Cell (Left and Right)
# X: Weight (g), Y: Load Cell L (Left and Right)
# Expected: |L| proportional to weight, L positive when pulling left (negative R)
df_lc = pd.read_csv(data_dir / "loadcell.csv")
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(df_lc['Weight_g'], df_lc['Left']/1000, 'b.-', linewidth=1.5, markersize=8, label='Left (L)')
ax.plot(df_lc['Weight_g'], df_lc['Right']/1000, 'r.-', linewidth=1.5, markersize=8, label='Right (R)')
ax.axhline(y=0, color='k', linewidth=0.5)
ax.set_xlabel("Weight (g)")
ax.set_ylabel("Load Cell (L) (x1000)")
ax.set_title("Load Cell Test: L vs Weight (Left/Right)")
ax.grid(True, alpha=0.3)

# Fit and annotate
slope_left, _ = np.polyfit(df_lc['Weight_g'], df_lc['Left'], 1)
slope_right, _ = np.polyfit(df_lc['Weight_g'], df_lc['Right'], 1)
ax.annotate(f"Left Scale Factor = {slope_left:.1f}\nRight Scale Factor = {abs(slope_right):.1f}", xy=(300, -15), fontsize=9)
ax.legend()

plt.tight_layout()
plt.savefig(output_dir / "loadcell.png", dpi=150)
plt.close()
print("Saved: loadcell.png")

# 5. Drift Detection Test
# X: accY (m/s^2), Y: FFB Force (showing 80% drop when threshold exceeded)
# Threshold = 3.0 * (1 + |v|)
df_drift = pd.read_csv(data_dir / "drift_detection.csv")
fig, ax = plt.subplots(figsize=(8, 6))

# Color by velocity
scatter = ax.scatter(df_drift['accY_ms2'], df_drift['FFB_Force']/1000,
                     c=df_drift['Velocity'], cmap='viridis', s=50, edgecolors='k', linewidth=0.5)
plt.colorbar(scatter, label='Velocity (m/s)')

ax.axhline(y=5, color='gray', linewidth=1, linestyle='--', alpha=0.7)
ax.set_xlabel("Lateral Acceleration accY (m/s²)")
ax.set_ylabel("FFB Force (kN)")
ax.set_title("Drift Detection Test: FFB vs accY\n(FFB drops ~80% when |accY| > threshold)")
ax.grid(True, alpha=0.3)

# Mark threshold and drop
threshold = 3.5
ax.axvline(x=threshold, color='r', linewidth=2, linestyle='--', label=f'Threshold ≈ {threshold}')
ax.axvline(x=-threshold, color='r', linewidth=2, linestyle='--')

normal_ffb = df_drift.loc[df_drift['accY_ms2'].abs() < threshold, 'FFB_Force'].mean()
drift_ffb = df_drift.loc[df_drift['accY_ms2'].abs() > threshold, 'FFB_Force'].mean()
ax.annotate(f"Normal FFB: {normal_ffb:.0f}\nDrift FFB: {drift_ffb:.0f}\nDrop: {(1-drift_ffb/normal_ffb)*100:.0f}%",
            xy=(5, 3), fontsize=9)

ax.legend()
plt.tight_layout()
plt.savefig(output_dir / "drift_detection.png", dpi=150)
plt.close()
print("Saved: drift_detection.png")

# 6. Surface Jolt Test
# X: |accZ| (m/s^2), Y: Surface Jolt Force
# Expected: Jolt proportional to |accZ|, G_z ~ 500
df_jolt = pd.read_csv(data_dir / "surface_jolt.csv")
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(df_jolt['accZ_abs_ms2'], df_jolt['Surface_Jolt_Force']/1000, 'orange', linewidth=2, marker='.')
ax.set_xlabel("|accZ| (m/s²)")
ax.set_ylabel("Surface Jolt Force (kN)")
ax.set_title("Surface Jolt Test: Jolt vs |accZ|")
ax.grid(True, alpha=0.3)

# Fit and annotate
slope_j, _ = np.polyfit(df_jolt['accZ_abs_ms2'], df_jolt['Surface_Jolt_Force'], 1)
x_trend = np.linspace(0, 8, 50)
ax.plot(x_trend, np.polyval([slope_j, 0], x_trend)/1000, 'r--', alpha=0.7, label=f'G_z = {slope_j:.1f}')
ax.legend()
ax.annotate(f"Gain G_z = {slope_j:.1f}\n(Expected: ~500)", xy=(5, 3), fontsize=9)

plt.tight_layout()
plt.savefig(output_dir / "surface_jolt.png", dpi=150)
plt.close()
print("Saved: surface_jolt.png")

print("\nAll plots generated successfully!")
print(f"Output directory: {output_dir}")