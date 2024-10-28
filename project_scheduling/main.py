
# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:33:59 2024

@author: k5kei
"""

# main.py

from data import make_1r
from optimization import solve_problem
from plot import plot_schedule

def main():
    problem_data = make_1r()
    
    J, p, task_attributes, P, R, robot_types, T, robot_capacities, workspace, workspace_distance, robot_initial_positions, C, RUB = problem_data
    
    result = solve_problem(problem_data)
    #print(result)  # ここでresultが正しく得られているか確認する
    
    J, p, task_attributes, P, R, robot_types, T, robot_capacities, workspace, workspace_distance, robot_initial_positions, C, RUB = problem_data  # C の読み込み修正
    plot_schedule(result, J, R, T, robot_types)
    

if __name__ == "__main__":
    main()