import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

# Set the directory containing your CSV files
directory = 'C:\\Users\\domi1\\Programowanie\\physics-engine\\Simulations\\training_1\\Simulations\\sims'  # Change this to your directory path
csv_files = glob.glob(os.path.join(directory, '*.csv'))

# Store all trajectory data to calculate global axis limits
all_x, all_y, all_z = [], [], []

# First pass: collect all data to compute global min/max
dataframes = []
for file in csv_files:
    df = pd.read_csv(file, skiprows=[0])
    dataframes.append((file, df))
    all_x.extend(df['pos_x'])
    all_y.extend(df['pos_y'])
    all_z.extend(df['pos_z'])

# Determine global axis limits
x_min, x_max = min(all_x), max(all_x)
y_min, y_max = min(all_y), max(all_y)
z_min, z_max = min(all_z), max(all_z)

# Plot each file's trajectory with consistent axis limits
for file, df in dataframes:
    filename = os.path.splitext(os.path.basename(file))[0]
    x = df['pos_x']
    y = df['pos_y']
    z = df['pos_z']

    # XZ Plane
    plt.figure(figsize=(8, 6))
    plt.plot(x, z, color='blue')
    plt.title(f'')
    plt.subplots_adjust(left=0.2)
    plt.xlabel('Przesunięcie w osi X [m]', fontsize=20)
    plt.ylabel('Wysokość [m]', fontsize=20)
    plt.grid(True)
    plt.xlim(x_min, x_max)
    plt.ylim(z_min, z_max)
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.axis('equal')
    plt.tight_layout()
    # plt.show()
    plt.savefig(os.path.join(directory, f'{filename}x.png'))
    plt.close()

    # YZ Plane
    plt.figure(figsize=(8, 6))
    plt.plot(y, z, color='green')
    plt.title(f'')
    plt.xlabel('Przesunięcie w osi Y [m]', fontsize=20)
    plt.ylabel('Wysokość [m]', fontsize=20)
    plt.grid(True)
    plt.xlim(y_min, y_max)
    plt.ylim(z_min, z_max)
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(os.path.join(directory, f'{filename}y.png'))
    plt.close()
