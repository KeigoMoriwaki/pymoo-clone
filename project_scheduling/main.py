# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:33:59 2024

@author: k5kei
"""

# main.py

from data import make_1r
from optimization import solve_problem
from plot import plot_schedule

def main():
    problem_data = make_1r()
    result = solve_problem(problem_data)

    print("Optimization result shapes:")
    print(f"result.F.shape: {result.F.shape}")
    print(f"result.X.shape: {result.X.shape}")

    J, P, R, T, p, RUB, C = problem_data

    # result.X を正しい形状に変換
    best_schedule = result.X.reshape((len(J), T))

    plot_schedule(best_schedule, J, R, T)

if __name__ == "__main__":
    main()

