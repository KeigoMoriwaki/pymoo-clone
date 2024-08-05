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
                         xl=0,
                         xu=len(self.R),
                         type_var=int)

    def _evaluate(self, x, out, *args, **kwargs):
        num_samples = len(x)
        finish_times = []
        constraints = []

        for ind in x:
            ind = np.array(ind).reshape((len(self.J), self.T))
            schedule = ind
            leftover = copy.deepcopy(self.p)
            resource_constraints = 0
            precedence_constraints = 0
            task_constraints = 0

            failed = np.zeros((len(self.J), self.T))

            for t in range(self.T):
                n_worker = np.zeros(len(self.R))
                for j in range(len(self.J)):
                    robot = schedule[j, t]
                    if robot != 0:
                        failure_probability = 1 - self.C * t
                        if np.random.rand() > failure_probability:
                            failed[j, t] = 1
                        else:
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

            task_finish_time = {}
            for j in range(len(self.J)):
                for t in range(self.T):
                    if schedule[j, t] != 0 and failed[j, t] == 0:
                        task_finish_time[self.J[j]] = t + 1

            for (x, y) in self.P:
                if task_finish_time.get(x, 0) >= task_finish_time.get(y, self.T + 1):
                    precedence_constraints += 1

            for j in range(len(self.J)):
                total_work = 0
                for t in range(self.T):
                    if schedule[j, t] != 0 and failed[j, t] == 0:
                        total_work += 1
                if total_work != self.p[self.J[j]]:
                    task_constraints += 1

            constraints.append([resource_constraints, precedence_constraints, task_constraints])

        constraints = np.array(constraints)
        num_constraints = constraints.shape[1]
        if num_constraints != self.n_constr:
            raise ValueError(f"Expected {self.n_constr} constraints but got {num_constraints}. Constraints: {constraints}")

        out["F"] = np.array(finish_times).reshape(-1, 1)
        out["G"] = constraints.reshape(num_samples, self.n_constr)