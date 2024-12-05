
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
from optimization import solve_problem2
from optimization import simulate_schedule1
from optimization import simulate_schedule2
from plot import plot_schedule, plot_value_over_generations, plot_average_value_over_generations
from plot import plot_schedule2, plot_value_over_generations2, plot_average_value_over_generations2

def main():
    all_min_values1 = []  # 各シードの評価値推移を保存するリスト
    all_min_values2 = []  # 各シードの評価値推移を保存するリスト
    seeds = range(42, 52)
    results_stage1 = {"with_failure": [], "without_failure": []}
    evaluation_values = {"with_failure": {"failure": [], "no_failure": []},
                         "without_failure": {"failure": [], "no_failure": []}}

    # 各シードの最小評価値を保存するリスト
    stage1_min_values = {"with_failure": [], "without_failure": []}

    for seed in seeds:
        print(f"Running first stage optimization for seed {seed}...")
        random.seed(seed)
        np.random.seed(seed)

        # データの準備
        problem_data = make_1r()
        robot_types, robot_initial_positions, J, p, task_attributes, P, R, T, robot_abilities, workspace, workspace_distance, moving_cost, C, RUB = problem_data

        # 故障を考慮する場合
        result1, min_value_over_gens1 = solve_problem(problem_data, seed)
        all_min_values1.append(min_value_over_gens1)
        stage1_min_values["with_failure"].append(min(min_value_over_gens1))
        results_stage1["with_failure"].append(result1)
        
        # スケジュールをプロット
        print(f"Plotting schedule for seed {seed}...")
        plot_schedule(result1, J, R, T, robot_types)  # 必要なデータを渡す

        # 評価値推移をプロット
        print(f"Plotting value over generations for seed {seed}...")
        plot_value_over_generations(min_value_over_gens1, seed)

        # 故障を考慮しない場合
        result2, min_value_over_gens2 = solve_problem2(problem_data, seed)
        all_min_values2.append(min_value_over_gens2)
        stage1_min_values["without_failure"].append(min(min_value_over_gens2))
        results_stage1["without_failure"].append(result2)
        
        # スケジュールをプロット
        print(f"Plotting schedule for seed {seed}...")
        plot_schedule2(result2, J, R, T, robot_types)  # 必要なデータを渡す

        # 評価値推移をプロット
        print(f"Plotting value over generations for seed {seed}...")
        plot_value_over_generations2(min_value_over_gens2, seed)

        # 2段階目の評価
        for mode, result in [("with_failure", result1), ("without_failure", result2)]:
            print(f"Simulating {mode} schedule with failure...")
            evaluation_with_failure = simulate_schedule1(result, problem_data, consider_failures=True)
            evaluation_values[mode]["failure"].append(evaluation_with_failure)

            print(f"Simulating {mode} schedule without failure...")
            evaluation_without_failure = simulate_schedule2(result, problem_data, consider_failures=False)
            evaluation_values[mode]["no_failure"].append(evaluation_without_failure)

    # 平均評価値の推移をプロット
    print("Plotting average value over generations...")
    plot_average_value_over_generations(all_min_values1)
    
    # 平均評価値の推移をプロット
    print("Plotting average value over generations...")
    plot_average_value_over_generations2(all_min_values2)

    # 平均値の計算
    avg_stage1_min_values = {
        mode: np.mean(stage1_min_values[mode]) for mode in ["with_failure", "without_failure"]
    }
    avg_simulation_values = {
        mode: {
            "failure": np.mean(evaluation_values[mode]["failure"]),
            "no_failure": np.mean(evaluation_values[mode]["no_failure"]),
        } for mode in ["with_failure", "without_failure"]
    }

    # 結果の出力
    for mode in ["with_failure", "without_failure"]:
        print(f"\nFinal evaluation values for {mode}:")
        failure_diff = avg_stage1_min_values[mode] - avg_simulation_values[mode]["failure"]
        print(f"{mode} - failure: Evaluation Value = {failure_diff}")
        no_failure_diff = avg_stage1_min_values[mode] - avg_simulation_values[mode]["no_failure"]
        print(f"{mode} - no_failure: Evaluation Value = {no_failure_diff}")
    
    # avg_stage1_min_values の出力
    print("\nAverage stage1 minimum values:")
    for mode, value in avg_stage1_min_values.items():
        print(f"{mode}: {value}")
    
    # avg_simulation_values の出力
    print("\nAverage simulation values:")
    for mode, sim_values in avg_simulation_values.items():
        print(f"{mode}:")
        for failure_mode, avg_value in sim_values.items():
            print(f"  {failure_mode}: {avg_value}")

if __name__ == "__main__":
    main()
