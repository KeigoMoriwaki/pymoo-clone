# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:32:04 2024

@author: k5kei
"""

import numpy as np
from pymoo.core.problem import Problem

class ResourceConstrainedSchedulingProblem(Problem):
    def __init__(self, J, P, R, T, p, c, a, RUB, locations, tasks, travel_time):
        self.J = J
        self.P = P
        self.R = R
        self.T = T
        self.p = p  # 総作業量
        self.c = c
        self.a = a
        self.RUB = RUB
        self.locations = locations
        self.tasks = tasks
        self.travel_time = travel_time
        self.current_locations = {r: 'A' for r in R}
        n_var = len(J) * T
        super().__init__(n_var=n_var, n_obj=1, n_constr=len(P) + len(R) * T, xl=0, xu=len(R), type_var=int)

    def _evaluate(self, x, out, *args, **kwargs):
        J, P, R, T, p, c, a, RUB, locations, tasks, travel_time = self.J, self.P, self.R, self.T, self.p, self.c, self.a, self.RUB, self.locations, self.tasks, self.travel_time
        
        x = x.reshape((x.shape[0], len(J), T))
        
        total_work = np.array([[np.sum(xi[j] > 0) for j in range(len(J))] for xi in x])
        finish_times = np.ceil(total_work / np.array([p[j+1] for j in range(len(J))])).astype(int)
        
        total_cost = np.array([np.max(finish_times[i]) for i in range(x.shape[0])])
        
        constraints = []
        
        for i in range(x.shape[0]):
            precedence_constraints = [np.sum(x[i, k-1]) - np.sum(x[i, j-1]) for (j, k) in P]
            constraints.append(precedence_constraints)
        
        for t in range(T):
            for r in range(1, len(R) + 1):
                resource_constraints = [np.sum([xi[j, t] == r for j in range(len(J))]) - 1 for xi in x]
                constraints.append(resource_constraints)
        
        constraints = np.hstack(constraints)
        
        for i in range(x.shape[0]):
            for r in range(1, len(R) + 1):
                current_location = 'A'
                for t in range(T):
                    tasks_for_robot = [j for j in range(len(J)) if x[i, j, t] == r]
                    if tasks_for_robot:
                        job = tasks_for_robot[0]
                        new_location = locations[job + 1]
                        travel_time_needed = travel_time[current_location][new_location]
                        if t + travel_time_needed < T:
                            constraints.append(x[i, job, t + travel_time_needed] != r)
                        current_location = new_location

        out["F"] = total_cost
        out["G"] = constraints
