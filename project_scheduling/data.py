# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:32:52 2024

@author: k5kei
"""

import yaml  # 外部ファイルを読み込むためのモジュール

def load_robot_data(yaml_file):
    """
    YAMLファイルを読み込み、ロボットのタイプ、初期位置、workspaceの対応を生成する。
    """
    with open(yaml_file, 'r') as file:
        robot_data = yaml.safe_load(file)

    # ロボットIDのリストを生成
    robot_types = {}
    robot_initial_positions = {}
    workspace_mapping = {
        '[0.0, 0.0]': '1',
        '[5.0, 5.0]': '2',
        '[0.0, 5.0]': '3',
        '[-5.0, -5.0]': '4'
    }

    id_counter = 1

    for robot_name, details in robot_data.items():
        robot_types[id_counter] = details['robot_type']
        robot_initial_positions[id_counter] = workspace_mapping[str(details['coordinate'])]
        id_counter += 1

    return robot_types, robot_initial_positions

def make_1r():
    # YAMLからロボット情報を読み込む
    yaml_file = "Robots.yaml"  # YAMLファイルのパス
    robot_types, robot_initial_positions = load_robot_data(yaml_file)

    J = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]  # タスクID
    p = {1: 12, 2: 6, 3: 10, 4: 3, 5: 3, 6: 3, 
         7: 3, 8: 3, 9: 3, 10: 3, 11: 3, 12: 5, 
         13: 5, 14: 4, 15: 4, 16: 5, 17: 8}  # 各タスクの仕事量

    task_attributes = {
        1: 'carry',
        2: 'build',
        3: 'build',
        4: 'carry',
        5: 'carry',
        6: 'carry',
        7: 'carry',
        8: 'build',
        9: 'build',
        10: 'build',
        11: 'build',
        12: 'build',
        13: 'build',
        14: 'carry',
        15: 'carry',
        16: 'build',
        17: 'build'
    }

    P = [(1, 2), (2, 3), (4, 8), (5, 9), (6, 10), (7, 11), (14, 16), (15, 17)]

    R = list(robot_types.keys())  # ロボットIDのリスト
    T = 6  # 総期間長

    robot_abilities = {
        'TWSH': {'carry': 3, 'build': 3, 'move': 3},
        'TWDH': {'carry': 3, 'build': 5, 'move': 3},
        'QWSH': {'carry': 4, 'build': 3, 'move': 3},
        'QWDH': {'carry': 4, 'build': 5, 'move': 3},
        'Dragon': {'carry': 1, 'build': 3, 'move': 2},
        'Minimal': {'carry': 1, 'build': 3, 'move': 1}
    }
    
    workspace = {1: '1', 2: '2', 3: '2', 4: '1', 5: '1', 6: '1', 
                 7: '1', 8: '3', 9: '3', 10: '3', 11: '3', 12: '3', 
                 13: '3', 14: '1', 15: '1', 16: '4', 17: '4'}

    workspace_distance = {
        '1': {'1': 0, '2': 7, '3': 5, '4': 7},
        '2': {'1': 7, '2': 0, '3': 5, '4': 14},
        '3': {'1': 5, '2': 5, '3': 0, '4': 11},
        '4': {'1': 7, '2': 14, '3': 11, '4': 0}
    }

    moving_cost = {
        '1': {'1': 0, '2': 0.35, '3': 0.25, '4': 0.35},
        '2': {'1': 0.35, '2': 0, '3': 0.25, '4': 0.7},
        '3': {'1': 0.25, '2': 0.25, '3': 0, '4': 0.55},
        '4': {'1': 0.35, '2': 0.7, '3': 0.55, '4': 0}
    }

    C = 0.1  # 故障確率の係数
    
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

    return robot_types, robot_initial_positions, J, p, task_attributes, P, R, T, robot_abilities, workspace, workspace_distance, moving_cost, C, RUB