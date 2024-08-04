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

    robot_schedule = [[] for _ in range(len(R))]
    for t in range(T):
        for i in range(len(J)):
            robot = schedule[i, t] - 1
            if robot >= 0:
                robot_schedule[robot].append((t, i + 1))

    for robot, tasks in enumerate(robot_schedule):
        for (t, task) in tasks:
            ax.broken_barh([(t, 1)], (robot * 10, 9), facecolors=(f"C{task}"))
            ax.text(t + 0.5, robot * 10 + 5, f"T{task}", color="black",
                    ha='center', va='center', fontsize=8)

    ax.set_ylim(0, len(R) * 10)
    ax.set_xlim(0, T)
    ax.set_xlabel('Time')
    ax.set_yticks([i * 10 + 5 for i in range(len(R))])
    ax.set_yticklabels([f"Robot {i+1}" for i in range(len(R))])
    ax.grid(True)

    plt.show()
