# -*- coding: utf-8 -*-
"""
Created on Thu May 30 20:02:17 2024

@author: k5kei
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_timeline(J, T, result, p, locations):
    x = result.X.reshape(len(J), T)
    fig, ax = plt.subplots()

    for j in range(len(J)):
        task_start = np.argmax(x[j])
        task_end = task_start + p[j+1]
        robot = np.max(x[j])
        ax.barh(y=j, width=task_end-task_start, left=task_start, color='orange', edgecolor='black')
        ax.text((task_start + task_end) / 2, j, f'R{int(robot)}', ha='center', va='center')

    ax.set_yticks(range(len(J)))
    ax.set_yticklabels([f'Task {j+1} ({locations[j+1]})' for j in range(len(J))])
    ax.set_xlabel('Time')
    ax.set_ylabel('Tasks')
    plt.show()
