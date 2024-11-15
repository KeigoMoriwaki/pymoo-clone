
# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:33:59 2024

@author: k5kei
"""

# main.py

import random
import numpy as np
from data import make_1r
from optimization import solve_problem
from plot import plot_schedule, plot_value_over_generations

def main(seed = None):
    # シード値が指定されていれば設定
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    # 問題のデータを取得
    problem_data = make_1r()
    J, p, task_attributes, P, R, robot_types, T, robot_abilities, workspace, workspace_distance, moving_cost, robot_initial_positions, C, RUB = problem_data
    
    # 問題の解決と評価値の遷移データを取得
    result, min_value_over_gens = solve_problem(problem_data, seed)
    
    # スケジュールをプロット
    plot_schedule(result, J, R, T, robot_types)
    
    # 評価値の遷移をプロット
    plot_value_over_generations(min_value_over_gens)

if __name__ == "__main__":
    main(seed = 42)