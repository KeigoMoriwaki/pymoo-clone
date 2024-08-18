# -*- coding: utf-8 -*-
"""
Created on Thu May 30 20:02:17 2024

@author: k5kei
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_schedule(result, J, R, T, C):
    schedule = result.reshape((len(J), T))
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.get_cmap('tab10', len(J))

    for j in range(len(J)):
        for t in range(T):
            robot = int(np.ceil(schedule[j, t]))
            failure_probability = 1 - C * t
            if np.random.rand() > failure_probability:
                ax.text(t + 0.5, j + 0.5, f"R{robot} (F)", ha='center', va='center', color='red') # 故障
            else:
                ax.broken_barh([(t, 1)], (j, 1), facecolors=(colors(j)))
                ax.text(t + 0.5, j + 0.5, f"R{robot}", ha='center', va='center', color='black')


    ax.set_xlabel('Time')
    ax.set_ylabel('Task')
    ax.set_yticks(np.arange(len(J)) + 0.5)
    ax.set_yticklabels([f'T{task}' for task in J])
    ax.set_xticks(np.arange(T + 1))
    plt.show()