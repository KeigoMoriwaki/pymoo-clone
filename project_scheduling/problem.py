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
        super().__init__(n_var=n_var,
                         n_obj=1,
                         n_constr=1,
                         xl=0,
                         xu=len(self.R),
                         type_var=int)


    def _evaluate(self, x, out, *args, **kwargs):
        finish_times = []
        constraints = []

        for ind in x:
            schedule = ind.reshape((len(self.J), self.T))
            leftover = copy.deepcopy(self.p)
            resource_constraints = 0
            t = 0
            for t in range(self.T):
                n_worker = np.zeros(len(self.R))
                for j in range(len(self.J)):
                    robot = schedule[j, t]
                    if robot != 0:
                        if n_worker[robot-1] > 0:
                            resource_constraints += 1  # 同じロボットに複数のタスクが割り当てられた場合のペナルティ
                        n_worker[robot-1] += 1
                        leftover[self.J[j]] -= 1
                        if leftover[self.J[j]] <= 0:
                            leftover[self.J[j]] = 0

                if sum(leftover.values()) == 0:
                    break

            finish_times.append(t + 1)

            for t in range(self.T):
                n_worker = np.zeros(len(self.R))
                for j in range(len(self.J)):
                    robot = schedule[j, t]
                    if robot != 0:
                        n_worker[robot-1] += 1
                for r in range(len(self.R)):
                    if self.RUB[(r+1, t+1)] < n_worker[r]:
                        resource_constraints += 1

            constraints.append(resource_constraints)

        out["F"] = np.array(finish_times).reshape(-1, 1)
        out["G"] = np.array(constraints).reshape(-1, 1)

        # 新しい評価ロジックの追加
        additional_constraints = []
        for ind in x:
            schedule = ind.reshape((len(self.J), self.T))
            task_constraints = 0
            for j in range(len(self.J)):
                total_work = 0
                for t in range(self.T):
                    if schedule[j, t] != 0:
                        total_work += 1
                if total_work != self.p[self.J[j]]:
                    task_constraints += 1

            additional_constraints.append(task_constraints)

        additional_constraints = np.array(additional_constraints).reshape(-1, 1)
        out["G"] = np.hstack((out["G"], additional_constraints)).sum(axis=1).reshape(-1, 1)