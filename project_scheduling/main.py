
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
from plot import plot_schedule, plot_value_over_generations, plot_average_value_over_generations


def main():
    seeds = range(42, 52)  # シード値 42～51
    all_min_values = []  # 各シードの評価値推移を保存するリスト
    
    for seed in seeds:
        print(f"Running optimization for seed {seed}...")
        
        # シード値を設定
        random.seed(seed)
        np.random.seed(seed)
        
        # 問題のデータを取得
        problem_data = make_1r()
        J, p, task_attributes, P, R, robot_types, T, robot_abilities, workspace, workspace_distance, moving_cost, robot_initial_positions, C, RUB = problem_data
        
        # 最適化を実行し、結果と評価値推移を取得
        result, min_value_over_gens = solve_problem(problem_data, seed)
        all_min_values.append(min_value_over_gens)
        
        # スケジュールをプロット
        print(f"Plotting schedule for seed {seed}...")
        plot_schedule(result, J, R, T, robot_types)  # 必要なデータを渡す
        
        # 評価値推移をプロット
        print(f"Plotting value over generations for seed {seed}...")
        plot_value_over_generations(min_value_over_gens, seed)
    
    # 平均評価値の推移をプロット
    print("Plotting average value over generations...")
    plot_average_value_over_generations(all_min_values)

if __name__ == "__main__":
    main()