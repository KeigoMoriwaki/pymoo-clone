# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:32:04 2024

@author: k5kei
"""

import numpy as np 
from pymoo.core.problem import Problem

class ResourceConstrainedSchedulingProblem(Problem):

    def __init__(self, J, p, P, R, T, C, RUB):
        #print(f"Debug: Inside class, J={J}, P={P}, R={R}, T={T}, p={p}, C={C}, RUB={RUB}")
        # Rがリストで、Tが整数であることを確認
        #print(f"Type of R: {type(R)}, Value of R: {R}")
        #print(f"Type of T: {type(T)}, Value of T: {T}")
        print(f"Type of P: {type(P)}, Value of R: {P}")
        self.J = J
        self.p = p
        self.P = P
        self.R = R
        self.T = T
        self.C = C  # Cを故障確率として使用
        self.RUB = RUB
        n_var = len(J) * T
        super().__init__(n_var=n_var,
                         n_obj=1,
                         n_constr=len(P) + len(R) * T,
                         xl=1,
                         xu=len(R),
                         type_var=int)

    def _evaluate(self, x, out, *args, **kwargs):
        J, p, P, R, T, C, RUB = self.J, self.p, self.P, self.R, self.T, self.C, self.RUB
        
        #print(f"J: {J}")
        #print(f"p: {p}")
        #print(f"P: {P}")
        #print(f"R: {R}")
        #print(f"T: {T}")
        #print(f"C: {C}")
        #print(f"RUB: {RUB}")
        #print(f"x: {x}")
        
        #print(f"x.shape before reshape: {x.shape}")
        x = x.reshape((x.shape[0], len(J), T))
        #print(f"x.shape after reshape: {x.shape}")


        total_cost = []
        failed_tasks = np.zeros_like(x)

        for i in range(x.shape[0]):
            #w = np.zeros_like(x[i])  # 仕事量の変数を新たに定義
            total_workload = np.zeros(len(J))  # 各タスクの合計仕事量
            task_completion_time = np.zeros(len(J))  # タスクの完了時間
            
            for t in range(T):
                for j in range(len(J)):
                    robot = int(x[i, j, t])
                    if robot > 0:
                        success_prob = (1 - C) ** t
                        #print(f"Robot {robot} at time {t}, success_prob: {success_prob}")
                        if np.random.random() > success_prob:
                            x[i, j, t] = (1 - C)  
                            failed_tasks[i, j, t] = 1  # 故障判定時、failed_tasksをカウントする。
                            #print(f"Task {j} at time {t} failed. New value: {x[i, j, t]}")
                        else:
                            x[i, j, t] = 1  
                            
                    # ここで順序制約を確認
                    for (x, y) in P:
                        # 先行タスクが完了していない場合、後続タスク y の仕事量を 0 にする
                        if total_workload[x - 1] < p[x]:
                            if y - 1 == j:
                                x[i, j, t] = 0  # 後続タスク y の仕事量を 0 にする
                    
                # タスクの合計仕事量を更新
                for j in range(len(J)):
                    total_workload[j] += x[i, j, t]  # タスクjの仕事量を合算


            # タスクが完了しているかどうかを確認
            for j in range(len(J)):
                if total_workload[j] >= p[j + 1]:
                    evaluation_value = t  # タスクが完了した最後の時間
                else:
                # タスクが完了していない場合はTを使用
                    evaluation_value = T + np.sum(np.maximum(0, p[j + 1] - total_workload[j]) for j in range(len(J)))

            total_cost.append(evaluation_value)
            
        out["F"] = total_cost
        out["failed_tasks"] = failed_tasks  # 故障したタスクを結果に含める
        