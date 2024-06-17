# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 22:54:00 2024

@author: k5kei
"""

class Job:
    def __init__(self, id, duration, location, task_type):
        self.id = id
        self.duration = duration
        self.location = location
        self.task_type = task_type

    def get_duration(self):
        return self.duration

    def get_location(self):
        return self.location

    def get_task_type(self):
        return self.task_type
