# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 11:28:59 2024

@author: k5kei
"""

def calculate_travel_times(start_locations, end_locations, travel_time):
    times = []
    for start, end in zip(start_locations, end_locations):
        times.append(travel_time[start][end])
    return times
