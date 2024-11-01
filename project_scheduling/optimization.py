# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:33:28 2024

@author: k5kei
"""

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
    
    # 遺伝的アルゴリズムの設定
    algorithm = GA(
        pop_size=300,
        sampling=IntegerRandomSampling(),
        mutation=PM(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
        crossover=SBX(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
        eliminate_duplicates=True
    )
    
    # 各世代ごとの最小評価値を記録するためのリストを作成
    min_fitness_over_gens = []

    # 最適化のコールバック関数を定義して世代ごとに最小評価値を記録
    def record_min_fitness(algorithm):
        gen_min_fitness = algorithm.pop.get("F").min()  # 現在の世代の最小評価値を取得
        min_fitness_over_gens.append(gen_min_fitness)    # リストに追加

    # 最適化を実行し、コールバック関数を利用してデータ収集
    result = minimize(problem, algorithm, ('n_gen', 300), verbose=True, callback=record_min_fitness)

    return result, min_fitness_over_gens  # 最適化結果と最小評価値のリストを返す