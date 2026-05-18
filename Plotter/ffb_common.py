import numpy as np
import re

def read_log_csv(filename):
    """Read CSV with format: Steer: x.xx | FFB: xxxx | Vel: x.x | Load: x.xg | AccXYZ: x.xx,x.xx,x.xx | GyroXYZ: x.xx,x.xx,x.xx"""
    times, steers, velocities, loads = [], [], [], []
    ffb_forces = []
    accX, accY, accZ = [], [], []
    gyroX, gyroY, gyroZ = [], [], []

    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            parts = [p.strip() for p in line.strip().split('|')]
            if len(parts) < 4:
                continue

            try:
                steer = float(parts[0].split(':')[1])
                ffb = float(parts[1].split(':')[1])
                vel = float(parts[2].split(':')[1].split('g')[0])
                load = float(parts[3].split(':')[1].split('g')[0])

                steers.append(steer)
                ffb_forces.append(ffb)
                velocities.append(vel)
                loads.append(load)
                times.append(i * 10)

                acc_x, acc_y, acc_z = 0.0, 0.0, 0.0
                gyro_x, gyro_y, gyro_z = 0.0, 0.0, 0.0

                for p in parts[4:]:
                    p = p.strip()
                    if p.startswith('AccXYZ'):
                        nums = p.split(':')[1].split(',')
                        if len(nums) == 3:
                            acc_x, acc_y, acc_z = float(nums[0]), float(nums[1]), float(nums[2])
                    elif p.startswith('GyroXYZ'):
                        nums = p.split(':')[1].split(',')
                        if len(nums) == 3:
                            gyro_x, gyro_y, gyro_z = float(nums[0]), float(nums[1]), float(nums[2])

                accX.append(acc_x)
                accY.append(acc_y)
                accZ.append(acc_z)
                gyroX.append(gyro_x)
                gyroY.append(gyro_y)
                gyroZ.append(gyro_z)

            except (ValueError, IndexError):
                continue

    return (np.array(times), np.array(steers), np.array(velocities), np.array(loads),
            np.array(ffb_forces), np.array(accX), np.array(accY), np.array(accZ),
            np.array(gyroX), np.array(gyroY), np.array(gyroZ))