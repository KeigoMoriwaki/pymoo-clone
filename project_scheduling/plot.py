# -*- coding: utf-8 -*-
"""
Created on Thu May 30 20:02:17 2024

@author: k5kei
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_timeline(J, T, result, p, locations, robots, travel_time):
    x = result.X.reshape((len(J), T))
    fig, ax = plt.subplots()
    
    # ロボットごとのタスクをプロット
    for robot_id in range(1, len(robots) + 1):
        current_location = 'A'
        for t in range(T):
            for job in range(len(J)):
                if x[job, t] == robot_id:
                    finish = t + int(np.ceil(p[job + 1] / np.sum(x[job] == robot_id)))  # 作業量を考慮して終了時間を計算
                    location = locations[job + 1]
                    travel_duration = 0
                    if current_location != location:
                        travel_duration = travel_time[current_location][location]
                        t += travel_duration  # 移動時間を考慮して開始時間を調整
                    ax.broken_barh([(t, finish - t)], (robot_id - 0.4, 0.8), facecolors='orange')
                    ax.text(t + (finish - t) / 2, robot_id, f'Job {job+1} ({location})', ha='center', va='center', color='black')
                    current_location = location

    ax.set_ylim(0, len(robots) + 1)
    ax.set_xlim(0, T)
    ax.set_xlabel('Time')
    ax.set_ylabel('Robot')
    ax.set_yticks(range(1, len(robots) + 1))
    ax.set_yticklabels([f'Robot {i}' for i in range(1, len(robots) + 1)])
    ax.grid(True)
    plt.show()
