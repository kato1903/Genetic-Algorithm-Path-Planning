#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on Mon Jul  1 09:51:31 2019

@author: toprak.kesgin
"""

import random
import matplotlib.pyplot as plt
import copy


# Environment Class Holds the grid map, obstacles and size of Map

class Environment:

    # Constructor for Environment

    def __init__(self, n, m, maplist="empty"):
        if n > 30 or m > 30 or n < 4 or m < 4:
            return None
        self.n = n
        self.m = m
        if maplist == "empty":
            self.Map = self.emptyMap(n, m)
        else:
            self.Map = maplist

    # Craates Empty Map

    def emptyMap(self, n, m):
        eMap = []
        for i in range(n):
            tmp = []
            for j in range(m):
                tmp.append(0)
            eMap.append(tmp)
        return eMap

    # Creates Random Map filled with obstacles

    def randomMap(self):
        Map = []
        for i in range(self.n):
            tmp = []
            for j in range(self.m):
                r = random.randint(1, 100)
                if r < 20:
                    tmp.append(1)
                else:
                    tmp.append(0)
            Map.append(tmp)
        self.Map = Map

    # Adds an obstacle for given coordinates

    def AddObstacle(self, x, y):
        if x < 30 and y < 30 and x >= 0 and y >= 0:
            print("girdi mi")
            self.Map[x][y] = 1
            return 1
        return 0

    # Deletes Obstacles for given coordinates

    def DeleteObstacle(self, x, y):
        if x < 30 and y < 30 and x >= 0 and y >= 0:
            self.Map[x][y] = 0
            return 1
        return 0

    # Shows the png of Map

    def showMap(self):
        plt.imshow(self.Map)
        plt.show()



