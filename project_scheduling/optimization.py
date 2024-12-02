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
from problem2 import ResourceConstrainedSchedulingProblem2
import numpy as np
import random

def solve_problem(problem_data, seed = None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    robot_types, robot_initial_positions, J, p, task_attributes, P, R, T, robot_abilities, workspace, workspace_distance, moving_cost, C, RUB = problem_data

    # 問題をインスタンス化
    problem = ResourceConstrainedSchedulingProblem(robot_types, robot_initial_positions, J, p, task_attributes, P, R, T, robot_abilities, workspace, workspace_distance, moving_cost, C, RUB)

    # 遺伝的アルゴリズムの設定
    algorithm = GA(
        pop_size=300,
        sampling=IntegerRandomSampling(),
        mutation=PM(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
        crossover=SBX(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
        eliminate_duplicates=True
    )

    # 各世代ごとの最小評価値を記録するためのリストを作成
    min_value_over_gens = []

    # 最適化のコールバック関数を定義して世代ごとに最小評価値を記録
    def record_min_value(algorithm):
        gen_min_value = algorithm.pop.get("F").min()  # 現在の世代の最小評価値を取得
        min_value_over_gens.append(gen_min_value)    # リストに追加

    # 最適化を実行し、コールバック関数を利用してデータ収集
    result1 = minimize(problem, algorithm, ('n_gen', 300), verbose=True, callback=record_min_value)

    return result1, min_value_over_gens  # 最適化結果と最小評価値のリストを返す

def solve_problem2(problem_data, seed = None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    robot_types, robot_initial_positions, J, p, task_attributes, P, R, T, robot_abilities, workspace, workspace_distance, moving_cost, C, RUB = problem_data

    # 問題をインスタンス化
    problem = ResourceConstrainedSchedulingProblem2(robot_types, robot_initial_positions, J, p, task_attributes, P, R, T, robot_abilities, workspace, workspace_distance, moving_cost, C, RUB)

    # 遺伝的アルゴリズムの設定
    algorithm = GA(
        pop_size=300,
        sampling=IntegerRandomSampling(),
        mutation=PM(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
        crossover=SBX(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
        eliminate_duplicates=True
    )

    # 各世代ごとの最小評価値を記録するためのリストを作成
    min_value_over_gens = []

    # 最適化のコールバック関数を定義して世代ごとに最小評価値を記録
    def record_min_value(algorithm):
        gen_min_value = algorithm.pop.get("F").min()  # 現在の世代の最小評価値を取得
        min_value_over_gens.append(gen_min_value)    # リストに追加

    # 最適化を実行し、コールバック関数を利用してデータ収集
    result2 = minimize(problem, algorithm, ('n_gen', 300), verbose=True, callback=record_min_value)

    return result2, min_value_over_gens  # 最適化結果と最小評価値のリストを返す

def simulate_schedule1(result, problem_data, consider_failures=True):
    robot_types, robot_initial_positions, J, p, task_attributes, P, R, T, robot_abilities, workspace, workspace_distance, moving_cost, C, RUB = problem_data

    # スケジュールを取得
    schedule = result.X.reshape((len(R), T))

    # 故障を考慮する場合の設定
    seed = 42  # シミュレーション用の固定シード
    rng = np.random.default_rng(seed)

    workload = np.zeros(len(J))
    task_completed = np.zeros(len(J))
    task_completion_time = np.full(len(J), -1)
    current_workspace = {r: robot_initial_positions[r + 1] for r in range(len(R))}

    for t in range(T):
        for r in range(len(R)):
            task = int(schedule[r, t])
            if task > 0:
                task_attr = task_attributes[task]
                robot_type = problem_data[0][r + 1]  # ロボットタイプ
                work = robot_abilities[robot_type][task_attr]
                task_workspace = workspace[task]

                # 移動コスト考慮
                if current_workspace[r] != task_workspace:
                    cost = moving_cost[current_workspace[r]][task_workspace]
                    work = work * (1 - cost / robot_abilities[robot_type]['move'])
                    current_workspace[r] = task_workspace

                # 故障の確率を適用
                if consider_failures and rng.random() > 1 - C:
                    continue  # このステップは無効化

                workload[task - 1] += work

                # タスク完了判定
                if workload[task - 1] >= p[task]:
                    task_completed[task - 1] = 1
                    if task_completion_time[task - 1] == -1:
                        task_completion_time[task - 1] = t + 1

    # 評価値の計算
    evaluation_value = 0
    if np.all(task_completed):
        evaluation_value = np.max(task_completion_time)
        print(f"All tasks completed by evaluation_value {evaluation_value}")
    else:
        # 未完了タスクがある場合は、まずTを加算する
        evaluation_value += T
        print(f"Some tasks are incomplete. Base evaluation value: {evaluation_value}")

        # 残りの仕事量を合算する
        for j in range(len(J)):
            if task_completed[j] == 0:
                remaining_workload = p[J[j]] - workload[j]
                evaluation_value += remaining_workload   # 残り仕事量のみを追加
                print(f"Task {J[j]} is incomplete. Remaining workload: {remaining_workload}. Total evaluation value now: {evaluation_value}")
                
    return evaluation_value

def simulate_schedule2(result, problem_data, consider_failures=False):
    robot_types, robot_initial_positions, J, p, task_attributes, P, R, T, robot_abilities, workspace, workspace_distance, moving_cost, C, RUB = problem_data

    # スケジュールを取得
    schedule = result.X.reshape((len(R), T))

    # 故障を考慮する場合の設定
    seed = 42  # シミュレーション用の固定シード
    rng = np.random.default_rng(seed)

    workload = np.zeros(len(J))
    task_completed = np.zeros(len(J))
    task_completion_time = np.full(len(J), -1)
    current_workspace = {r: robot_initial_positions[r + 1] for r in range(len(R))}

    for t in range(T):
        for r in range(len(R)):
            task = int(schedule[r, t])
            if task > 0:
                task_attr = task_attributes[task]
                robot_type = problem_data[0][r + 1]  # ロボットタイプ
                work = robot_abilities[robot_type][task_attr]
                task_workspace = workspace[task]

                # 移動コスト考慮
                if current_workspace[r] != task_workspace:
                    cost = moving_cost[current_workspace[r]][task_workspace]
                    work = work * (1 - cost / robot_abilities[robot_type]['move'])
                    current_workspace[r] = task_workspace

                workload[task - 1] += work

                # タスク完了判定
                if workload[task - 1] >= p[task]:
                    task_completed[task - 1] = 1
                    if task_completion_time[task - 1] == -1:
                        task_completion_time[task - 1] = t + 1

    # 評価値の計算
    evaluation_value = 0
    if np.all(task_completed):
        evaluation_value = np.max(task_completion_time)
        print(f"All tasks completed by evaluation_value {evaluation_value}")
    else:
        # 未完了タスクがある場合は、まずTを加算する
        evaluation_value += T
        print(f"Some tasks are incomplete. Base evaluation value: {evaluation_value}")

        # 残りの仕事量を合算する
        for j in range(len(J)):
            if task_completed[j] == 0:
                remaining_workload = p[J[j]] - workload[j]
                evaluation_value += remaining_workload   # 残り仕事量のみを追加
                print(f"Task {J[j]} is incomplete. Remaining workload: {remaining_workload}. Total evaluation value now: {evaluation_value}")
                
    return evaluation_value