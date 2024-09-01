# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:33:28 2024

@author: k5kei
"""

from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from problem import ResourceConstrainedSchedulingProblem

def solve_problem(problem_data):
    J, P, R, T, p, c, RUB = problem_data
    problem = ResourceConstrainedSchedulingProblem(J, P, R, T, p, c, RUB)
    algorithm = GA(pop_size=300,
                   sampling=IntegerRandomSampling(),
                   mutation=PM(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
                   crossover=SBX(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
                   eliminate_duplicates=True)
    result = minimize(problem, algorithm, ('n_gen', 300), verbose=True)

    return result