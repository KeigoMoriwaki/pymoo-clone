# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 15:39:52 2024

@author: k5kei
"""

from pymoo.algorithms.soo.nonconvex.ga import GA 
from pymoo.optimize import minimize
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from simulate_failure import ResourceConstrainedSchedulingProblem3
from simulate_no_failure import ResourceConstrainedSchedulingProblem4
import numpy as np
import random

def simulate_problem(problem_data, seed = None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    robot_types, robot_initial_positions, J, p, task_attributes, P, R, T, robot_abilities, workspace, workspace_distance, moving_cost, C, RUB = problem_data

    # 問題をインスタンス化
    problem = ResourceConstrainedSchedulingProblem3(robot_types, robot_initial_positions, J, p, task_attributes, P, R, T, robot_abilities, workspace, workspace_distance, moving_cost, C, RUB)

    # 遺伝的アルゴリズムの設定
    algorithm = GA(
        pop_size=300,
        sampling=IntegerRandomSampling(),
        mutation=PM(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
        crossover=SBX(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
        eliminate_duplicates=True
    )

    # 各世代ごとの最小評価値を記録するためのリストを作成
    min_value_over_gens3 = []

    # 最適化のコールバック関数を定義して世代ごとに最小評価値を記録
    def record_min_value(algorithm):
        gen_min_value = algorithm.pop.get("F").min()  # 現在の世代の最小評価値を取得
        min_value_over_gens3.append(gen_min_value)    # リストに追加

    # 最適化を実行し、コールバック関数を利用してデータ収集
    result3 = minimize(problem, algorithm, ('n_gen', 300), verbose=True, callback=record_min_value)

    return result3, min_value_over_gens3  # 最適化結果と最小評価値のリストを返す

def simulate_problem2(problem_data, seed = None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    robot_types, robot_initial_positions, J, p, task_attributes, P, R, T, robot_abilities, workspace, workspace_distance, moving_cost, C, RUB = problem_data

    # 問題をインスタンス化
    problem = ResourceConstrainedSchedulingProblem4(robot_types, robot_initial_positions, J, p, task_attributes, P, R, T, robot_abilities, workspace, workspace_distance, moving_cost, C, RUB)

    # 遺伝的アルゴリズムの設定
    algorithm = GA(
        pop_size=300,
        sampling=IntegerRandomSampling(),
        mutation=PM(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
        crossover=SBX(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
        eliminate_duplicates=True
    )

    # 各世代ごとの最小評価値を記録するためのリストを作成
    min_value_over_gens4 = []

    # 最適化のコールバック関数を定義して世代ごとに最小評価値を記録
    def record_min_value(algorithm):
        gen_min_value = algorithm.pop.get("F").min()  # 現在の世代の最小評価値を取得
        min_value_over_gens4.append(gen_min_value)    # リストに追加

    # 最適化を実行し、コールバック関数を利用してデータ収集
    result4 = minimize(problem, algorithm, ('n_gen', 300), verbose=True, callback=record_min_value)

    return result4, min_value_over_gens4  # 最適化結果と最小評価値のリストを返す
