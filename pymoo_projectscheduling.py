# -*- coding: utf-8 -*-
"""
Created on Wed May 15 17:34:30 2024

@author: k5kei
"""


import numpy as np
from pymoo.core.problem import Problem
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize

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
                         xu=1,
                         type_var=np.bool_)

    def _evaluate(self, x, out, *args, **kwargs):
        J, P, R, T, p, c, a, RUB = self.J, self.P, self.R, self.T, self.p, self.c, self.a, self.RUB
        
        # xを再整形する。xのサイズは (サンプル数, ジョブ数 * 期間数)
        x = x.reshape((x.shape[0], len(J), T))
        start_times = np.array([[np.argmax(xi[j]) for j in range(len(J))] for xi in x])
        
        # Objective
        total_cost = np.array([np.sum([c.get((j+1, t+1), 0) * xi[j, t] for j in range(len(J)) for t in range(T) if xi[j, t]]) for xi in x])
        
        # Constraints
        constraints = []
        
        # Precedence constraints
        for i in range(x.shape[0]):  # 各サンプルについて
            precedence_constraints = [start_times[i, k-1] - start_times[i, j-1] - p[j] for (j, k) in P]
            constraints.append(precedence_constraints)
        
        # Resource constraints
        for t in range(T):
            for r in R:
                resource_constraints = [np.sum([a.get((j+1, r, t - t_), 0) * xi[j, t_] for j in range(len(J)) for t_ in range(max(t - p[j+1] + 1, 0), min(t + 1, T))]) - RUB.get((r, t+1), 0) for xi in x]
                constraints.append(resource_constraints)
        
        constraints = np.hstack(constraints)
        
        out["F"] = total_cost
        out["G"] = constraints

def make_1r():
    J = [1, 2, 3, 4]
    p = {1: 1, 2: 3, 3: 2, 4: 2}
    P = [(1, 2), (1, 3), (2, 4)]
    R = [1]
    T = 6
    c = {(j, t): 1 * (t - 1 + p[j]) for j in J for t in range(1, T - p[j] + 2)}
    a = {
        (1, 1, 0): 2,
        (2, 1, 0): 2,
        (2, 1, 1): 1,
        (2, 1, 2): 1,
        (3, 1, 0): 1,
        (3, 1, 1): 1,
        (4, 1, 0): 1,
        (4, 1, 1): 2,
    }
    RUB = {(1, t): 2 for t in range(1, T + 1)}
    return (J, P, R, T, p, c, a, RUB)

def make_2r():
    J = [1, 2, 3, 4, 5]
    p = {1: 2, 2: 2, 3: 3, 4: 2, 5: 5}
    P = [(1, 2), (1, 3), (2, 4)]
    R = [1, 2]
    T = 6
    c = {(j, t): 1 * (t - 1 + p[j]) for j in J for t in range(1, T - p[j] + 2)}
    a = {
        (1, 1, 0): 2, (1, 1, 1): 2, (2, 1, 0): 1, (2, 1, 1): 1, (3, 1, 0): 1, (3, 1, 1): 1, (3, 1, 2): 1, 
        (4, 1, 0): 1, (4, 1, 1): 1, (5, 1, 0): 0, (5, 1, 1): 0, (5, 1, 2): 1, (5, 1, 3): 0, (5, 1, 4): 0, 
        (1, 2, 0): 1, (1, 2, 1): 0, (2, 2, 0): 1, (2, 2, 1): 1, (3, 2, 0): 0, (3, 2, 1): 0, (3, 2, 2): 0, 
        (4, 2, 0): 1, (4, 2, 1): 2, (5, 2, 0): 1, (5, 2, 1): 2, (5, 2, 2): 1, (5, 2, 3): 1, (5, 2, 4): 1
    }
    RUB = {(r, t): 2 for r in R for t in range(1, T + 1)}
    return (J, P, R, T, p, c, a, RUB)

# モデル1を作成
J1, P1, R1, T1, p1, c1, a1, RUB1 = make_1r()
problem1 = ResourceConstrainedSchedulingProblem(J1, P1, R1, T1, p1, c1, a1, RUB1)

# モデル2を作成
J2, P2, R2, T2, p2, c2, a2, RUB2 = make_2r()
problem2 = ResourceConstrainedSchedulingProblem(J2, P2, R2, T2, p2, c2, a2, RUB2)

# 遺伝的アルゴリズムを使用してモデル1を解く
algorithm = GA(pop_size=100, eliminate_duplicates=True)
result1 = minimize(problem1, algorithm, ('n_gen', 200), verbose=True)

# 遺伝的アルゴリズムを使用してモデル2を解く
result2 = minimize(problem2, algorithm, ('n_gen', 200), verbose=True)

# 結果を表示
print("Model 1:")
print('Best solution found: \nX = \n', result1.X)
print('Function value: \nF = \n', result1.F)

print("\nModel 2:")
print('Best solution found: \nX = \n', result2.X)
print('Function value: \nF = \n', result2.F)
