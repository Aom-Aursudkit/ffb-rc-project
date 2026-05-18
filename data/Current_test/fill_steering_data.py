import pandas as pd
import numpy as np

np.random.seed(42)

data_dir = r"C:\College 3.2\Open Topic\ffb-rc-project\data"

# Load both files
df_air = pd.read_csv(f'{data_dir}\\steering_air.csv', header=None, names=['Time','Steering','Current'])
df_lam = pd.read_csv(f'{data_dir}\\steering_laminate.csv', header=None, names=['Time','Steering','Current'])

def fill_missing_currents(df, name):
    df = df.copy()

    # Get stats from neighbors
    mean_1, std_1 = df[df['Steering']==1]['Current'].mean(), df[df['Steering']==1]['Current'].std()
    mean_179, std_179 = df[df['Steering']==179]['Current'].mean(), df[df['Steering']==179]['Current'].std()

    print(f"{name}:")
    print(f"  Angle 1: mean={mean_1:.4f}, std={std_1:.4f}")
    print(f"  Angle 179: mean={mean_179:.4f}, std={std_179:.4f}")

    # Count how many samples we need to add for 0 and 180
    count_1 = len(df[df['Steering']==1])
    count_179 = len(df[df['Steering']==179])

    print(f"  Will add {count_1} samples for angle 0, {count_179} samples for angle 180")

    # Get max time for each
    max_time_0 = df[df['Steering']==0]['Time'].values[0]
    max_time_180 = df[df['Steering']==180]['Time'].values[0]

    # Generate new rows for angle 0 (time values before max_time_0)
    new_rows_0 = []
    for i in range(count_1):
        time_val = max_time_0 - (count_1 - i) * 10  # decreasing time
        current_val = np.clip(np.random.normal(mean_1, std_1), 1.5, 2.5)
        new_rows_0.append([time_val, 0, current_val])

    # Generate new rows for angle 180 (time values after max_time_180)
    new_rows_180 = []
    for i in range(count_179):
        time_val = max_time_180 + (i + 1) * 10  # increasing time
        current_val = np.clip(np.random.normal(mean_179, std_179), 1.5, 2.5)
        new_rows_180.append([time_val, 180, current_val])

    # Combine and sort by time
    new_df = pd.DataFrame(new_rows_0 + new_rows_180, columns=['Time','Steering','Current'])
    df = pd.concat([df, new_df], ignore_index=True)
    df = df.sort_values('Time').reset_index(drop=True)

    return df

# Process both
df_air_filled = fill_missing_currents(df_air, "Air")
df_lam_filled = fill_missing_currents(df_lam, "Laminate")

# Save
df_air_filled.to_csv(f'{data_dir}\\steering_air_filled.csv', index=False, header=False)
df_lam_filled.to_csv(f'{data_dir}\\steering_laminate_filled.csv', index=False, header=False)

print("\nSaved: steering_air_filled.csv")
print("Saved: steering_laminate_filled.csv")

# Verify
print("\nVerification:")
print(f"Air filled shape: {df_air_filled.shape}")
print(f"Laminate filled shape: {df_lam_filled.shape}")
print(f"Air steering 0 samples: {len(df_air_filled[df_air_filled['Steering']==0])}")
print(f"Air steering 180 samples: {len(df_air_filled[df_air_filled['Steering']==180])}")
print(f"Laminate steering 0 samples: {len(df_lam_filled[df_lam_filled['Steering']==0])}")
print(f"Laminate steering 180 samples: {len(df_lam_filled[df_lam_filled['Steering']==180])}")