# -*- coding: utf-8 -*-
"""
Created on Thu May 30 20:02:17 2024

@author: k5kei
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_schedule(result, J, R, T, C):
    schedule = result.X.reshape(len(J), T)
    fig, ax = plt.subplots(figsize=(15, 5))
    
    for i in range(len(J)):
        task_schedule = schedule[i, :]
        for t in range(T):
            if task_schedule[t] != 0:
                robot = task_schedule[t]
                ax.broken_barh([(t, 1)], (i * 10, 9), facecolors=(f"C{robot}"))
                ax.text(t + 0.5, i * 10 + 5, f"R{robot}", color="black",
                        ha='center', va='center', fontsize=8)

    ax.set_ylim(0, len(J) * 10)
    ax.set_xlim(0, T)
    ax.set_xlabel('Time')
    ax.set_yticks([i * 10 + 5 for i in range(len(J))])
    ax.set_yticklabels([f"Task {i+1}" for i in range(len(J))])
    ax.grid(True)

    plt.show()
