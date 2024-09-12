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
        
        print(f"x.shape before reshape: {x.shape}")
        x = x.reshape((x.shape[0], len(J), T))
        print(f"x.shape after reshape: {x.shape}")

        total_work = np.array([[np.sum(xi[j] > 0) for j in range(len(J))] for xi in x])
        finish_times = np.ceil(total_work / np.array([p[j+1] for j in range(len(J))])).astype(int)

        total_cost = []

        constraints = []
        failed_tasks = np.zeros_like(x)

        for i in range(x.shape[0]):
            total_workload = np.zeros(len(J))  # 各タスクの合計仕事量
            
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
                    
                    total_workload[j] += x[i, j, t]  # タスクjの仕事量を合算

            task_completion = total_workload - np.array([p[j+1] for j in range(len(J))])  # 仕事量からpを引く

            if np.all(task_completion >= 0):
                evaluation_value = np.max(np.nonzero(total_workload)[0])  # タスクが割り振られた最後の時間
            else:
                evaluation_value = T - np.sum(task_completion[task_completion < 0])

            total_cost.append(evaluation_value)

        precedence_constraints = np.sum([x[:, pair[0] - 1] - x[:, pair[1] - 1] for pair in self.P], axis=1)
        print(f"precedence_constraints.shape: {precedence_constraints.shape}")
        constraints.append(precedence_constraints)


        for t in range(T):
            for r in range(1, len(R) + 1):
                resource_constraints = [np.sum([xi[j, t] == r for j in range(len(J))]) - 1 for xi in x]
                print(f"resource_constraints.shape (t={t}, r={r}): {np.shape(resource_constraints)}")
                constraints.append(resource_constraints)

        constraints = np.hstack(constraints)

        out["F"] = total_cost
        out["G"] = constraints
        out["failed_tasks"] = failed_tasks  # Include failed tasks in the output