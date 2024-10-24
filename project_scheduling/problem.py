# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:32:04 2024

@author: k5kei
"""

import numpy as np 
from pymoo.core.problem import Problem

class ResourceConstrainedSchedulingProblem(Problem):

    def __init__(self, J, p, task_attributes, P, R, robot_types, T, robot_capacities, workspace, workspace_distance, C, RUB):
        #print(f"Debug: Inside class, J={J}, P={P}, R={R}, T={T}, p={p}, C={C}, RUB={RUB}")
        # Rがリストで、Tが整数であることを確認
        #print(f"Type of R: {type(R)}, Value of R: {R}")
        #print(f"Type of T: {type(T)}, Value of T: {T}")
        #print(f"Type of P: {type(P)}, Value of R: {P}")
        self.J = J
        self.p = p
        self.task_attributes = task_attributes
        self.P = P
        self.R = R
        self.robot_types = robot_types
        self.T = T
        self.robot_capacities = robot_capacities
        self.workspace = workspace
        self.workspace_distance = workspace_distance
        self.C = C  # Cを故障確率として使用
        self.RUB = RUB
        n_var = len(R) * T
        super().__init__(n_var=n_var,
                         n_obj=1,
                         #n_constr=len(P) + len(R) * T,
                         xl=1,
                         xu=len(J),
                         type_var=int)

    def _evaluate(self, x, out, *args, **kwargs):
        J, p, task_attributes, P, R, robot_types, T, robot_capacities, workspace, workspace_distance, C, RUB = self.J, self.p, self.task_attributes, self.P, self.R, self.robot_types, self.T, self.robot_capacities, self.workspace, self.workspace_distance, self.C, self.RUB

        x = x.reshape((x.shape[0], len(R), T))

        total_time = []
        failed_tasks = np.zeros_like(x)
        moving_tasks = np.zeros_like(x)  # 移動を記録するための配列

        for i in range(x.shape[0]):
            workload = np.zeros(len(J))  # 各タスクの合計仕事量
            task_completed = np.zeros(len(J))
            task_completion_time = np.full(len(J), -1)  # タスクの完了時間を初期化
            
            print(f"--- Evaluation of Individual {i+1} ---")
            
            # 各ロボットの現在の workspace と移動残距離をトラッキング
            current_workspace = {r: None for r in range(len(R))}
            remaining_distance = {r: 0 for r in range(len(R))}  # 移動中の残り距離

            for t in range(T):
                for r in range(len(R)):
                    task = int(x[i, r, t])

                    if task > 0:
                        task_attr = task_attributes[task]  # タスクの属性を取得
                        robot_type = robot_types[r + 1]    # ロボットの種類を取得
                        work = robot_capacities[robot_type][task_attr]  # 仕事量を取得
                        task_workspace = workspace[task]  # タスクのworkspaceを取得

                        # 初回のタスクの場合
                        if current_workspace[r] is None:
                            current_workspace[r] = task_workspace
                            remaining_distance[r] = 0  # 初回のタスクでは移動不要

                        # 前回のタスクと異なる場合、移動を行う必要がある
                        elif current_workspace[r] != task_workspace:
                            if remaining_distance[r] == 0:
                                # 移動が必要な距離を計算
                                remaining_distance[r] = workspace_distance[current_workspace[r]][task_workspace]
                                print(f"Robot {r+1} starts moving from workspace {current_workspace[r]} to {task_workspace}. Total distance: {remaining_distance[r]}")
                            
                            move_capacity = robot_capacities[robot_type]['move']

                            if remaining_distance[r] > 0:
                                # 1期間で移動できる距離が足りない場合、移動を続ける
                                if remaining_distance[r] > move_capacity:
                                    remaining_distance[r] -= move_capacity
                                    moving_tasks[i, r, t] = 1  # 移動中のフラグを立てる
                                    print(f"Robot {r+1} is moving. Remaining distance: {remaining_distance[r]} at time {t+1}")
                                    continue  # この期間はタスク実行なし
                                else:
                                    # 移動が完了
                                    current_workspace[r] = task_workspace
                                    remaining_distance[r] = 0
                                    moving_tasks[i, r, t] = 1  # 移動中のフラグを立てる
                                    print(f"Robot {r+1} completed moving to workspace {task_workspace} at time {t+1}")
                                    continue  # この期間はタスク実行なし
                            else:
                                current_workspace[r] = task_workspace
                                continue

                        # 順序制約を確認
                        for (pred_task, succ_task) in P:
                            if task > 0:  # タスクが割り当てられている場合
                                if workload[pred_task - 1] < p[pred_task]:  # 順序制約を確認
                                    if task == succ_task:
                                        work = 0  # 順序制約に違反した場合、仕事量を0に設定
                                        #print(f"Order constraint prevents task {task} from progressing at time {t+1} by Robot {r+1}")

                        # 故障確率の判定
                        success_prob = (1 - C) ** t
                        if np.random.random() > success_prob:
                            work = 0  # 故障時に仕事量を0に設定
                            failed_tasks[i, r, t] = 1
                            print(f"Robot {r+1} failed at time {t+1} for task {task}")

                            continue

                        # タスクが順序制約を満たし、故障していない場合、仕事量をworkloadに反映
                        for j in range(len(J)):
                            if task == J[j]:
                                workload[j] += work
                                print(f"Task {task} (attribute: {task_attr}) executed by Robot {r+1} (type: {robot_type}) at time {t+1}: Workload = {workload[j]}/{p[task]}")

                                
                        # タスクが完了しているかをチェック
                        if workload[task - 1] >= p[task]:
                            task_completed[task - 1] = 1
                            if task_completion_time[task - 1] == -1:
                                task_completion_time[task - 1] = t + 1
                                print(f"Task {task} completed at time {task_completion_time[task - 1]}")

            

            # 全タスクの最大完了時間を評価値とする
            evaluation_value = 0
            if np.all(task_completed):
                evaluation_value = np.max(task_completion_time)
                print(f"All tasks completed by evaluation_value {evaluation_value}")
            else:
                # 未完了タスクがある場合は、まずTを加算する
                evaluation_value += T
                print(f"Some tasks are incomplete. Base evaluation value: {evaluation_value}")
    
                # 残りの仕事量を合算する
                for j in range(len(J)):
                    if task_completed[j] == 0:
                        remaining_workload = p[J[j]] - workload[j]
                        evaluation_value += remaining_workload  # 残り仕事量のみを追加
                        print(f"Task {J[j]} is incomplete. Remaining workload: {remaining_workload}. Total evaluation value now: {evaluation_value}")

            total_time.append(evaluation_value)

            
        out["F"] = total_time
        out["failed_tasks"] = failed_tasks  # 故障したタスクを結果に含める
        out["moving_tasks"] = moving_tasks  # 移動中の情報を追加