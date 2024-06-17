# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:32:04 2024

@author: k5kei
"""

import numpy as np
from pymoo.core.problem import Problem

class ResourceConstrainedSchedulingProblem(Problem):

    def __init__(self, J, P, R, T, p, c, a, RUB, locations, tasks, travel_time, robot_initial_locations):
        self.J = J
        self.P = P
        self.R = R
        self.T = T
        self.p = p
        self.c = c
        self.a = a
        self.RUB = RUB
        self.locations = locations
        self.tasks = tasks
        self.travel_time = travel_time
        self.robot_initial_locations = robot_initial_locations
        n_var = len(J) * T
        super().__init__(n_var=n_var,
                         n_obj=1,
                         n_constr=len(P) + len(R) * T,
                         xl=0,
                         xu=len(R),
                         type_var=int)
        
    def _calculate_constraints(self):
        num_precedence_constraints = len(self.P)
        num_resource_constraints = len(self.R) * self.T
        num_travel_constraints = len(self.R) * (self.T - 1) * len(self.J) * (len(self.J) - 1)

        total_constraints = num_precedence_constraints + num_resource_constraints + num_travel_constraints
        print(f"Total constraints calculated: {total_constraints}")
        return total_constraints

    def _evaluate(self, x, out, *args, **kwargs):
        J, P, R, T, p, c, a, RUB, locations, tasks, travel_time, robot_initial_locations = self.J, self.P, self.R, self.T, self.p, self.c, self.a, self.RUB, self.locations, self.tasks, self.travel_time, self.robot_initial_locations
        
        x = x.reshape((x.shape[0], len(J), T))
        
        total_work = np.array([[np.sum(xi[j] > 0) for j in range(len(J))] for xi in x])
        finish_times = np.ceil(total_work / np.array([p[j+1] for j in range(len(J))])).astype(int)
        
        total_cost = np.array([np.max(finish_times[i]) for i in range(x.shape[0])])
        
        constraints = []
        
        #for i in range(x.shape[0]):
            #precedence_constraints = [np.sum(x[i, k-1]) - np.sum(x[i, j-1]) for (j, k) in P]
                                        #np.sum(x[i, k-1]) - np.sum(x[i, j-1])
            #constraints.append(precedence_constraints)
        
        #for t in range(T):
            #for r in range(1, len(R) + 1):
                #resource_constraints = [np.sum([xi[j, t] == r for j in range(len(J))]) - 1 for xi in x]
                                        #np.sum([x[i, j, t] == r for j in range(len(J))]) - 1
                #constraints.append(resource_constraints)
        
        
        # 何か行動が終わる前に追加で行動を行わないようにする制約
        precedence_constraints = []
        for i in range(x.shape[0]):
            for (j, k) in P:
                precedence_constraints.append(np.sum(x[i, k-1]) - np.sum(x[i, j-1]))
        print(f"Precedence constraints: {len(precedence_constraints)}")
        constraints.extend(precedence_constraints)
        
        resource_constraints = []
        for i in range(x.shape[0]):
            for t in range(T):
                for r in range(1, len(R) + 1):
                    resource_constraints.append(np.sum([x[i, j, t] == r for j in range(len(J))]) - 1)
        print(f"Resource constraints: {len(resource_constraints)}")
        constraints.extend(resource_constraints)
        
        # ロボットの移動時間を考慮した制約を追加
        travel_constraints = []
        for i in range(x.shape[0]):  # 各サンプルについて
            for t in range(T):
                for r in range(1, len(R) + 1):
                    for j in range(len(J)):
                        if x[i, j, t] == r:
                            previous_location = robot_initial_locations[r]
                            current_location = locations[j]
                            travel_duration = travel_time[previous_location][current_location]
                            if t + travel_duration < T:
                                constraints = np.append(constraints, x[i, j, t + travel_duration] != r)
        print(f"Travel constraints: {len(travel_constraints)}")
        constraints.extend(travel_constraints)
        
        
        constraints = np.hstack(constraints)
        
        out["F"] = total_cost
        out["G"] = constraints



        # 制約の長さを確認
        print(f"Expected constraints: {self.n_constr * x.shape[0]}")
        print(f"Actual constraints: {out['G'].shape[0]}")
        if out["G"].shape[0] != self.n_constr * x.shape[0]:
            raise ValueError(f"Number of constraints does not match: expected {self.n_constr * x.shape[0]}, got {out['G'].shape[0]}")
