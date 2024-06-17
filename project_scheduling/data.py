# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:32:52 2024

@author: k5kei
"""

def make_1r():
    J = [1, 2, 3, 4]
    p = {1: 1, 2: 3, 3: 2, 4: 2}
    P = [(1, 2), (1, 3), (2, 4)]
    R = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    T = 6
    c = {(j, t): 1 * (t - 1 + p[j]) for j in J for t in range(1, T - p[j] + 2)}
    a = {
        (1, 1, 0): 2,
        (2, 1, 0): 2,
        (2, 1, 1): 1,
        (2, 1, 2): 1,
        (3, 1, 0): 1,
        (3, 1, 1): 1,
        (4, 1, 0): 1,
        (4, 1, 1): 2,
    }
    RUB = {(1, t): 2 for t in range(1, T + 1)}
    
    locations = {1: 'A', 2: 'B', 3: 'C', 4: 'A'}
    tasks = {1: 'X', 2: 'Y', 3: 'X', 4: 'Y'}
    
    travel_time = {
        'A': {'A': 0, 'B': 2, 'C': 4},
        'B': {'A': 2, 'B': 0, 'C': 3},
        'C': {'A': 4, 'B': 3, 'C': 0}
    }
    
    robot_initial_locations = {r: 'A' for r in R}
    
    return (J, P, R, T, p, c, a, RUB, locations, tasks, travel_time, robot_initial_locations)

def make_2r():
    J = [1, 2, 3, 4, 5]
    p = {1: 2, 2: 2, 3: 3, 4: 2, 5: 5}
    P = [(1, 2), (1, 3), (2, 4)]
    R = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    T = 6
    c = {(j, t): 1 * (t - 1 + p[j]) for j in J for t in range(1, T - p[j] + 2)}
    a = {
        (1, 1, 0): 2, (1, 1, 1): 2, (2, 1, 0): 1, (2, 1, 1): 1, (3, 1, 0): 1, (3, 1, 1): 1, (3, 1, 2): 1, 
        (4, 1, 0): 1, (4, 1, 1): 1, (5, 1, 0): 0, (5, 1, 1): 0, (5, 1, 2): 1, (5, 1, 3): 0, (5, 1, 4): 0, 
        (1, 2, 0): 1, (1, 2, 1): 0, (2, 2, 0): 1, (2, 2, 1): 1, (3, 2, 0): 0, (3, 2, 1): 0, (3, 2, 2): 0, 
        (4, 2, 0): 1, (4, 2, 1): 2, (5, 2, 0): 1, (5, 2, 1): 2, (5, 2, 2): 1, (5, 2, 3): 1, (5, 2, 4): 1
    }
    RUB = {(r, t): 2 for r in R for t in range(1, T + 1)}
    
    locations = {1: 'A', 2: 'B', 3: 'C', 4: 'A', 5: 'B'}
    tasks = {1: 'X', 2: 'Y', 3: 'X', 4: 'Y', 5: 'X'}
    
    travel_time = {
        'A': {'A': 0, 'B': 2, 'C': 4},
        'B': {'A': 2, 'B': 0, 'C': 3},
        'C': {'A': 4, 'B': 3, 'C': 0}
    }
    
    robot_initial_locations = {r: 'A' for r in R}
    
    return (J, P, R, T, p, c, a, RUB, locations, tasks, travel_time, robot_initial_locations)
