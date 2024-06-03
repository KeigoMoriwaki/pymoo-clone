# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:33:28 2024

@author: k5kei
"""

from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize

def solve_problem(problem):
    algorithm = GA(pop_size=200)
    res = minimize(problem, algorithm, ('n_gen', 200), verbose=True)
    return res
