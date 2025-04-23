import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set the Seaborn style
sns.set_theme(style="whitegrid")

# Data from the table
iterations = [100, 200, 300, 400, 500, 1000]
avg_time = [57.34773599, 50.14779221, 61.32278639, 72.69106676, 83.96071975, 140.3157019]
total_distance = [431.6781648, 381.0439724, 368.3155603, 350.370104, 339.7023133, 333.2147089]

# Create figure and axis
fig, ax = plt.figure(figsize=(10, 6)), plt.gca()

# Plot using Seaborn
sns.lineplot(x=iterations, y=avg_time, marker='o', label='Average Time', color='blue')
sns.lineplot(x=iterations, y=total_distance, marker='o', label='Total Distance', color='green')

# Add labels and title
plt.xlabel('Number of Iterations')
plt.ylabel('Values')
plt.title('Average Time and Total Distance vs Number of Iterations')

# Set y-axis limits to make the graph more readable
plt.ylim(40, 450)

# Make the grid denser by setting more ticks
ax.xaxis.set_major_locator(plt.MultipleLocator(100))  # Major ticks every 100 units
ax.yaxis.set_major_locator(plt.MultipleLocator(50))   # Major ticks every 50 units
ax.xaxis.set_minor_locator(plt.MultipleLocator(50))   # Minor ticks every 50 units
ax.yaxis.set_minor_locator(plt.MultipleLocator(25))   # Minor ticks every 25 units
ax.grid(which='minor', alpha=0.3)  # Show minor grid lines with lower opacity
ax.grid(which='major', alpha=0.7)  # Show major grid lines with higher opacity

# Save the figure with 300 DPI
plt.savefig('iterations_analysis_dense_grid.png', dpi=300)

# Display the plot
plt.tight_layout()

