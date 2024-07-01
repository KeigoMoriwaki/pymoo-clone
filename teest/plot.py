# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 10:49:23 2024

@author: k5kei
"""

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from data import get_data

def plot_schedule(schedule, jobs, robots):
    fig, ax = plt.subplots()
    jobs, robots, distances = get_data()
    
    # 各ロボットの仕事リストを初期化
    robot_tasks = [[] for _ in range(len(robots))]
    robot_times = [0] * len(robots)  # 各ロボットの現在の時間
    robot_positions = [0] * len(robots)  # 各ロボットの現在の位置

    # 仕事に名前を付ける
    job_names = [chr(65 + i) for i in range(len(jobs))]  # A, B, C, ...

    # 仕事ごとの色を生成
    colors = list(mcolors.TABLEAU_COLORS.values())
    travel_color = 'grey'  # 移動時間の色

    for job_idx, robot_idx in enumerate(schedule):
        job = jobs[job_idx]
        robot_idx = int(round(robot_idx))  # インデックスを整数に変換
        robot = robots[robot_idx]

        travel_time = distances[robot_positions[robot_idx]][job['location']]
        execution_time = job['workload'] / robot['capacity']
        start_time = robot_times[robot_idx] + travel_time

        # 移動時間を追加
        if travel_time > 0:
            robot_tasks[robot_idx].append((robot_times[robot_idx], travel_time, None))
        
        # 仕事時間を追加
        robot_tasks[robot_idx].append((start_time, execution_time, job_idx))
        robot_times[robot_idx] = start_time + execution_time
        robot_positions[robot_idx] = job['location']

    # グラフの描画
    for robot_idx, tasks in enumerate(robot_tasks):
        for start_time, duration, job_idx in tasks:
            if job_idx is None:
                color = travel_color  # 移動時間の色
                label = 'Travel'
            else:
                color = colors[job_idx % len(colors)]  # 仕事ごとの色
                label = job_names[job_idx]

            ax.broken_barh([(start_time, duration)], (robot_idx * 10, 9), facecolors=(color))
            if job_idx is not None:
                ax.text(start_time + duration / 2, robot_idx * 10 + 4.5, label, 
                        ha='center', va='center', color='white', fontsize=8, fontweight='bold')

    ax.set_xlabel('Time')
    ax.set_ylabel('Robot')
    ax.set_yticks([i * 10 + 5 for i in range(len(robots))])
    ax.set_yticklabels([f'Robot {i+1}' for i in range(len(robots))])
    plt.show()
