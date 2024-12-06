# -*- coding: utf-8 -*-
"""
Created on Thu May 30 20:02:17 2024

@author: k5kei
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_schedule(result1, J, R, T, robot_types):
    schedule = result1.X.reshape((len(R), T))  # ロボットごとのスケジュールを保持
    failed_tasks = result1.algorithm.pop.get("failed_tasks")[0]
    moving_tasks = result1.algorithm.pop.get("moving_tasks")[0]  # 移動中の情報を取得
    half_task_flag = result1.algorithm.pop.get("half_task_flag")[0]  # 新しいフラグを取得

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
                #ax.text(t + 0.5, r + 0.5, "move", ha='center', va='center', color=text_color)  # 移動中には「move」を表示

            elif half_task_flag[r, t] == 1 and task_id > 0 and failed_tasks[r, t] == 1:  # half_task_flagが設定されている場合
                task_color = colors(int(task_id - 1))  # タスクIDに対応する色
                ax.broken_barh([(t, 0.5)], (r, 1), facecolors='white')  # 左半分を白
                ax.broken_barh([(t + 0.5, 0.5)], (r, 1), facecolors=(task_color))  # 右半分をタスクの色
                ax.text(t + 0.5, r + 0.5, f"T{int(task_id)}", ha='center', va='center', color='white')

            elif half_task_flag[r, t] == 1 and task_id > 0:  # half_task_flagが設定されている場合
                task_color = colors(int(task_id - 1))  # タスクIDに対応する色
                ax.broken_barh([(t, 0.5)], (r, 1), facecolors='white')  # 左半分を白
                ax.broken_barh([(t + 0.5, 0.5)], (r, 1), facecolors=(task_color))  # 右半分をタスクの色
                ax.text(t + 0.5, r + 0.5, f"T{int(task_id)}", ha='center', va='center', color='black')

            elif task_id > 0:  # タスクが割り当てられている場合
                face_color = colors(int(task_id - 1))  # タスクに対応する色
                text_color = 'white' if failed_tasks[r, t] == 1 else 'black'  # 故障時は白色、それ以外は黒色
                ax.broken_barh([(t, 1)], (r, 1), facecolors=(face_color))
                if failed_tasks[r, t] == 1:
                    # 故障時に細い白線を重ねる
                    #ax.plot([t+0.005, t+0.975], [r+0.5, r+0.5], color='white', linewidth=1)
                    ax.text(t + 0.5, r + 0.5, f"T{int(task_id)}", ha='center', va='center', color=text_color)  # タスクIDを表示
                else:
                    ax.text(t + 0.5, r + 0.5, f"T{int(task_id)}", ha='center', va='center', color='black')

    # 内部の縦線を追加
    #for t in range(T + 1):  # T + 1とすることで終端にも線を追加
        #ax.vlines(t, ymin=0, ymax=len(R), colors='gray', linestyles='dotted', linewidth=0.5)

    # 凡例を追加
    #legend_labels = [f"T{int(j)}" for j in range(1, len(J) + 1)]
    #legend_patches = [plt.Line2D([0], [0], color=colors(j-1), lw=4) for j in range(1, len(J) + 1)]
    #ax.legend(legend_patches, legend_labels, title="Tasks", bbox_to_anchor=(1.05, 1), loc='upper left')

    # x軸とy軸のラベル設定
    ax.set_xlabel('Time')
    ax.set_ylabel('Robot')
    ax.set_yticks(np.arange(len(R)) + 0.5)
    ax.set_yticklabels([f'R{r} ({robot_types[r]})' for r in R])
    
    # x軸の目盛りを10刻みで設定し、そのラベルを1/10にした表示に変更
    ax.set_xticks(np.arange(T + 1))

    plt.show()

def plot_value_over_generations(min_value_over_gens1, seed):
    plt.figure(figsize=(10, 6))
    plt.plot(min_value_over_gens1, color='b', label=f'Seed {seed}')
    plt.xlabel('Generation')
    plt.ylabel('Minimum Evaluation Value')
    plt.title(f'Value Over Generations (Seed {seed})')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'value_over_generations_seed_{seed}.png')  # シードごとに保存
    plt.show()

def plot_average_value_over_generations(all_min_values1):
    # 各世代ごとの平均を計算
    all_min_values1 = np.array(all_min_values1)
    average_values = np.mean(all_min_values1, axis=0)

    plt.figure(figsize=(10, 6))
    plt.plot(average_values, color='r', label='Average Value')
    plt.xlabel('Generation')
    plt.ylabel('Average Minimum Evaluation Value')
    plt.title('Average Value Over Generations')
    plt.legend()
    plt.grid(True)
    plt.savefig('average_value_over_generations.png')  # 平均推移を保存
    plt.show()

def plot_schedule2(result2, J, R, T, robot_types):
    schedule = result2.X.reshape((len(R), T))  # ロボットごとのスケジュールを保持
    failed_tasks = result2.algorithm.pop.get("failed_tasks")[0]
    moving_tasks = result2.algorithm.pop.get("moving_tasks")[0]  # 移動中の情報を取得
    half_task_flag = result2.algorithm.pop.get("half_task_flag")[0]  # 新しいフラグを取得

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
                #ax.text(t + 0.5, r + 0.5, "move", ha='center', va='center', color=text_color)  # 移動中には「move」を表示

            elif half_task_flag[r, t] == 1 and task_id > 0 and failed_tasks[r, t] == 1:  # half_task_flagが設定されている場合
                task_color = colors(int(task_id - 1))  # タスクIDに対応する色
                ax.broken_barh([(t, 0.5)], (r, 1), facecolors='white')  # 左半分を白
                ax.broken_barh([(t + 0.5, 0.5)], (r, 1), facecolors=(task_color))  # 右半分をタスクの色
                ax.text(t + 0.5, r + 0.5, f"T{int(task_id)}", ha='center', va='center', color='white')

            elif half_task_flag[r, t] == 1 and task_id > 0:  # half_task_flagが設定されている場合
                task_color = colors(int(task_id - 1))  # タスクIDに対応する色
                ax.broken_barh([(t, 0.5)], (r, 1), facecolors='white')  # 左半分を白
                ax.broken_barh([(t + 0.5, 0.5)], (r, 1), facecolors=(task_color))  # 右半分をタスクの色
                ax.text(t + 0.5, r + 0.5, f"T{int(task_id)}", ha='center', va='center', color='black')

            elif task_id > 0:  # タスクが割り当てられている場合
                face_color = colors(int(task_id - 1))  # タスクに対応する色
                text_color = 'white' if failed_tasks[r, t] == 1 else 'black'  # 故障時は白色、それ以外は黒色
                ax.broken_barh([(t, 1)], (r, 1), facecolors=(face_color))
                if failed_tasks[r, t] == 1:
                    # 故障時に細い白線を重ねる
                    #ax.plot([t+0.005, t+0.975], [r+0.5, r+0.5], color='white', linewidth=1)
                    ax.text(t + 0.5, r + 0.5, f"T{int(task_id)}", ha='center', va='center', color=text_color)  # タスクIDを表示
                else:
                    ax.text(t + 0.5, r + 0.5, f"T{int(task_id)}", ha='center', va='center', color='black')

    # 内部の縦線を追加
    #for t in range(T + 1):  # T + 1とすることで終端にも線を追加
        #ax.vlines(t, ymin=0, ymax=len(R), colors='gray', linestyles='dotted', linewidth=0.5)

    # 凡例を追加
    #legend_labels = [f"T{int(j)}" for j in range(1, len(J) + 1)]
    #legend_patches = [plt.Line2D([0], [0], color=colors(j-1), lw=4) for j in range(1, len(J) + 1)]
    #ax.legend(legend_patches, legend_labels, title="Tasks", bbox_to_anchor=(1.05, 1), loc='upper left')

    # x軸とy軸のラベル設定
    ax.set_xlabel('Time')
    ax.set_ylabel('Robot')
    ax.set_yticks(np.arange(len(R)) + 0.5)
    ax.set_yticklabels([f'R{r} ({robot_types[r]})' for r in R])

    # x軸の目盛りを10刻みで設定し、そのラベルを1/10にした表示に変更
    ax.set_xticks(np.arange(T + 1))

    plt.show()

def plot_value_over_generations2(min_value_over_gens2, seed):
    plt.figure(figsize=(10, 6))
    plt.plot(min_value_over_gens2, color='b', label=f'Seed {seed}')
    plt.xlabel('Generation')
    plt.ylabel('Minimum Evaluation Value')
    plt.title(f'Value Over Generations (Seed {seed})')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'value_over_generations2_seed_{seed}.png')  # シードごとに保存
    plt.show()

def plot_average_value_over_generations2(all_min_values2):
    # 各世代ごとの平均を計算
    all_min_values2 = np.array(all_min_values2)
    average_values = np.mean(all_min_values2, axis=0)

    plt.figure(figsize=(10, 6))
    plt.plot(average_values, color='r', label='Average Value')
    plt.xlabel('Generation')
    plt.ylabel('Average Minimum Evaluation Value')
    plt.title('Average Value Over Generations')
    plt.legend()
    plt.grid(True)
    plt.savefig('average_value_over_generations2.png')  # 平均推移を保存
    plt.show()