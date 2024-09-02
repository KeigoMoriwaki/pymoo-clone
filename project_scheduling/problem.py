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
        # Make sure R is a list and T is an integer
        #print(f"Type of R: {type(R)}, Value of R: {R}")
        #print(f"Type of T: {type(T)}, Value of T: {T}")
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
                         xl=0,
                         xu=len(R),
                         type_var=int)

    def _evaluate(self, x, out, *args, **kwargs):
        J, p, P, R, T, C, RUB = self.J, self.p, self.P, self.R, self.T, self.C, self.RUB
        
        x = x.reshape((x.shape[0], len(J), T))

        total_work = np.array([[np.sum(xi[j] > 0) for j in range(len(J))] for xi in x])
        finish_times = np.ceil(total_work / np.array([p[j+1] for j in range(len(J))])).astype(int)

        total_cost = np.array([np.max(finish_times[i]) for i in range(x.shape[0])])

        constraints = []


        for i in range(x.shape[0]):
            for t in range(T):
                for j in range(len(J)):
                    robot = int(x[i, j, t])
                    if robot > 0:
                        success_prob = (1 - C) ** t
                        #print(f"Robot {robot} at time {t}, success_prob: {success_prob}")
                        if np.random.random() > success_prob:
                            x[i, j, t] = (1 - C)  
                            #print(f"Task {j} at time {t} failed. New value: {x[i, j, t]}")
                        else:
                            x[i, j, t] = 1  

            precedence_constraints = [np.sum(x[i, k-1]) - np.sum(x[i, j-1]) for (j, k) in P]
            constraints.append(precedence_constraints)

        for t in range(T):
            for r in range(1, len(R) + 1):
                resource_constraints = [np.sum([xi[j, t] == r for j in range(len(J))]) - 1 for xi in x]
                constraints.append(resource_constraints)

        constraints = np.hstack(constraints)

        out["F"] = total_cost
        out["G"] = constraints
