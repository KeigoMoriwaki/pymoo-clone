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
    J, p, task_attributes, P, R, robot_types, T, robot_capacities, workspace, workspace_distance, C, RUB = problem_data
    
    problem = ResourceConstrainedSchedulingProblem(J, p, task_attributes, P, R, robot_types, T, robot_capacities, workspace, workspace_distance, C, RUB)
    algorithm = GA(pop_size=500,
                   sampling=IntegerRandomSampling(),
                   mutation=PM(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
                   crossover=SBX(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
                   eliminate_duplicates=True)
    result = minimize(problem, algorithm, ('n_gen', 300), verbose=True)

    return result