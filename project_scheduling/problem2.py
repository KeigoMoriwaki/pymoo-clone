# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 21:19:42 2024

@author: k5kei
"""

import numpy as np 
from pymoo.core.problem import Problem
import random  # シード管理用に追加

class ResourceConstrainedSchedulingProblem2(Problem):

    def __init__(self,robot_types, robot_initial_positions, J, p, task_attributes, P, R, T, robot_abilities, workspace, workspace_distance, moving_cost, C, RUB, seed = None):
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        self.robot_types = robot_types
        self.robot_initial_positions = robot_initial_positions
        self.J = J
        self.p = p
        self.task_attributes = task_attributes
        self.P = P
        self.R = R
        self.T = T
        self.robot_abilities = robot_abilities
        self.workspace = workspace
        self.workspace_distance = workspace_distance
        self.moving_cost = moving_cost
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
        robot_types, robot_initial_positions, J, p, task_attributes, P, R, T, robot_abilities, workspace, workspace_distance, moving_cost, C, RUB = self.robot_types, self.robot_initial_positions, self.J, self.p, self.task_attributes, self.P, self.R, self.T, self.robot_abilities, self.workspace, self.workspace_distance, self.moving_cost, self.C, self.RUB

        x = x.reshape((x.shape[0], len(R), T))
    
        total_time2 = []
        failed_tasks2 = np.zeros_like(x)
        moving_tasks2 = np.zeros_like(x)  # 移動を記録するための配列
        half_task_flag2 = np.zeros_like(x)  # 新しいフラグを追加
        robot_failed2 = np.zeros((x.shape[0], len(R)), dtype=bool)  # ロボットごとの故障状態を追跡 (0: 正常, 1: 故障)
    
        for i in range(x.shape[0]):
            
            # シード値を定義
            seed = 45
            # シード値に基づいた乱数生成器を作成
            rng = np.random.default_rng(seed)
            
            workload2 = np.zeros(len(J))  # 各タスクの合計仕事量
            task_completed2 = np.zeros(len(J))
            task_completion_time2 = np.full(len(J), -1)  # タスクの完了時間を初期化
                
            print(f"--- Evaluation of Individual {i+1} ---")
                
            # 各ロボットの現在位置を初期位置に設定
            current_workspace = {r: self.robot_initial_positions[r + 1] for r in range(len(self.R))}
            remaining_distance = {r: 0 for r in range(len(R))}  # 移動中の残り距離
    
                # pop_size の10単位ごとにシード更新
                #if i % 10 == 0:
                    #np.random.seed(random.randint(0, 1000))  # 新しいシードで再設定
    
            for t in range(T):
                for r in range(len(R)):
                    if robot_failed2[i, r] == 1:  # 故障中のロボットは処理をスキップ
                        continue
                        
                    task2 = int(x[i, r, t])
    
                    if task2 > 0:
                        task_attr = task_attributes[task2]  # タスクの属性を取得
                        robot_type = robot_types[r + 1]    # ロボットの種類を取得
                        work = robot_abilities[robot_type][task_attr]  # 仕事量を取得
                        task_workspace = workspace[task2]  # タスクのworkspaceを取得
                            
                    # 現在の作業場所とタスクの作業場所が異なる場合、移動を考慮
                        if current_workspace[r] != task_workspace:
                            cost = moving_cost[current_workspace[r]][task_workspace]
                            work = work * (1 - cost / robot_abilities[robot_type]['move'])
                
                                # 作業量が減少したタスクを記録
                            half_task_flag2[i, r, t] = 1
                            current_workspace[r] = task_workspace
    
    
                            # タスクIDが前回と同じ場合、移動なしで作業を続行
                            #if current_workspace[r] == task_workspace:
                                #remaining_distance[r] = 0
                            #else:
                                # 異なるタスクの場合、移動距離を計算
                                #if remaining_distance[r] == 0:
                                    #remaining_distance[r] = workspace_distance[current_workspace[r]][task_workspace]
    
                                # 移動可能距離を取得
                                #move_ability = robot_abilities[robot_type]['move']
                                #remaining_distance[r] -= move_ability
    
                                # 移動中の場合の条件分岐
                                #if remaining_distance[r] > 0:
                                    # 移動中（remaining_distanceが0を超えている場合）、次の時間も移動を続行
                                    #moving_tasks[i, r, t] = 1  # 移動中のフラグを設定
                                    #print(f"[Time {t+1}] Robot {r+1} is moving, remaining distance: {remaining_distance[r]}.")
                                    #continue  # 移動中はタスクを実行しない
                                
                                #elif remaining_distance[r] == 0:
                                    # 移動完了（remaining_distanceが0の場合）
                                    #current_workspace[r] = task_workspace
                                    #remaining_distance[r] = 0  # 念のためremaining_distanceを0に設定
                                    #moving_tasks[i, r, t] = 1  # 移動完了フラグを設定
                                    #print(f"[Time {t+1}] Robot {r+1} completed move to workspace {current_workspace[r]}.")
                                    #continue  # 移動が完了した時間ではタスクを実行しない
                                
                                #elif remaining_distance[r] < 0:
                                    # 移動完了（remaining_distanceが0以下の場合）、タスクを実行可能
                                    #current_workspace[r] = task_workspace
                                    #half_task_flag[i, r, t] = 1  # half_task_flag を設定
                                    #print(f"[Time {t+1}] Robot {r+1} completed move to workspace {current_workspace[r]}, task execution with reduced workload.")
                                
                                    # ここで仕事量を半分にする
                                    #work = work / 2
    
                            # 順序制約を確認
                        for (pred_task, succ_task) in P:
                            if task2 > 0:  # タスクが割り当てられている場合
                                if workload2[pred_task - 1] < p[pred_task]:  # 順序制約を確認
                                    if task2 == succ_task:
                                        work = 0  # 順序制約に違反した場合、仕事量を0に設定
                                            #print(f"Order constraint prevents task {task} from progressing at time {t+1} by Robot {r+1}")
    

    
    
                            # タスクが順序制約を満たし、故障していない場合、仕事量をworkloadに反映
                        for j in range(len(J)):
                            if task2 == J[j]:
                                workload2[j] += work
                                print(f"Task {task2} (attribute: {task_attr}) executed by Robot {r+1} (type: {robot_type}) at time {t+1}: Workload = {workload2[j]}/{p[task2]}")
    
                                    
                            # タスクが完了しているかをチェック
                        if workload2[task2 - 1] >= p[task2]:
                            task_completed2[task2 - 1] = 1
                            if task_completion_time2[task2 - 1] == -1:
                                task_completion_time2[task2 - 1] = t + 1
                                print(f"Task {task2} completed at time {task_completion_time2[task2 - 1]}")
    
            # 全タスクの最大完了時間を評価値とする
            evaluation_value2 = 0
            if np.all(task_completed2):
                evaluation_value2 = np.max(task_completion_time2)
                print(f"All tasks completed by evaluation_value {evaluation_value2}")
            else:
                # 未完了タスクがある場合は、まずTを加算する
                evaluation_value2 += T
                print(f"Some tasks are incomplete. Base evaluation value: {evaluation_value2}")
        
                # 残りの仕事量を合算する
                for j in range(len(J)):
                    if task_completed2[j] == 0:
                        remaining_workload2 = p[J[j]] - workload2[j]
                        evaluation_value2 += remaining_workload2   # 残り仕事量のみを追加
                        print(f"Task {J[j]} is incomplete. Remaining workload: {remaining_workload2}. Total evaluation value now: {evaluation_value2}")
    
            total_time2.append(evaluation_value2)

        out["F2"] = total_time2
        out["failed_tasks2"] = failed_tasks2  # 故障したタスクを結果に含める
        out["moving_tasks2"] = moving_tasks2  # 移動中の情報を追加
        # 最後に out に half_task_flag を追加
        out["half_task_flag2"] = half_task_flag2