# -*- coding: utf-8 -*-
"""
Created on Thu May 30 20:02:17 2024

@author: k5kei
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_schedule(result, J, R, T):
    #print(f"Debug in plot_schedule: T={T}"
    schedule = result.X.reshape((len(R), T))
    failed_tasks = result.algorithm.pop.get("failed_tasks")[0]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.get_cmap('tab10', len(J))
    
    # 各ロボットが担当するタスクを追跡するための配列
    task_allocation = np.zeros((len(R), T))  # ロボット x 時間のタスク割り当て

    # スケジュールデータからタスクの割り当てを確認
    for r in range(len(R)):  # 各ロボットについて
        for t in range(T):  # 各時間について
            # ロボットrが時間tに実行しているタスクがある場合、task_allocationに記録
            task_id = schedule[r, t]
            if task_id > 0:  # タスクが割り当てられている場合
                task_allocation[r, t] = task_id  # タスク番号を割り当て
    
    # グラフの描画
    for r in range(len(R)):  # 各ロボットについて
        for t in range(T):  # 各時間について
            task_id = task_allocation[r, t]
            if task_id > 0:  # タスクが割り当てられている場合のみ描画
                face_color = colors(int(task_id - 1))  # タスクに対応する色
                text_color = 'white' if failed_tasks[r, t] == 1 else 'black'  # 故障時は白色、それ以外は黒色
                ax.broken_barh([(t, 1)], (r, 1), facecolors=(face_color))
                ax.text(t + 0.5, r + 0.5, f"T{int(task_id)}", ha='center', va='center', color=text_color)  # タスクIDを表示
    
    ax.set_xlabel('Time')
    ax.set_ylabel('Robot')
    ax.set_yticks(np.arange(len(R)) + 0.5)
    ax.set_yticklabels([f'R{r}' for r in R])
    ax.set_xticks(np.arange(T + 1))
    plt.show()
    
