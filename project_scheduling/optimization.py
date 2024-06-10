# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:33:28 2024

@author: k5kei
"""

from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize
from problem import ResourceConstrainedSchedulingProblem
from data import make_1r, make_2r

def solve_problem(problem_data):
    J, P, R, T, p, c, a, RUB, locations, tasks, travel_time = problem_data
    problem = ResourceConstrainedSchedulingProblem(J, P, R, T, p, c, a, RUB, locations, tasks, travel_time)
    
    algorithm = GA(pop_size=100, eliminate_duplicates=True)
    result = minimize(problem, algorithm, ('n_gen', 200), verbose=True)
    
    return result
