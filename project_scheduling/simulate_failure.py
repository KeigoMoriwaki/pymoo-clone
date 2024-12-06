# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 08:23:11 2024

@author: k5kei
"""

import numpy as np

def simulate_schedule1(result, problem_data, consider_failures=True):
    robot_types, robot_initial_positions, J, p, task_attributes, P, R, T, robot_abilities, workspace, workspace_distance, moving_cost, C, RUB = problem_data

    schedule = result.X.reshape((len(R), T))
    
    seeds = range(80, 90)
    
    evaluation_values_per_seed = []  # 各シード値の評価値を格納するリスト
    
    for seed in seeds:
    
        rng = np.random.default_rng(seeds)
    
        workload = np.zeros(len(J))
        task_completed = np.zeros(len(J))
        task_completion_time = np.full(len(J), -1)
        current_workspace = {r: robot_initial_positions[r + 1] for r in range(len(R))}
    
        for t in range(T):
            for r in range(len(R)):
                
                task = int(schedule[r, t])
                
                if task > 0:
                    task_attr = task_attributes[task]
                    robot_type = problem_data[0][r + 1]
                    work = robot_abilities[robot_type][task_attr]
                    task_workspace = workspace[task]
                    
                    if current_workspace[r] != task_workspace:
                        cost = moving_cost[current_workspace[r]][task_workspace]
                        work = work * (1 - cost / robot_abilities[robot_type]['move'])
                        current_workspace[r] = task_workspace
                        
                    if consider_failures and rng.random() > 1 - C:
                        continue
                    
                    workload[task - 1] += work
                    if workload[task - 1] >= p[task]:
                        task_completed[task - 1] = 1
                        if task_completion_time[task - 1] == -1:
                            task_completion_time[task - 1] = t + 1

            # シード値ごとの評価値を保存
        evaluation_value_seed = 0
        if np.all(task_completed):
            evaluation_value_seed = np.max(task_completion_time)
        else:
            evaluation_value_seed += T
            for j in range(len(J)):
                if task_completed[j] == 0:
                    remaining_workload = p[J[j]] - workload[j]
                    evaluation_value_seed += remaining_workload
                
        # シード値ごとの評価値をリストに追加
        evaluation_values_per_seed.append(evaluation_value_seed)
                
            # シード範囲の平均を計算
    evaluation_with_failure = np.mean(evaluation_values_per_seed)

    return evaluation_with_failure