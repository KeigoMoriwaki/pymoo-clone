# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 10:48:50 2024

@author: k5kei
"""

import numpy as np
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize

class SchedulingProblem(ElementwiseProblem):
    def __init__(self, jobs, robots, distances):
        self.jobs = jobs
        self.robots = robots
        self.distances = distances
        super().__init__(n_var=len(jobs), n_obj=1, n_constr=0, xl=0, xu=len(robots)-1)
    
    def _evaluate(self, x, out, *args, **kwargs):
        total_time = 0
        robot_times = [0] * len(self.robots)
        robot_positions = [0] * len(self.robots)

        for job_idx, robot_idx in enumerate(x):
            job = self.jobs[job_idx]
            robot_idx = int(round(robot_idx))  # インデックスを整数に変換
            robot = self.robots[robot_idx]

            travel_time = self.distances[robot_positions[robot_idx]][job['location']]
            robot_positions[robot_idx] = job['location']

            execution_time = job['workload'] / robot['capacity']

            robot_times[robot_idx] += travel_time + execution_time

        total_time = max(robot_times)
        out["F"] = total_time

def optimize_schedule(jobs, robots, distances):
    problem = SchedulingProblem(jobs, robots, distances)
    algorithm = GA(pop_size=100)
    result = minimize(problem, algorithm, seed=1, verbose=True)
    return result.X



