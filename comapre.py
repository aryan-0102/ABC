#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
df = pd.read_csv('abc_distances1000.csv')

df2 = pd.read_csv('dijkstra.csv')
df1 = pd.read_csv('astar.csv')


abc = df['Distance(meters)']
dikstra = df2['Distance(meters)']

star = df1['ShortestDistance']

plt.plot(abc, linestyle='-',label='ABC')
plt.plot(dikstra, linestyle='-',label='DIJKSTRA')
plt.plot(star, linestyle='-',label='STAR')
plt.legend()
plt.grid(True)
plt.rcParams['figure.dpi'] = 300

plt.savefig('time_compare.png', dpi=300)
column = ['Name','Total_Distance','Mean','Median']
data = pd.DataFrame(columns=column)


data.loc[len(data)] = ["Dijkstra", dikstra.sum(), dikstra.mean(), dikstra.median()]
data.loc[len(data)] = ['ABC',abc.sum(), abc.mean(), abc.median()]
data.loc[len(data)] = ['A-Star',star.sum(),star.mean(),star.median()]

def create_stats_table_image(df: pd.DataFrame, output_filename: str = "deliverystats.png"):
    if not isinstance(df, pd.DataFrame):
        print("Error: Input must be a pandas DataFrame.")
        return

    df_display = df.copy()
    numeric_cols = df_display.select_dtypes(include=np.number).columns
    df_display[numeric_cols] = df_display[numeric_cols].round(2)

    num_rows, num_cols = df_display.shape
    fig_height = max(1.5, num_rows * 0.5)
    fig_width = max(6, num_cols * 1.5)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    ax.axis('tight')
    ax.axis('off')

    table = ax.table(cellText=df_display.values,
                     colLabels=df_display.columns,
                     cellLoc='center',
                     loc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.1, 1.1)

    try:
        plt.savefig(output_filename, bbox_inches='tight', dpi=300)
        print(f"Successfully generated table image: '{output_filename}'")
    except Exception as e:
        print(f"Error saving table image '{output_filename}': {e}")
    finally:
        plt.close(fig)

stats_df = pd.DataFrame(data)

create_stats_table_image(stats_df,"DistanceTable.png")

