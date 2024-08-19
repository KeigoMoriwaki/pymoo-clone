# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:32:04 2024

@author: k5kei
"""

import numpy as np
import copy
from pymoo.core.problem import Problem

class ResourceConstrainedSchedulingProblem(Problem):
    # Parameters:
    #     - J: set of jobs
    #     - P: set of precedence constraints between jobs
    #     - R: set of resources
    #     - T: number of periods
    #     - p[j]: processing time of job j
    #     - RUB[r,t]: upper bound for resource r on period t
    #     - C: failure probability coefficient

    def __init__(self, problem_data):
        self.J, self.P, self.R, self.T, self.p, self.RUB, self.C = problem_data
        n_var = len(self.J) * self.T
        super().__init__(n_var=n_var,
                         n_obj=1,
                         n_constr=1,
                         xl=0,
                         xu=len(self.R),
                         type_var=int)

    def _evaluate(self, x, out, *args, **kwargs):
        finish_times = []
        constraints = []
        
        for ind in x:
            schedule = ind.reshape((len(self.J), self.T))
            leftover = copy.deepcopy(self.p)
            resource_constraints = 0
            failure_constraints = 0
            precedence_constraints = 0
            task_completion_constraints = 0
            t = 0
            task_end_times = {}
        
            for t in range(self.T):
                n_worker = np.zeros(len(self.R))
                for j in range(len(self.J)):
                    robot = schedule[j, t]
                    if robot != 0:
                        # ロボットの故障確率を考慮
                        failure_probability = 1 - self.C * t
                        if np.random.rand() > failure_probability:
                            failure_constraints += 1  # 故障が発生した場合のペナルティ
                            continue
                    
                        if n_worker[robot-1] > 0:
                            resource_constraints += 1  # 同じロボットに複数のタスクが割り当てられた場合のペナルティ
                            
                        if leftover[self.J[j]] > 0:
                            task_completion_constraints += 1  # タスクが完了していない場合のペナルティ
                    
                        n_worker[robot-1] += 1
                        leftover[self.J[j]] -= 1
                        if leftover[self.J[j]] <= 0:
                            leftover[self.J[j]] = 0
                            task_end_times[self.J[j]] = t + 1  # タスクが終了した時間を記録

                if sum(leftover.values()) == 0:
                    break

            finish_times.append(t + 1)

            # リソース制約を考慮
            for t in range(self.T):
                n_worker = np.zeros(len(self.R))
                for j in range(len(self.J)):
                    robot = schedule[j, t]
                    if robot != 0:
                        n_worker[robot-1] += 1
                for r in range(len(self.R)):
                    if self.RUB[(r+1, t+1)] < n_worker[r]:
                        resource_constraints += 1
                        
            # 順序制約を確認
            for (pre, post) in self.P:
                if pre in task_end_times and post in task_end_times:
                    if task_end_times[post] <= task_end_times[pre]:
                        precedence_constraints += 1  # 順序制約違反のペナルティ

            finish_times.append(t + 1)
            constraints.append(resource_constraints + failure_constraints + precedence_constraints + task_completion_constraints)
            
            # finish_timesの要素数が300になるように調整
            if len(finish_times) > 300:
                finish_times = finish_times[:300]
            elif len(finish_times) < 300:
            # 要素数が足りない場合は、適切な値で補填する
                finish_times.extend([0] * (300 - len(finish_times)))

        out["F"] = np.array(finish_times).reshape(-1, 1)
        out["G"] = np.array(constraints).reshape(-1, 1)
        
        
        
        #ロボットに対して同時間帯に2つ以上のタスクを割り振らないようにするのではなく
        #タスクのIDが若い方を優先するようにする