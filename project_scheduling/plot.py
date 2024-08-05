# -*- coding: utf-8 -*-
"""
Created on Thu May 30 20:02:17 2024

@author: k5kei
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_schedule(schedule, J, R, T):
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.get_cmap('tab10', len(J))

    for r in range(len(R)):
        for t in range(T):
            tasks_at_t = [j for j in range(len(J)) if schedule[j, t] == r + 1]
            for task in tasks_at_t:
                ax.broken_barh([(t, 1)], (r - 0.4, 0.8), facecolors=(colors(task)))
                ax.text(t + 0.5, r, f"T{J[task]}", ha='center', va='center', color='black')

    ax.set_xlabel('Time')
    ax.set_ylabel('Robot')
    ax.set_yticks(np.arange(len(R)))
    ax.set_yticklabels([f'R{r}' for r in R])
    ax.set_xticks(np.arange(T + 1))
    plt.show()
