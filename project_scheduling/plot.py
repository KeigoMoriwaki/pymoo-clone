# -*- coding: utf-8 -*-
"""
Created on Thu May 30 20:02:17 2024

@author: k5kei
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_schedule(result, J, R, T, robot_types):
    schedule = result.X.reshape((len(R), T))  # ロボットごとのスケジュールを保持
    failed_tasks = result.algorithm.pop.get("failed_tasks")[0]
    moving_tasks = result.algorithm.pop.get("moving_tasks")[0]  # 移動中の情報を取得
    
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.get_cmap('tab10', len(J))  # タスク数に基づいたカラーマップを設定
    
    # ロボットと時間ごとのタスク割り当てを確認し、タスクIDを対応付け
    task_allocation = np.zeros((len(R), T))  # ロボット x 時間のタスク割り当て

    # スケジュールデータに基づき、ロボットが担当するタスクを確認
    for r in range(len(R)):  # 各ロボットについて
        for t in range(T):  # 各時間について
            task_id = schedule[r, t]  # 各ロボットのスケジュールからタスクIDを確認
            if task_id > 0 and task_id <= len(J):  # タスクが割り当てられている場合
                task_allocation[r, t] = task_id
    
    # グラフの描画
    for r in range(len(R)):
        for t in range(T):
            task_id = task_allocation[r, t]
            
            if moving_tasks[r, t] == 1:  # 移動中の場合
                face_color = 'white'  # 移動中は背景を白にする
                text_color = 'black'  # 文字色は黒に設定
                ax.broken_barh([(t, 1)], (r, 1), facecolors=(face_color))
                ax.text(t + 0.5, r + 0.5, "move", ha='center', va='center', color=text_color)  # 移動中には「move」を表示
            
            elif task_id > 0:  # タスクが割り当てられている場合
                face_color = colors(int(task_id - 1))  # タスクに対応する色
                text_color = 'white' if failed_tasks[r, t] == 1 else 'black'  # 故障時は白色、それ以外は黒色
                ax.broken_barh([(t, 1)], (r, 1), facecolors=(face_color))
                ax.text(t + 0.5, r + 0.5, f"T{int(task_id)}", ha='center', va='center', color=text_color)  # タスクIDを表示

    ax.set_xlabel('Time')
    ax.set_ylabel('Robot')
    ax.set_yticks(np.arange(len(R)) + 0.5)
    ax.set_yticklabels([f'R{r} ({robot_types[r]})' for r in R])
    ax.set_xticks(np.arange(T + 1))
    plt.show()