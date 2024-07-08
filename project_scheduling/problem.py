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
    #     - a[j,r,t]: resource r usage for job j on period t (after job starts)
    #     - RUB[r,t]: upper bound for resource r on period t

    def __init__(self, problem_data):
        self.J, self.P, self.R, self.T, self.p, self.RUB, self.backup_robots = problem_data
        n_var = len(self.J) * self.T
        super().__init__(n_var=n_var,
                         n_obj=1,
                         n_constr=2,  # 制約条件を追加
                         xl=0,
                         xu=len(self.R),
                         type_var=int)

    def _evaluate(self, x, out, *args, **kwargs):
        finish_times = []
        constraints = []

        for ind in x:
            schedule = ind.reshape((len(self.J), self.T))
            leftover = copy.deepcopy(self.p)
            t = 0

            for t, s in enumerate(schedule.T):
                for i, j in enumerate(s):
                    if j != 0:
                        leftover[i + 1] = max(0, leftover[i + 1] - 1)
                if sum(leftover.values()) == 0:
                    break
            finish_times.append(t + 1)  # タスクが終了した時刻を記録

            resource_constraints = []
            backup_constraints = []
            for t, s in enumerate(schedule.T):
                n_worker = np.zeros(len(self.R))
                for i, j in enumerate(s):
                    if j != 0:
                        n_worker[j-1] += 1
                for r in range(len(self.R)):
                    if self.RUB[(r+1, t+1)] - n_worker[r] < 0:
                        resource_constraints.append(self.RUB[(r+1, t+1)] - n_worker[r])
                    # バックアップロボットが使用されているか確認
                    if (r+1) in self.backup_robots and self.RUB[(r+1, t+1)] - n_worker[r] < 0:
                        backup_constraints.append(self.RUB[(r+1, t+1)] - n_worker[r])
            if len(resource_constraints) == 0:
                resource_constraints.append(0)
            constraints.append(sum(resource_constraints))
            if len(backup_constraints) == 0:
                backup_constraints.append(0)
            constraints.append(sum(backup_constraints))

        out["F"] = np.array(finish_times).reshape(-1, 1)  # 正しい形状に変換
        out["G"] = np.array(constraints).reshape(-1, 2)  # 制約条件が2つになったので形状も修正


