# -*- coding: utf-8 -*-
"""
Created on Thu May 30 20:02:17 2024

@author: k5kei
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_schedule(R, T, p, x, title="Schedule"):
    """
    ロボットのスケジュールを可視化する関数。

    Parameters:
    R (list): ロボットのリスト
    T (int): 期間の数
    p (dict): ジョブの処理時間
    x (ndarray): スケジュール (ジョブ数 x 期間数)
    title (str): グラフのタイトル
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    # ロボットごとに色を分けるためのカラーマップ
    cmap = plt.get_cmap("tab10")
    colors = cmap.colors

    for j in range(x.shape[0]):
        for t in range(x.shape[1]):
            if x[j, t] > 0:
                robot = int(np.round(x[j, t])) - 1
                start_time = t
                end_time = start_time + p[j + 1]
                ax.broken_barh([(start_time, p[j + 1])], (robot - 0.4, 0.8), facecolors=(colors[j % len(colors)]))
                ax.text(start_time + p[j + 1] / 2, robot, f'Job {j+1}', 
                        ha='center', va='center', color='black')

    ax.set_xlabel('Time')
    ax.set_ylabel('Robot')
    ax.set_yticks(range(len(R)))
    ax.set_yticklabels([f'Robot {r}' for r in R])
    ax.set_xticks(range(T + 1))
    ax.set_xlim(0, T)
    ax.set_title(title)
    plt.show()
