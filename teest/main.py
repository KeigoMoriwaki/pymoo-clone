# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 10:48:13 2024

@author: k5kei
"""

from scheduler import optimize_schedule
from visualization import plot_schedule
from data import get_data

def main():
    jobs, robots, distances = get_data()
    schedule = optimize_schedule(jobs, robots, distances)
    plot_schedule(schedule, jobs, robots)

if __name__ == "__main__":
    main()
