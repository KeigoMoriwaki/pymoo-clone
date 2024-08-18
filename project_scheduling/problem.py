# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:32:04 2024

@author: k5kei
"""

import numpy as np
import copy
from pymoo.core.problem import Problem

class ResourceConstrainedSchedulingProblem(Problem):
    # Parameters:
    #     - J: set of jobs
    #     - P: set of precedence constraints between jobs
    #     - R: set of resources
    #     - T: number of periods
    #     - p[j]: processing time of job j
    #     - RUB[r,t]: upper bound for resource r on period t
    #     - C: failure probability coefficient

    def __init__(self, problem_data):
        self.J, self.P, self.R, self.T, self.p, self.RUB, self.C = problem_data
        n_var = len(self.J) * self.T
        num_resource_constraints = len(self.R) * self.T
        num_precedence_constraints = len(self.P)
        num_task_constraints = len(self.J)
        n_constr = num_resource_constraints + num_precedence_constraints + num_task_constraints
        super().__init__(n_var=n_var,
                         n_obj=1,
                         n_constr=n_constr,
                         xl=1,
                         xu=len(self.R),
                         type_var=int)

    def _evaluate(self, x, out, *args, **kwargs):
        num_samples = len(x)
        finish_times = []
        constraints = np.zeros((num_samples, self.n_constr))
        # 閾値の設定
        threshold = 10

        for ind in x:
            ind = np.array(ind).reshape((len(self.J), self.T))
            schedule = ind
            leftover = copy.deepcopy(self.p)
            resource_constraints = 0
            precedence_constraints = 0
            task_constraints = 0

            failed = np.zeros((len(self.J), self.T))
            
            for t in range(self.T):
                # ロボットの稼働状況を記録する配列
                robot_status = np.zeros(len(self.R))
                # 優先度の高いタスクから順に処理
                for j in sorted(range(len(self.J)), key=lambda j: self.P[j][0] if j < len(self.P) and self.P[j] else float('inf')):
                # 前提条件を満たしているか確認
                    if all(schedule[p, t] == 0 for p in self.P[j] for t in range(self.T)):  # ここでTに変更
                        # タスクを割り当てるロボットを選択
                        for robot in range(len(self.R)):  # ここでrobotを定義
                            if robot_status[robot] == 0:  # ロボットが空いている場合
                                # 空きのあるロボットにタスクを割り当てる
                                schedule[j, t] = robot + 1
                                robot_status[robot] = 1
                                break  # 最初の空いているロボットに割り当てたらループを抜ける
                    # 同じロボットに複数のタスクが割り当てられた場合は大きなペナルティ
                    else:
                        # 同じ時間帯に同じロボットに複数のタスクが割り当てられた場合、ペナルティ
                        resource_constraints += 10000

                        leftover[self.J[j]] -= 1
                        if leftover[self.J[j]] <= 0:
                            leftover[self.J[j]] = 0

                if sum(leftover.values()) == 0:
                    break

            finish_times.append(t + 1)

            for t in range(self.T):
                for r in range(len(self.R)):
                    # 同じロボットに割り当てられたタスクの数をカウント
                    is_assigned = (schedule[:, t] == r+1).astype(int)
                    num_tasks_assigned = np.sum(is_assigned)
                    # 同じロボットに複数のタスクが割り当てられている場合、ペナルティを課す
                    resource_constraints += np.sum(is_assigned * (is_assigned - 1))
                
            task_finish_time = {}
            
            for j in range(len(self.J)):
                for t in range(self.T):
                    if schedule[j, t] != 0 and failed[j, t] == 0:
                        task_finish_time[self.J[j]] = t + 1

            for element in self.P:
                if len(element) == 2:  # 要素がタプルで、要素数が2の場合
                    x, y = element
                    if task_finish_time.get(x, 0) >= task_finish_time.get(y, self.T + 1):
                        precedence_constraints += 1
                else:
                    print(f"Warning: Element in self.P is not a tuple of length 2: {element}")

            for j in range(len(self.J)):
                total_work = 0
                for t in range(self.T):
                    if schedule[j, t] != 0 and failed[j, t] == 0:
                        total_work += 1
                if total_work != self.p[self.J[j]]:
                    task_constraints += 100
                    
            # 3つの制約値を結合
            total_constraints = np.array([resource_constraints, precedence_constraints, task_constraints]).sum(axis=0)
            # 各サンプルの制約ベクトルを追加
            constraints[ind] = total_constraints
            
            def simulate_task_execution(schedule, p):
                # 各タスクの開始時刻と終了時刻を格納する辞書
                start_times = {}
                end_times = {}

            # 各時間帯で実行するタスクを決定
                for t in range(self.T):
                    for j in range(len(self.J)):
                        robot = schedule[j, t]
                        if robot != 0:
                            # 同じロボットが割り当てられたタスクの中で、数字が小さいタスクを優先
                            if robot not in start_times:
                                start_times[robot] = t
                            else:
                                start_times[robot] += 1
                            end_times[robot] = start_times[robot] + self.p[self.J[j]]

                return start_times, end_times
            
            

            
        constraints = np.array(constraints)
        num_constraints = constraints.shape[1]
        if num_constraints != self.n_constr:
            raise ValueError(f"Expected {self.n_constr} constraints but got {num_constraints}. Constraints: {constraints}")

        # 閾値を超えた場合はペナルティを大きくする
        if total_constraints > threshold:
            total_constraints *= 1000

        out["F"] = np.array(finish_times).reshape(-1, 1) 
        out["G"] = constraints.reshape(num_samples, self.n_constr)
        
        
        
        
        
        #ロボットに対して同時間帯に2つ以上のタスクを割り振らないようにするのではなく
        #タスクのIDが若い方を優先するようにする