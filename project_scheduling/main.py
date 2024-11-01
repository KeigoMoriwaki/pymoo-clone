
# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:33:59 2024

@author: k5kei
"""

# main.py

from data import make_1r
from optimization import solve_problem
from plot import plot_schedule, plot_fitness_over_generations

def main():
    # 問題のデータを取得
    problem_data = make_1r()
    J, p, task_attributes, P, R, robot_types, T, robot_abilities, workspace, workspace_distance, robot_initial_positions, C, RUB = problem_data
    
    # 問題の解決と評価値の遷移データを取得
    result, min_fitness_over_gens = solve_problem(problem_data)
    
    # スケジュールをプロット
    plot_schedule(result, J, R, T, robot_types)
    
    # 評価値の遷移をプロット
    plot_fitness_over_generations(min_fitness_over_gens)

if __name__ == "__main__":
    main()