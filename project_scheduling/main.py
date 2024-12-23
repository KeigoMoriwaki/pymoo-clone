
# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:33:59 2024

@author: k5kei
"""

# main.py

import random
import numpy as np
import json
from data import make_1r
from optimization import solve_problem
from optimization import solve_problem2
from simulate import simulate_problem
from simulate import simulate_problem2
from plot import plot_schedule
from plot import plot_schedule2
from plot import plot_value_comparison
from plot import plot_average_value_comparison

def main():
    all_min_values1 = []  # 各シードの評価値推移を保存するリスト
    all_min_values2 = []  # 各シードの評価値推移を保存するリスト
    all_min_values3 = []
    all_min_values4 = []
    seeds = range(60, 70)
    results_stage1 = {"with_failure": [], "without_failure": []}
    results_stage2 = {"failure": [], "no_failure": []}

    # 各シードの評価値リストを保存
    evaluation_values_stage1 = {"with_failure": [], "without_failure": []}
    evaluation_values_stage2 = {"failure": [], "no_failure": []}

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
        results_stage1["with_failure"].append(result1)
        evaluation_values_stage1["with_failure"].append(min_value_over_gens1[-1])  # 最後の評価値を保存
        
        # スケジュールをプロット
        print(f"Plotting schedule for seed {seed}...")
        plot_schedule(result1, J, R, T, robot_types, seed)  # 必要なデータを渡す

        # 故障を考慮しない場合
        result2, min_value_over_gens2 = solve_problem2(problem_data, seed)
        all_min_values2.append(min_value_over_gens2)
        results_stage1["without_failure"].append(result2)
        evaluation_values_stage1["without_failure"].append(min_value_over_gens2[-1])  # 最後の評価値を保存
        
        # スケジュールをプロット
        print(f"Plotting schedule for seed {seed}...")
        plot_schedule2(result2, J, R, T, robot_types, seed)  # 必要なデータを渡す

        # 評価値推移をプロット
        print(f"Plotting value over generations for seed {seed}...")
        plot_value_comparison(min_value_over_gens1, min_value_over_gens2, seed)

        # 故障を考慮する場合（シミュレーション）
        result3, min_value_over_gens3 = simulate_problem(problem_data, seed)
        all_min_values3.append(min_value_over_gens3)
        results_stage2["failure"].append(result3)
        evaluation_values_stage2["failure"].append(min_value_over_gens3[-1])  # 最後の評価値を保存

        # 故障を考慮しない場合（シミュレーション）
        result4, min_value_over_gens4 = simulate_problem2(problem_data, seed)
        all_min_values4.append(min_value_over_gens4)
        results_stage2["no_failure"].append(result4)
        evaluation_values_stage2["no_failure"].append(min_value_over_gens4[-1])  # 最後の評価値を保存

    # 平均評価値の推移をプロット
    print("Plotting average value over generations...")
    plot_average_value_comparison(all_min_values1, all_min_values2)

    # 平均値を計算
    print("Calculating averages...")
    averaged_results_stage1 = {
        "with_failure": np.mean(evaluation_values_stage1["with_failure"]),
        "without_failure": np.mean(evaluation_values_stage1["without_failure"]),
    }
    averaged_results_stage2 = {
        "failure": np.mean(evaluation_values_stage2["failure"]),
        "no_failure": np.mean(evaluation_values_stage2["no_failure"]),
    }

    # 4通りの引き算
    print("Calculating final evaluation values...")
    with_failure_vs_failure = averaged_results_stage1["with_failure"] - averaged_results_stage2["failure"]
    with_failure_vs_no_failure = averaged_results_stage1["with_failure"] - averaged_results_stage2["no_failure"]
    without_failure_vs_failure = averaged_results_stage1["without_failure"] - averaged_results_stage2["failure"]
    without_failure_vs_no_failure = averaged_results_stage1["without_failure"] - averaged_results_stage2["no_failure"]

    # 計算結果をprintで表示
    print(f"with_failure - failure: {with_failure_vs_failure}")
    print(f"with_failure - no_failure: {with_failure_vs_no_failure}")
    print(f"without_failure - failure: {without_failure_vs_failure}")
    print(f"without_failure - no_failure: {without_failure_vs_no_failure}")

    final_evaluation_values = {
        "with_failure - failure": with_failure_vs_failure,
        "with_failure - no_failure": with_failure_vs_no_failure,
        "without_failure - failure": without_failure_vs_failure,
        "without_failure - no_failure": without_failure_vs_no_failure,
    }

    # 結果をテキストファイルに保存
    print("Saving results to text file...")
    results_to_save = {
        "averaged_results_stage1": averaged_results_stage1,
        "averaged_results_stage2": averaged_results_stage2,
        "final_evaluation_values": final_evaluation_values,
    }

    with open("optimization_results.txt", "w") as f:
        f.write(json.dumps(results_to_save, indent=4))

    print("Results saved successfully.")

if __name__ == "__main__":
    main()