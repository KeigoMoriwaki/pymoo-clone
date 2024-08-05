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
                         n_constr=2,  # 2つの制約に対応
                         xl=0,
                         xu=len(self.R),
                         type_var=int)

    def _evaluate(self, x, out, *args, **kwargs):
        finish_times = []
        resource_constraints_list = []
        order_constraints_list = []

        for ind in x:
            schedule = ind.reshape((len(self.J), self.T))
            leftover = copy.deepcopy(self.p)
            resource_constraints = 0
            order_constraints = 0
            t = 0
            for t in range(self.T):
                n_worker = np.zeros(len(self.R))
                for j in range(len(self.J)):
                    robot = schedule[j, t]
                    if robot != 0:
                        failure_probability = 1 - self.C * t
                        if np.random.rand() <= failure_probability:
                            if n_worker[robot-1] > 0:
                                resource_constraints += 1
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

            # 順序制約のチェック
            for (pred, succ) in self.P:
                pred_finish_time = np.where(schedule[self.J.index(pred), :] > 0)[0]
                succ_start_time = np.where(schedule[self.J.index(succ), :] > 0)[0]
                
                if len(pred_finish_time) > 0 and len(succ_start_time) > 0:
                    pred_finish_time = pred_finish_time[-1] + 1
                    succ_start_time = succ_start_time[0]
                    if pred_finish_time > succ_start_time:
                        order_constraints += 1

            resource_constraints_list.append(resource_constraints)
            order_constraints_list.append(order_constraints)

        out["F"] = np.array(finish_times).reshape(-1, 1)
        out["G"] = np.hstack((np.array(resource_constraints_list).reshape(-1, 1),
                              np.array(order_constraints_list).reshape(-1, 1)))
