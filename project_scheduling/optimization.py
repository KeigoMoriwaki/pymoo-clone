# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:33:28 2024

@author: k5kei
"""

from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.ux import UniformCrossover
from pymoo.operators.mutation.rm import ChoiceRandomMutation
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from problem import ResourceConstrainedSchedulingProblem

def solve_problem(problem_data):
    problem = ResourceConstrainedSchedulingProblem(problem_data)

    algorithm = GA(pop_size=100,
                   sampling=IntegerRandomSampling(),
                   mutation=PM(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
                   crossover=SBX(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
                   eliminate_duplicates=True)

    result = minimize(problem, algorithm, ('n_gen', 100), seed=1, verbose=True)

    return result