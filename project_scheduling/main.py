# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:33:59 2024

@author: k5kei
"""

from data import make_1r
from optimization import solve_problem
from plot import plot_schedule

def main():
    problem_data = make_1r()
    result = solve_problem(problem_data)

    print(result.F)
    print(result.X)
    
    J, P, R, T, p, RUB, C = problem_data
    plot_schedule(result, J, R, T, C)

if __name__ == "__main__":
    main()
