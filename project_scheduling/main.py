# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:33:59 2024

@author: k5kei
"""

import data
import problem
import optimization
import plot
import job
import robot

# データの読み込み
J, P, R, T, p, c, a, RUB, locations, tasks, travel_time = data.make_1r()

# 問題の定義
problem_instance = problem.ResourceConstrainedSchedulingProblem(J, P, R, T, p, c, a, RUB, locations, tasks, travel_time)

# 最適化の実行
result = optimization.solve_problem(problem_instance)

# グラフのプロット
plot.plot_timeline(J, T, result, p, locations, R, travel_time)
