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
        n_constr = self._calculate_constraints()
        super().__init__(n_var=n_var, n_obj=1, n_constr=n_constr, xl=0, xu=len(R), type_var=int)

    def _calculate_constraints(self):
        num_precedence_constraints = len(self.P)
        num_resource_constraints = len(self.R) * self.T
        num_assignment_constraints = len(self.J) * self.T
        num_travel_constraints = len(self.R) * (self.T - 1) * len(self.J) * (len(self.J) - 1)

        total_constraints = num_precedence_constraints + num_resource_constraints + num_assignment_constraints + num_travel_constraints
        print(f"Total constraints calculated: {total_constraints}")
        return total_constraints

    def _evaluate(self, x, out, *args, **kwargs):
        J, P, R, T, p, c, a, RUB, locations, tasks, travel_time, robot_initial_locations = self.J, self.P, self.R, self.T, self.p, self.c, self.a, self.RUB, self.locations, self.tasks, self.travel_time, self.robot_initial_locations
        x = x.reshape((x.shape[0], len(J), T))

        total_work = np.array([[np.sum(xi[j] > 0) for j in range(len(J))] for xi in x])
        finish_times = np.ceil(total_work / np.array([p[j+1] for j in range(len(J))])).astype(int)

        total_cost = np.array([np.max(finish_times[i]) for i in range(x.shape[0])])

        constraints = []

        # 先行制約の追加
        precedence_constraints = []
        for i in range(x.shape[0]):
            for (j, k) in P:
                precedence_constraints.append(np.sum(x[i, k-1]) - np.sum(x[i, j-1]))
        print(f"Precedence constraints: {len(precedence_constraints)}")
        constraints.extend(precedence_constraints)

        # 資源制約の追加
        resource_constraints = []
        for i in range(x.shape[0]):
            for t in range(T):
                for r in range(1, len(R) + 1):
                    resource_constraints.append(np.sum([x[i, j, t] == r for j in range(len(J))]) - 1)
        print(f"Resource constraints: {len(resource_constraints)}")
        constraints.extend(resource_constraints)


        # 同じジョブが同じ時間に複数のロボットに割り当てられないようにする制約
        assignment_constraints = []
        for i in range(x.shape[0]):
            for j in range(len(J)):
                for t in range(T):
                    if x[i, j, t] > 0:
                        assignment_constraints.append(np.sum(x[i, j, :] == x[i, j, t]) <= 1)
        print(f"Assignment constraints: {len(assignment_constraints)}")
        constraints.extend(assignment_constraints)

        # ロボットの移動時間を考慮した制約の追加
        travel_constraints = []
        for i in range(x.shape[0]):
            for t in range(T-1):
                for r in range(1, len(R) + 1):
                    for j in range(len(J)):
                        if x[i, j, t] == r:
                            current_location = locations[j]
                            for k in range(len(J)):
                                if j != k and x[i, k, t+1] == r:
                                    next_location = locations[k]
                                    travel_duration = travel_time[current_location][next_location]
                                    if t + travel_duration < T:
                                        travel_constraints.append(x[i, k, t + travel_duration] != r)
        print(f"Travel constraints: {len(travel_constraints)}")
        constraints.extend(travel_constraints)

        # 制約を平坦化し、`out["G"]`に設定
        out["F"] = total_cost
        out["G"] = np.hstack(constraints).flatten()

        # 制約の長さを確認
        print(f"Expected constraints: {self.n_constr * x.shape[0]}")
        print(f"Actual constraints: {out['G'].shape[0]}")
        if out["G"].shape[0] != self.n_constr * x.shape[0]:
            raise ValueError(f"Number of constraints does not match: expected {self.n_constr * x.shape[0]}, got {out['G'].shape[0]}")
