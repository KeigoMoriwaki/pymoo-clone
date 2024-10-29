# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:32:52 2024

@author: k5kei
"""

def make_1r():
    J = [1, 2, 3, 4]  # タスクID
    p = {1: 40, 2: 30, 3: 60, 4: 60}  # 各タスクの仕事量
    
    # 各タスクの属性 ('運搬' または '建設')
    task_attributes = {
        1: 'carry',
        2: 'carry',
        3: 'build',
        4: 'build'
    }
    
    #P = [[], [1, 2], [1, 3], [2, 4]]  # 各タスクの順序制約
    P = [(1, 2), (1, 3), (2, 4)]
    R = [1, 2, 3]  # 各ロボット種類のID
    robot_types = {
        1: 'TWSH',
        2: 'QWDH',
        3: 'Worm'
    }
    
    T = 60  # 総期間長data.py
    
    # 各ロボットの種類ごとに、運搬と建設の仕事量
    robot_abilities = {
        'TWSH': {'carry': 3, 'build': 3, 'move': 2},
        'TWDH': {'carry': 3, 'build': 5, 'move': 2},
        'QWSH': {'carry': 5, 'build': 3, 'move': 3},
        'QWDH': {'carry': 5, 'build': 5, 'move': 3},
        'Worm': {'carry': 1, 'build': 1, 'move': 2},
        'Hand': {'carry': 1, 'build': 1, 'move': 1}
    }
    
    workspace = {1: '1', 2: '2', 3: '3', 4: '4'}
    workspace_distance = {
        '1': {'1': 0, '2': 10, '3': 20, '4': 30},
        '2': {'1': 10, '2': 0, '3': 30, '4': 20},
        '3': {'1': 20, '2': 30, '3': 0, '4': 10},
        '4': {'1': 30, '2': 20, '3': 10, '4': 0}
    }
    
    # 各ロボットの初期位置を設定する辞書
    robot_initial_positions = {1: '1', 2: '1', 3: '1'}  # ロボット1はワークスペース1からスタートなど
    
    C = 0.01  # 故障確率の係数
    
    # 各期間ごとに仕事をスタートさせる費用，今回の問題では必要ない
    # c = {(j, t): 1 * (t - 1 + p[j]) for j in J for t in range(1, T - p[j] + 2)}
    # 各期間ごとにどの資源がどれだけ必要かが定義されるが，今回の問題では必要ない
    # a = {
    #     (1, 1, 0): 2,
    #     (2, 1, 0): 2,
    #     (2, 1, 1): 1,
    #     (2, 1, 2): 1,
    #     (3, 1, 0): 1,
    #     (3, 1, 1): 1,
    #     (4, 1, 0): 1,
    #     (4, 1, 1): 2,
    # }
    # 各期間ごとにどのロボットがどれだけ働けるか（各ロボットの台数）
    RUB = {
        (1, 1): 2,
        (1, 2): 2,
        (1, 3): 2,
        (1, 4): 2,
        (1, 5): 2,
        (1, 6): 2,
        (1, 7): 2,
        (2, 1): 1,
        (2, 2): 1,
        (2, 3): 1,
        (2, 4): 1,
        (2, 5): 1,
        (2, 6): 1,
        (2, 7): 1,
        (3, 1): 1,
        (3, 2): 1,
        (3, 3): 1,
        (3, 4): 1,
        (3, 5): 1,
        (3, 6): 1,
        (3, 7): 1,
    }

    return J, p, task_attributes, P, R, robot_types, T, robot_abilities, workspace, workspace_distance, robot_initial_positions, C, RUB