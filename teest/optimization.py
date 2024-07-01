# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 20:00:09 2024

@author: k5kei
"""

from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize
from problem import SchedulingProblem

def optimize_schedule(jobs, robots, distances):
    problem = SchedulingProblem(jobs, robots, distances)
    algorithm = GA(pop_size=100)
    result = minimize(problem, algorithm, seed=1, verbose=True)
    return result.X
