# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 10:49:54 2024

@author: k5kei
"""

def get_data():
    jobs = [
        {'workload': 15, 'location': 0},
        {'workload': 15, 'location': 1},
        {'workload': 20, 'location': 2},
        {'workload': 25, 'location': 0},
        {'workload': 35, 'location': 1},
        {'workload': 50, 'location': 2},
    ]
    
    robots = [
        {'capacity': 1},
        {'capacity': 1.5},
        {'capacity': 2}, 
        {'capacity': 2}, 
    ]

    distances = [
        [0, 10, 20],
        [10, 0, 15],
        [20, 15, 0],
    ]

    return jobs, robots, distances
