import matplotlib.pyplot as plt
import numpy as np

def read_csv(filename):
    times, angles, currents = [], [], []
    with open(filename, 'r') as f:
        for line in f:
            if not line.strip(): continue
            parts = line.strip().split(',')
            if len(parts) != 3: continue
            try:
                times.append(float(parts[0]) / 1000.0)
                angles.append(float(parts[1]))
                currents.append(float(parts[2]))
            except ValueError:
                continue
    return np.array(times), np.array(angles), np.array(currents)

# Read both files
idle_times, idle_angles, idle_currents = read_csv('data/Current_test/idle2.csv')
sweep_times, sweep_angles, sweep_currents = read_csv('data/Current_test/steering_laminate2.csv')

# Normalize time
idle_times = idle_times - idle_times[0]
sweep_times = sweep_times - sweep_times[0]

fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# ===== TOP PLOT: Time series comparison =====
ax1 = axes[0]
ax1_twin = ax1.twinx()

ax1.plot(sweep_times, sweep_angles, 'b-', linewidth=2, label='Steering Angle')
ax1.set_ylabel('Steering Angle (°)', color='blue', fontsize=11)
ax1.set_ylim(-10, 190)
ax1.set_yticks(range(0, 181, 30))

ax1_twin.plot(idle_times, idle_currents, 'g-', alpha=0.7, linewidth=1.5, label='Idle Current')
ax1_twin.plot(sweep_times, sweep_currents, 'r-', alpha=0.7, linewidth=1.5, label='Sweep Current')
ax1_twin.set_ylabel('Current (A)', color='red', fontsize=11)
ax1_twin.set_ylim(-0.5, 4.0)

ax1.set_xlabel('Time (s)')
ax1.set_title('Current Sensor Problem: Idle vs Sweep Comparison', fontsize=14)
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend(loc='upper left')
ax1_twin.legend(loc='upper right')

# ===== BOTTOM PLOT: Current distribution =====
ax2 = axes[1]

# Idle current histogram
ax2.hist(idle_currents, bins=50, alpha=0.6, label=f'Idle (μ={np.mean(idle_currents):.3f}A, σ={np.std(idle_currents):.3f}A)', color='green', density=True)

# Sweep current when angle is CHANGING (velocity > threshold)
angle_diff = np.diff(sweep_angles)
time_diff = np.diff(sweep_times)
velocity = np.abs(angle_diff / (time_diff + 1e-6))
is_moving = velocity > 5  # deg/ms threshold
moving_currents = sweep_currents[1:][is_moving]
stationary_currents = sweep_currents[1:][~is_moving]

ax2.hist(moving_currents, bins=50, alpha=0.6, label=f'Moving (μ={np.mean(moving_currents):.3f}A, σ={np.std(moving_currents):.3f}A)', color='red', density=True)
ax2.hist(stationary_currents, bins=50, alpha=0.6, label=f'Stop(from moving) (μ={np.mean(stationary_currents):.3f}A, σ={np.std(stationary_currents):.3f}A)', color='orange', density=True)

ax2.set_xlabel('Current (A)')
ax2.set_ylabel('Density')
ax2.set_title('Current Distribution: Moving vs Stationary', fontsize=14)
ax2.legend()
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.set_xlim(-0.5, 4.0)

plt.tight_layout()
plt.savefig('Plotter/current_comparison.png', dpi=150)
plt.show()

# ===== STATS =====
print("\n=== IDLE ===")
print(f"  Mean: {np.mean(idle_currents):.4f} A")
print(f"  Std:  {np.std(idle_currents):.4f} A")
print(f"  Min:  {np.min(idle_currents):.4f} A")
print(f"  Max:  {np.max(idle_currents):.4f} A")
print(f"  Range: {np.max(idle_currents) - np.min(idle_currents):.4f} A")

print("\n=== SWEEP (Moving) ===")
print(f"  Mean: {np.mean(moving_currents):.4f} A")
print(f"  Std:  {np.std(moving_currents):.4f} A")
print(f"  Min:  {np.min(moving_currents):.4f} A")
print(f"  Max:  {np.max(moving_currents):.4f} A")
print(f"  Range: {np.max(moving_currents) - np.min(moving_currents):.4f} A")

print("\n=== SWEEP (Stationary) ===")
print(f"  Mean: {np.mean(stationary_currents):.4f} A")
print(f"  Std:  {np.std(stationary_currents):.4f} A")
print(f"  Min:  {np.min(stationary_currents):.4f} A")
print(f"  Max:  {np.max(stationary_currents):.4f} A")

print("\n=== CONCLUSION ===")
overlap = max(np.mean(idle_currents) - 2*np.std(idle_currents), np.mean(moving_currents) - 2*np.std(moving_currents))
print(f"  Overlap region: {overlap:.3f} to {max(np.max(idle_currents), np.max(moving_currents)):.3f} A")
print(f"  Current cannot reliably distinguish movement from idle due to noise/spikes")