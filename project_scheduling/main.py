# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:33:59 2024

@author: k5kei
"""

from problem import ResourceConstrainedSchedulingProblem
from data import make_1r, make_2r
from optimization import solve_problem

def main():
    # モデル1を作成
    J1, P1, R1, T1, p1, c1, a1, RUB1 = make_1r()
    problem1 = ResourceConstrainedSchedulingProblem(J1, P1, R1, T1, p1, c1, a1, RUB1)

    # モデル2を作成
    J2, P2, R2, T2, p2, c2, a2, RUB2 = make_2r()
    problem2 = ResourceConstrainedSchedulingProblem(J2, P2, R2, T2, p2, c2, a2, RUB2)

    # 遺伝的アルゴリズムを使用してモデル1を解く
    result1 = solve_problem(problem1)

    # 遺伝的アルゴリズムを使用してモデル2を解く
    result2 = solve_problem(problem2)

    # 結果を表示
    print("Model 1:")
    print('Best solution found: \nX = \n', result1.X)
    print('Function value: \nF = \n', result1.F)

    print("\nModel 2:")
    print('Best solution found: \nX = \n', result2.X)
    print('Function value: \nF = \n', result2.F)

if __name__ == "__main__":
    main()
