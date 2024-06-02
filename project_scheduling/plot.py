# -*- coding: utf-8 -*-
"""
Created on Thu May 30 20:02:17 2024

@author: k5kei
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_timeline(J, T, result, p):
    x = result.X.reshape(len(J), T)
    fig, ax = plt.subplots(figsize=(12, 8))

    task_data = []

    for j in range(len(J)):
        for t in range(T):
            if x[j, t] > 0:
                robot = int(x[j, t])
                start = t
                finish = t + p[J[j]]
                task_data.append((start, finish, f'Task {J[j]}', f'R{robot}'))
                break

    # Convert task data to DataFrame for easier plotting
    df = pd.DataFrame(task_data, columns=['Start', 'Finish', 'Task', 'Robot'])

    for i, row in df.iterrows():
        ax.broken_barh([(row['Start'], row['Finish'] - row['Start'])], (i - 0.4, 0.8),
                       facecolors=f'tab:orange', edgecolors='black')
        ax.text((row['Start'] + row['Finish']) / 2, i, row['Robot'], va='center', ha='center', color='black', fontsize=12)

    ax.set_yticks(np.arange(len(df)))
    ax.set_yticklabels(df['Task'])
    ax.set_xticks(np.arange(T + 1))
    ax.set_xlabel('Time Period')
    ax.set_ylabel('Tasks')
    ax.grid(True)

    # Add timeline markers for better visualization
    for i, row in df.iterrows():
        ax.plot([row['Start'], row['Finish']], [i, i], color='tab:orange', marker='|')
        ax.text(row['Start'], i + 0.2, f'Start: {row["Start"]}', ha='center', fontsize=8, color='blue')
        ax.text(row['Finish'], i - 0.2, f'Finish: {row["Finish"]}', ha='center', fontsize=8, color='red')

    plt.title('Task Scheduling Timeline')
    plt.show()
