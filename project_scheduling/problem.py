# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:32:04 2024

@author: k5kei
"""

import numpy as np
from pymoo.core.problem import Problem

class ResourceConstrainedSchedulingProblem(Problem):

    def __init__(self, J, P, R, T, p, c, a, RUB):
        self.J = J
        self.P = P
        self.R = R
        self.T = T
        self.p = p
        self.c = c
        self.a = a
        self.RUB = RUB
        n_var = len(J) * T  # 変数の数はジョブ数×期間数
        super().__init__(n_var=n_var,
                         n_obj=1,
                         n_constr=len(P) + len(R) * T,
                         xl=0,
                         xu=len(R),
                         type_var=int)

    def _evaluate(self, x, out, *args, **kwargs):
        J, P, R, T, p, c, a, RUB = self.J, self.P, self.R, self.T, self.p, self.c, self.a, self.RUB
        
        # xを再整形する。xのサイズは (サンプル数, ジョブ数 * 期間数)
        x = x.reshape((x.shape[0], len(J), T))
        
        # Calculate start times
        start_times = np.array([[np.argmax(xi[j] > 0) for j in range(len(J))] for xi in x])
        
        # Calculate finish times
        finish_times = start_times + np.array([p[j+1] for j in range(len(J))])
        
        # Objective: minimize the weighted maximum finish time
        total_cost = np.array([np.max(finish_times[i]) + 0.1 * np.sum(finish_times[i]) for i in range(x.shape[0])])
        
        # Constraints
        constraints = []
        
        # Precedence constraints
        for i in range(x.shape[0]):  # 各サンプルについて
            precedence_constraints = [start_times[i, k-1] - finish_times[i, j-1] for (j, k) in P]
            constraints.append(precedence_constraints)
        
        # Resource constraints
        for t in range(T):
            for r in range(1, len(R) + 1):
                resource_constraints = [np.sum([xi[j, t] == r for j in range(len(J))]) - 1 for xi in x]
                constraints.append(resource_constraints)
        
        constraints = np.hstack(constraints)
        
        out["F"] = total_cost
        out["G"] = constraints
