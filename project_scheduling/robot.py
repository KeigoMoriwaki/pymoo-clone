# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 11:28:43 2024

@author: k5kei
"""


class Robot:
    def __init__(self, id, current_location='A'):
        self.id = id
        self.current_location = current_location

    def move_to(self, new_location, travel_time):
        self.current_location = new_location
        return travel_time[self.current_location][new_location]
