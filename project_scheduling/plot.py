# -*- coding: utf-8 -*-
"""
Created on Thu May 30 20:02:17 2024

@author: k5kei
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_schedule(result, problem_data):
    J, P, R, T, p, RUB, backup_robots = problem_data

    # 最適化結果からスケジュールを取得
    expected_shape = (len(J) * T,)
    if result.X.shape == expected_shape:  # 形状が期待通りの場合
        best_schedule = result.X.reshape((len(J), T))
    else:
        raise ValueError(f"Unexpected result.X shape: {result.X.shape}, expected {expected_shape}")

    fig, ax = plt.subplots()
    colors = plt.cm.get_cmap('tab20', len(J))

    for r in range(len(R)):
        for t in range(T):
            for j in range(len(J)):
                if best_schedule[j, t] == r + 1:  # ロボット r+1 が仕事 j を時間 t に担当している場合
                    ax.broken_barh([(t, 1)], (r * 10, 9), facecolors=colors(j))
                    ax.text(t + 0.5, r * 10 + 5, f'J{j+1}', ha='center', va='center', color='black')

    ax.set_xlabel('Time')
    ax.set_ylabel('Robots')
    ax.set_yticks(np.arange(len(R)) * 10 + 5)
    ax.set_yticklabels([f'R{r+1}' for r in range(len(R))])
    plt.show()