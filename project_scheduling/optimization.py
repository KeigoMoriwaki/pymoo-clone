# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:33:28 2024

@author: k5kei
"""

import numpy as np
import random  # シード管理用に追加
from pymoo.algorithms.soo.nonconvex.ga import GA 
from pymoo.optimize import minimize
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from problem import ResourceConstrainedSchedulingProblem

def solve_problem(problem_data):
    J, p, task_attributes, P, R, robot_types, T, robot_abilities, workspace, workspace_distance, robot_initial_positions, C, RUB = problem_data

    # 問題をインスタンス化
    problem = ResourceConstrainedSchedulingProblem(J, p, task_attributes, P, R, robot_types, T, robot_abilities, workspace, workspace_distance, robot_initial_positions, C, RUB)
    
    # シード管理のための変数を初期化
    initial_seed = 42
    pop_size = 300
    
    # 遺伝的アルゴリズムの設定
    algorithm = GA(
        pop_size=pop_size,
        sampling=IntegerRandomSampling(),
        mutation=PM(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
        crossover=SBX(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
        eliminate_duplicates=True
    )
    
    # 各世代ごとの最小評価値を記録するためのリストを作成
    min_value_over_gens = []

    # 最適化のコールバック関数を定義して世代ごとに最小評価値を記録
    def record_min_value(algorithm):
        nonlocal initial_seed
        F_values = algorithm.pop.get("F")

        # 現在の世代の評価結果を初期シードから10個ずつ区切って評価平均を計算
        num_groups = pop_size // 10
        avg_values_per_seed = []

        for i in range(num_groups):
            # 現在のシードを設定し、そのシードでの個体の評価平均を計算
            current_seed = initial_seed + i
            random.seed(current_seed)
            np.random.seed(current_seed)

            # シードに基づいて10個の個体の平均評価を計算し、リストに追加
            group_values = F_values[i * 10:(i + 1) * 10]
            avg_value = np.mean(group_values)
            avg_values_per_seed.append(avg_value)

        # この世代で最も低い評価平均を求めて記録
        min_avg_value = min(avg_values_per_seed)
        min_value_over_gens.append(min_avg_value)

        # シードを進めて次の世代に使用する
        initial_seed += num_groups
        print(f"New seeds range applied: {initial_seed - num_groups} to {initial_seed - 1}")

    # 最適化を実行し、コールバック関数を利用してデータ収集
    result = minimize(problem, algorithm, ('n_gen', 300), verbose=True, callback=record_min_value)

    return result, min_value_over_gens  # 最適化結果と最小評価値のリストを返す