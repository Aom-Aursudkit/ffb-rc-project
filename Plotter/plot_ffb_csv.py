import matplotlib.pyplot as plt
import numpy as np

# ===== EDIT THIS =====
CSV_FILE = "data\\ffb_tests\\sat.csv"
# ====================

def read_log_csv(filename):
    steers, velocities, loads, ffb_forces = [], [], [], []
    accX, accY, accZ = [], [], []
    gyroX, gyroY, gyroZ = [], [], []
    times = []

    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            parts = [p.strip() for p in line.strip().split('|')]
            if len(parts) < 4:
                continue

            try:
                steers.append(float(parts[0].split(':')[1]))
                ffb_forces.append(float(parts[1].split(':')[1]))
                velocities.append(float(parts[2].split(':')[1].split('g')[0]))
                loads.append(float(parts[3].split(':')[1].split('g')[0]))

                acc_x, acc_y, acc_z = 0.0, 0.0, 0.0
                gyro_x, gyro_y, gyro_z = 0.0, 0.0, 0.0

                for p in parts[4:]:
                    if 'AccXYZ' in p:
                        nums = p.split(':')[1].split(',')
                        acc_x, acc_y, acc_z = float(nums[0]), float(nums[1]), float(nums[2])
                    elif 'GyroXYZ' in p:
                        nums = p.split(':')[1].split(',')
                        gyro_x, gyro_y, gyro_z = float(nums[0]), float(nums[1]), float(nums[2])

                accX.append(acc_x)
                accY.append(acc_y)
                accZ.append(acc_z)
                gyroX.append(gyro_x)
                gyroY.append(gyro_y)
                gyroZ.append(gyro_z)
                times.append(i * 10)

            except (ValueError, IndexError):
                continue

    return np.array(times), np.array(steers), np.array(velocities), np.array(loads), np.array(ffb_forces), np.array(accX), np.array(accY), np.array(accZ), np.array(gyroX), np.array(gyroY), np.array(gyroZ)

def plot_all(times, steers, velocities, loads, ffb_forces, accX, accY, accZ, gyroX, gyroY, gyroZ):
    if times[0] != 0:
        times = times - times[0]
    times = times / 1000.0

    num_rows = 4
    fig, axes = plt.subplots(num_rows, 1, figsize=(14, 3*num_rows))
    fig.suptitle(f"FFB Test Data: {CSV_FILE}", fontsize=14)

    axes[0].plot(times, steers, 'b-', linewidth=1.5)
    axes[0].set_ylabel('Steer')
    axes[0].grid(True, linestyle='--', alpha=0.5)

    axes[1].plot(times, velocities, 'g-', linewidth=1.5)
    axes[1].set_ylabel('Vel (m/s)')
    axes[1].grid(True, linestyle='--', alpha=0.5)

    axes[2].plot(times, ffb_forces, 'r-', linewidth=1.5)
    axes[2].set_ylabel('FFB')
    axes[2].grid(True, linestyle='--', alpha=0.5)

    axes[3].plot(times, loads, 'm-', linewidth=1.5, label='Load')
    axes[3].set_ylabel('Load (g)')
    axes[3].set_xlabel('Time (s)')
    axes[3].grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig(CSV_FILE.replace('.csv', '.png'), dpi=150)
    plt.show()

    fig2, axes2 = plt.subplots(2, 1, figsize=(14, 8))
    fig2.suptitle("IMU Data")

    axes2[0].plot(times, accX, 'r-', linewidth=1, label='AccX', alpha=0.8)
    axes2[0].plot(times, accY, 'g-', linewidth=1, label='AccY', alpha=0.8)
    axes2[0].plot(times, accZ, 'b-', linewidth=1, label='AccZ', alpha=0.8)
    axes2[0].set_ylabel('Acc')
    axes2[0].legend()
    axes2[0].grid(True, linestyle='--', alpha=0.5)

    axes2[1].plot(times, gyroX, 'r-', linewidth=1, label='GyroX', alpha=0.8)
    axes2[1].plot(times, gyroY, 'g-', linewidth=1, label='GyroY', alpha=0.8)
    axes2[1].plot(times, gyroZ, 'b-', linewidth=1, label='GyroZ', alpha=0.8)
    axes2[1].set_ylabel('Gyro')
    axes2[1].set_xlabel('Time (s)')
    axes2[1].legend()
    axes2[1].grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig(CSV_FILE.replace('.csv', '_imu.png'), dpi=150)
    plt.show()

    print(f"\n=== Summary ===")
    print(f"File: {CSV_FILE}")
    print(f"Samples: {len(times)}")
    print(f"Duration: {times[-1]:.1f}s")
    print(f"Steer: {np.min(steers):.2f} ~ {np.max(steers):.2f}")
    print(f"Vel: {np.min(velocities):.3f} ~ {np.max(velocities):.3f}")
    print(f"FFB: {np.min(ffb_forces):.0f} ~ {np.max(ffb_forces):.0f}")
    print(f"Load: {np.min(loads):.1f} ~ {np.max(loads):.1f}")
    print(f"AccX: {np.min(accX):.2f} ~ {np.max(accX):.2f}")
    print(f"AccY: {np.min(accY):.2f} ~ {np.max(accY):.2f}")
    print(f"AccZ: {np.min(accZ):.2f} ~ {np.max(accZ):.2f}")
    print(f"GyroX: {np.min(gyroX):.2f} ~ {np.max(gyroX):.2f}")
    print(f"GyroY: {np.min(gyroY):.2f} ~ {np.max(gyroY):.2f}")
    print(f"GyroZ: {np.min(gyroZ):.2f} ~ {np.max(gyroZ):.2f}")

times, steers, velocities, loads, ffb_forces, accX, accY, accZ, gyroX, gyroY, gyroZ = read_log_csv(CSV_FILE)
if len(times) == 0:
    print("No data found!")
else:
    plot_all(times, steers, velocities, loads, ffb_forces, accX, accY, accZ, gyroX, gyroY, gyroZ)