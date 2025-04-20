
import fastf1
from fastf1 import plotting
import pandas as pd
import matplotlib.pyplot as plt

# Enable caching
fastf1.Cache.enable_cache('cache')

# === Ask user for input ===
year = 2025
race_name = input("Enter Grand Prix name (e.g. 'Saudi Arabia', 'Australia'): ")
session_type = input("Enter session type (FP1, FP2, FP3, Q, R, S): ").upper()

# Load session
try:
    session = fastf1.get_session(year, race_name, session_type)
    session.load()
except Exception as e:
    print(f"Error loading session: {e}")
    exit()

# Collect top speeds with full driver names
top_speeds = {}

for drv_code in session.drivers:
    driver_laps = session.laps.pick_drivers(drv_code)
    if driver_laps.empty:
        continue

    try:
        fastest_lap = driver_laps.loc[driver_laps['LapTime'].idxmin()]
        telemetry = fastest_lap.get_car_data().add_distance()
        max_speed = telemetry['Speed'].max()
        full_name = session.get_driver(drv_code)['FullName']
        top_speeds[full_name] = max_speed
    except:
        continue

# Convert to DataFrame
speed_df = pd.DataFrame.from_dict(top_speeds, orient='index', columns=['Top Speed (km/h)'])
speed_df.sort_values(by='Top Speed (km/h)', ascending=False, inplace=True)

# Plot
plt.figure(figsize=(12, 6))
bars = plt.bar(speed_df.index, speed_df['Top Speed (km/h)'], color='skyblue')

# Add value labels on top
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 1, f"{height:.1f}", ha='center', va='bottom', fontsize=9)

plt.title(f'Speed Trap Leaderboard - {year} {race_name} GP {session_type}')
plt.xlabel('Driver')
plt.ylabel('Top Speed (km/h)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.show()
