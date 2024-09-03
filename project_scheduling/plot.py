# -*- coding: utf-8 -*-
"""
Created on Thu May 30 20:02:17 2024

@author: k5kei
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_schedule(result, J, R, T):
    #print(f"Debug in plot_schedule: T={T}"
    schedule = result.X.reshape((len(J), T))
    failed_tasks = result.algorithm.pop.get("failed_tasks")[0]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.get_cmap('tab10', len(J))
    
    for j in range(len(J)):
        for t in range(T):
            if schedule[j, t] > 0:
                robot = int(np.ceil(schedule[j, t]))
                face_color = colors(j)
                text_color = 'white' if failed_tasks[j, t] == 1 else 'black'  # タスクの仕事量が1未満の場合、故障と見なす
                ax.broken_barh([(t, 1)], (robot - 1, 1), facecolors=(face_color))
                ax.text(t + 0.5, robot - 0.5, f"J{J[j]}", ha='center', va='center', color=text_color)
    
    ax.set_xlabel('Time')
    ax.set_ylabel('Robot')
    ax.set_yticks(np.arange(len(R)) + 0.5)
    ax.set_yticklabels([f'R{r}' for r in R])
    ax.set_xticks(np.arange(T + 1))
    plt.show()
    
