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
        n_var = len(R) * T
        super().__init__(n_var=n_var,
                         n_obj=1,
                         #n_constr=len(P) + len(R) * T,
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
        x = x.reshape((x.shape[0], len(R), T))
        #print(f"x.shape after reshape: {x.shape}")


        total_cost = []
        failed_tasks = np.zeros_like(x)

        for i in range(x.shape[0]):
            #w = np.zeros_like(x[i])  # 仕事量の変数を新たに定義
            workload = np.zeros(len(J))  # 各タスクの合計仕事量
            task_completed = np.zeros(len(J))  # タスクの完了時間
            
            for t in range(T):
                for r in range(len(R)):
                    robot = int(x[i, r, t])

                    if robot > 0:
                        # w(x(t,r)) として仕事量を定義
                        work = 1  # 初期仕事量を1と設定

                        # 順序制約を確認
                        for (pred_task, succ_task) in P:
                            if task_completed[pred_task - 1] < 1 and robot == succ_task:
                                work = 0  # 順序制約に違反した場合、仕事量を0に設定

                        # 故障確率の判定
                        success_prob = (1 - C) ** t
                        if np.random.random() > success_prob:
                            work = 0  # 故障時に仕事量を0に設定
                            failed_tasks[i, r, t] = 1

                        # タスクが順序制約を満たし、故障していない場合、仕事量をworkloadに反映
                        for j in range(len(J)):
                            if robot == J[j]:
                                workload[j] += work

                        # 各タスクが完了しているかをチェック
                        for j in range(len(J)):
                            if workload[j] >= p[J[j]]:
                                task_completed[j] = 1  # タスクが完了したらフラグを立てる

            # 最後に全タスクの完了時間を計算
            evaluation_value = 0
            for j in range(len(J)):
                if task_completed[j] == 1:
                    evaluation_value += 1  # タスクが完了していれば評価値を加算
                else:
                    # 未完了タスクのペナルティを計算
                    evaluation_value += T + (p[J[j]] - workload[j])

            total_cost.append(evaluation_value)
            
        out["F"] = total_cost
        out["failed_tasks"] = failed_tasks  # 故障したタスクを結果に含める
        