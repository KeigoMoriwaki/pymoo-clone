# -*- coding: utf-8 -*-
"""
Created on Thu May 30 20:02:17 2024

@author: k5kei
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_schedule(result, problem_data):
    J, P, R, T, p, RUB, backup_robots = problem_data

    # 最適化結果からスケジュールを取得
    expected_shape = (len(J) * T,)
    if result.X.shape == expected_shape:
        best_schedule = result.X.reshape((len(J), T))
    else:
        raise ValueError(f"Unexpected result.X shape: {result.X.shape}, expected {expected_shape}")

    fig, ax = plt.subplots()
    colors = plt.cm.get_cmap('tab20', len(J))

    for r in range(len(R)):
        for t in range(T):
            for j in range(len(J)):
                if best_schedule[j, t] == r + 1:
                    ax.broken_barh([(t, 1)], (r * 10, 9), facecolors=colors(j))
                    ax.text(t + 0.5, r * 10 + 5, f'J{j+1}', ha='center', va='center', color='black')

    for r in backup_robots:
        for t in range(T):
            for j in range(len(J)):
                if best_schedule[j, t] == r:
                    ax.broken_barh([(t, 1)], ((r-1) * 10, 9), facecolors=colors(j))
                    ax.text(t + 0.5, (r-1) * 10 + 5, f'J{j+1}', ha='center', va='center', color='black')

    ax.set_xlabel('Time')
    ax.set_ylabel('Robots')
    y_ticks = []
    y_labels = []

    for r in range(len(R)):
        if r+1 in backup_robots:
            y_labels.append(f'BR{r+1}')
        else:
            y_labels.append(f'R{r+1}')
        y_ticks.append(r * 10 + 5)

    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels)
    plt.show()
