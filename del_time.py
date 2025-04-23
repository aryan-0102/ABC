import pandas as pd
import matplotlib.pyplot as plt


# Load the CSV files
file_dijkstra = 'optimized_schedule_dijkstra_v4.csv'
file_abc = 'optimized_schedule_abc_v4.csv'

# Read the CSV files
df_dijkstra = pd.read_csv(file_dijkstra)
df_abc = pd.read_csv(file_abc)

# Extract relevant columns (assuming the columns are named 'TotalMinutes' and 'TravelMinutes')
df_dijkstra = df_dijkstra[['TotalMinutes', 'TravelMinutes']]
df_abc = df_abc[['TotalMinutes', 'TravelMinutes']]


# Calculate and print the average, maximum, and difference for both TotalMinutes and TravelMinutes
def print_time_stats(df, source_name):
    total_minutes_avg = df['TotalMinutes'].mean()
    total_minutes_max = df['TotalMinutes'].max()
    travel_minutes_avg = df['TravelMinutes'].mean()
    travel_minutes_max = df['TravelMinutes'].max()
    print(source_name)
    print('total', df['TotalMinutes'].sum())
    print('travel', df['TravelMinutes'].sum())
    total_minutes_diff = total_minutes_max - total_minutes_avg
    travel_minutes_diff = travel_minutes_max - travel_minutes_avg

    return [source_name,df['TotalMinutes'].sum(),df['TravelMinutes'].sum(),df['TotalMinutes'].sum() - df['TravelMinutes'].sum()]



dat = pd.DataFrame(columns = ["Name","Total Time","Travel Time(min)","Wait Times"])
# Print stats for both datasets
dat.loc[len(dat)] = print_time_stats(df_dijkstra, "Dijkstra")
dat.loc[len(dat)] = print_time_stats(df_abc, "ABC")
df = pd.DataFrame(dat)
# Line plot for TravelMinutes comparison
plt.figure(figsize=(10, 6))

plt.plot(df_dijkstra['TravelMinutes'], label='Dijkstra TravelMinutes', color='blue', linestyle='-')
plt.plot(df_abc['TravelMinutes'], label='ABC TravelMinutes', color='green', linestyle='-')

plt.title('TravelMinutes Comparison: Dijkstra vs. ABC')
plt.xlabel('Index')
plt.ylabel('TravelMinutes')
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig('delivery.png', dpi=300)

print(dat)

fig, ax = plt.subplots(figsize=(8, 3))  # Adjust figure size as needed

# Hide axes
ax.axis('off')

# Create the table
table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')

# Adjust table properties (optional)
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)  # Adjust cell size

# Save the figure as a JPG image
plt.savefig('deliverystats.jpg', bbox_inches='tight')

print("Table saved as table.jpg")


