# -*- coding: utf-8 -*-
"""
Created on Thu May 30 20:02:17 2024

@author: k5kei
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_schedule(result, J, R, T):
    schedule = result.X.reshape((len(J), T))

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.get_cmap('tab10', len(J))

    for j in range(len(J)):
        for t in range(T):
            if schedule[j, t] != 0:
                robot = int(np.ceil(schedule[j, t]))  # 小数の場合、切り上げして整数にする
                ax.broken_barh([(t, 1)], (robot - 1, 1), facecolors=(colors(j)))
                ax.text(t + 0.5, robot - 0.5, f"J{J[j]}", ha='center', va='center', color='black')

    ax.set_xlabel('Time')
    ax.set_ylabel('Robot')
    ax.set_yticks(np.arange(len(R)) + 0.5)
    ax.set_yticklabels([f'R{r}' for r in R])
    ax.set_xticks(np.arange(T + 1))
    plt.show()