# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:33:59 2024

@author: k5kei
"""

from data import make_1r, make_2r
from optimization import solve_problem
from plot import plot_schedule

def main():
    # Solve first problem instance
    problem_data = make_1r()
    result = solve_problem(problem_data)
    J, P, R, T, p, c, a, RUB, locations, tasks, travel_time, robot_initial_locations = problem_data
    plot_schedule(result, J, R, T, p, c, a, RUB, locations, tasks, travel_time)

    # Solve second problem instance
    problem_data = make_2r()
    result = solve_problem(problem_data)
    J, P, R, T, p, c, a, RUB, locations, tasks, travel_time, robot_initial_locations = problem_data
    plot_schedule(result, J, R, T, p, c, a, RUB, locations, tasks, travel_time)

if __name__ == "__main__":
    main()
