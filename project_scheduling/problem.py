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
                         n_constr=len(self.R) * self.T,  # 各ロボットの各時間ステップに対する制約
                         xl=0,
                         xu=len(self.R),
                         type_var=int)


    def _evaluate(self, x, out, *args, **kwargs):
        finish_times = []
        constraints = []

        for ind in x:
            schedule = ind.reshape((len(self.J), self.T))
            leftover = {i: self.p[i + 1] for i in range(len(self.J))}
            robot_usage = np.zeros((len(self.R), self.T))
            task_completion = np.zeros(len(self.J))
            constraint_violation = np.zeros(len(self.R) * self.T)

            for t in range(self.T):
                robot_assigned = [False] * len(self.R)
                for i in range(len(self.J)):
                    j = schedule[i, t]
                    if j != 0:
                        robot_index = j - 1
                        if not robot_assigned[robot_index] and leftover[i] > 0:
                            if robot_usage[robot_index, t] == 0:
                                leftover[i] = max(0, leftover[i] - 1)
                                robot_usage[robot_index, t] += 1
                                if leftover[i] == 0:
                                    task_completion[i] = t 
                                robot_assigned[robot_index] = True
                            else:
                                schedule[i, t] = 0 
                        else:
                            schedule[i, t] = 0 

            for r in range(len(self.R)):
                for t in range(self.T):
                    if robot_usage[r, t] > 1:
                        constraint_violation[r * self.T + t] = robot_usage[r, t] - 1

            finish_time = max(task_completion)
            if finish_time == 0:
                finish_time = self.T
            finish_times.append(finish_time)

            constraints.append(constraint_violation)

            for t in range(self.T):
                failure_prob = 1 - self.C * t
                if failure_prob < np.random.rand():
                    for i, j in enumerate(schedule[:, t]):
                        if j != 0:
                            finish_times[-1] += 100 

        out["F"] = np.array(finish_times).reshape(-1, 1)
        out["G"] = np.vstack(constraints).reshape(-1, len(self.R) * self.T)