# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 09:54:15 2019

@author: toprak.kesgin
"""

import random
import matplotlib.pyplot as plt
import copy
from Environment import Environment
import time


class GenetikAlgorithm():

    # Constructor For GenetikAlgorithm.
    # start = starting coordinates [0,0]
    # end = ending coordinates     [5,5]
    # environment = The Grid Map with Obstacles
    # runtime = limited runtime of drone  50

    def __init__(self,start,end,environment,runtime):
        self.start = start
        self.end = end
        self.maze = environment
        self.moves = self.getMoves()
        self.pop = self.initializePop(250)
        self.runtime = runtime

    # Fitness function to evaluate the produced paths
    # state = path array

    def fitness(self,state):
        i = 0

        # to exit while hitting an obstacle or leaving the map

        flag = True

        # get the copy of map

        tmpMap = self.maze.Map.copy()

        # get the start point coorinates

        tmpStart = self.start.copy()

        # set these coordinates on the map for visualization

        #tmpMap[tmpStart[0]][tmpStart[1]] = 2

        # Out of Map Cost

        mazeCost = 0

        # Hitting the obstacle Cost

        ObstacleCost = 0

        # Manhatten distance from current state to end state

        DistanceCost = 0

        # the cost of how little moved on the map

        PathCost = 0

        # whether the path found.

        found = False

        # If the state's fitness score was calculated in advance

        if len(state) == 3:
            state = state[0]

        while i < len(state) and flag == True:

            # where is it on the map now

            current = tmpStart

            # Left, Right, Up and Down

            if(state[i] == 1):
                current[0] -= 1
            elif(state[i] == 2):
                current[0] += 1
            elif(state[i] == 3):
                current[1] -= 1
            else:
                current[1] += 1

            # to exit from while at the end of the state.

            i+=1

            # if outside of the map

            if current[0] < 0 or current[1] < 0 or current[0] >= self.maze.n or current[1] >= self.maze.m:

                # To Exit While

                flag = False

                # Out of Map Cost

                mazeCost = 100

            # if there is an obstacle

            elif tmpMap[current[0]][current[1]] == 1:

                # if hits the obstacle random change last 4 moves

                index = int(i/4)*4

                rd = random.randint(0, 99)
                rd *= 4


                state[index] = self.moves[rd]
                state[index+1] = self.moves[rd+1]
                state[index+2] = self.moves[rd+2]
                state[index+3] = self.moves[rd+3]

                # To Exit While

                flag = False

                # Hitting the obstacle Cost

                ObstacleCost = 50


            # if the end point are reached

            elif current == self.end:

                # To Exit While

                flag = False

                # Path is Found

                found = True


        # Manhatten distance Cost

        DistanceCost = (abs(current[0] - self.end[0]) + abs(current[1] - self.end[1]))*5


        # if the path is found how good is this path

        if found==True:
            PathCost = int(i / 1)

        # the cost of how little moved on the map

        else:
            PathCost = (10 - (abs(current[0] - self.start[0]) + abs(current[1] - self.start[1]) ) )
            PathCost += (160 - i)
            if PathCost < 0:
                PathCost = 0

        # Sum of All Costs

        Cost = mazeCost + ObstacleCost + DistanceCost + PathCost

        # Returning required variables

        return state,Cost,found,i


    # initializes the first random population

    def initializePop(self,popCount):

        # Lists for population

        population = []
        path = []
        individual = []

        # For loop for given population count

        for j in range(0,popCount):

            # 70*4 move count of individual

            for i in range(0,90):

                # Creates random moves for map

                rd = random.randint(0, 99)
                rd *= 4
                path.append(self.moves[rd])
                path.append(self.moves[rd+1])
                path.append(self.moves[rd+2])
                path.append(self.moves[rd+3])

            # Adding created individuals to population

            path,fitnessPoint,found,yol = self.fitness(path)
            individual.append(path)
            individual.append(fitnessPoint)
            individual.append(found)
            individual.append(yol)
            population.append(individual)
            individual = []
            path = []
        return population

    # Returns the best individual of population

    def bestindividual(self):
        min = self.pop[0][1]
        best = self.pop[0]
        for i in self.pop:
            if (i[1] < min):
                min = i[1]
                best = i
        return best

    # Returns the worst individual of population

    def worstindividual(self):
        min = self.pop[0][1]
        best = self.pop[0]
        for i in self.pop:
            if (i[1] > min):
                min = i[1]
                best = i
        return best


    # For given two individual creates a new individual

    def crossover(self,parent1,parent2):

        # Creates random division point

        rd = random.randint(1, int((len(parent1[0]) / 4) - 1))
        rd *= 4
        child = []
        path = []

        # Adds some part of parent1

        for i in range(rd):
            path.append(parent1[0][i])

        # Adds other part of parent2

        while i < len(parent1[0])-1:
            path.append(parent2[0][i])
            i += 1

        # Calculates fitness of new child and returns the child

        path,fitnessPoint,found,yol = self.fitness(path)
        child.append(path)
        child.append(fitnessPoint)
        child.append(found)
        child.append(yol)

        return child

    # For given individual changes the random 4 values of these individual

    def mutation(self,child):

        # Creates a random split point

        rd = random.randint(1, int((len(child[0]) / 4) - 1))
        rd *= 4

        rd2 = random.randint(0, 99)
        rd2 *= 4

        # Changes 4 values with 4 randomly created new values

        child[0][rd] = self.moves[rd2]
        child[0][rd+1] = self.moves[rd2+1]
        child[0][rd+2] = self.moves[rd2+2]
        child[0][rd+3] = self.moves[rd2+3]

        # Calculates new individual's new fitness score

        child[0],fitnessPoint,found,yol = self.fitness(child[0])
        child[1] = fitnessPoint
        child[2] = found
        child[3] = yol

        return child

    def genetic(self):

        # For maximum value of while loop

        k = 0

        foundTmp = False

        while(not(foundTmp) and k < 2000):
            if k % 100 == 0:
                print(str(k) + " " + "Best Score " + str(self.bestindividual()[1]) + " " + str(self.bestindividual()[2]))
            k += 1
#            if k % 100 == 0:
#                self.ShowPath(self.bestindividual())
            # Creates empty new population

            newpop = []

            # Adds the founds maps to new population

            foundTmp = self.getFound()
            for j in foundTmp:
                newpop.append(j)

            # Removes the worst 10 individual from the population

            for i in range(10):
                worst = self.worstindividual()
                self.pop.remove(worst)

            # Creates new 10 length population and adds to new population

            RanPop = self.initializePop(10)
            for j in RanPop:
                self.pop.append(j)

            u = len(newpop)

            # Empties the Random Population

            RanPop = []

            # Main Loop For Reproduce

            for i in range(len(self.pop) - u - 100):

                # Selects two random individual

                parent1 = self.selection()
                parent2 = self.selection()
                m = 0

                # if these 2 individual same selects again

                while(parent1==parent2 and m < 10):
                    parent2 = self.selection()
                    m += 1

                # creates a new individual with these parents

                child = self.crossover(parent1,parent2)

                # if there will be a mutation

                if (random.randint(1, 100) < 85):

                    # How many kromozom will change

                    for mn in range(random.randint(1, 20)):
                        child = self.mutation(child)

                # Finally adds the new child to new population

                newpop.append(child)

            # Holds the best 100 individual from previous population

            for n in range(100):
                best = self.bestindividual()
                self.pop.remove(best)

                # if the path is not found creates occurs mutation with some probability

                if (random.randint(1, 100) < 40 and not(best[2])):
                    for mn in range(random.randint(1, 3)):
                        best = self.mutation(best)

                # Adds these individuals to new population

                newpop.append(best)

            # Changes old population with new population

            self.pop = newpop




        # if the found path exceeds the runtime gives warnings


        # Returns the best individual and it's coordinates

        if self.getFound():

            # Shortens the found path

            Cor = self.getCor(self.getFound()[0])
            Cor = self.TrimPath(Cor)
            Cor = self.TrimPathNew(Cor)
            if len(Cor) > self.runtime:
                print("Not Enough Runtime")
                return -1
            return Cor
        else:
            print("path not found")

            Cor = self.getCor(self.bestindividual())
            Cor = self.TrimPath(Cor)
            Cor = self.TrimPathNew(Cor)

            return 0

    # Finds the found paths from population

    def getFound(self):
        foundparents = []
        for i in self.pop:
            if i[2]:
                foundparents.append(i)
        return foundparents

    # returns random individual according to it's fitness score

    def selection(self):
        sum = 0
        pr = []
        p = 0
        for i in self.pop:
            sum += int((800 - i[1]))
            pr.append(sum)

        p = random.randint(1, sum)
        c = 0
        while pr[c] < p:
            c += 1

        return self.pop[c]

    # For given state shows to pgn of the path

    def ShowPath(self,state):
        tmpMap = copy.deepcopy(self.maze.Map)
        current = self.start.copy()
        i = 0
        flag = True
        while flag and i < len(state[0]):

            if(state[0][i] == 1):
                current[0] -= 1
            elif(state[0][i] == 2):
                current[0] += 1
            elif(state[0][i] == 3):
                current[1] -= 1
            else:
                current[1] += 1
            i+=1

            if current[0] < 0 or current[1] < 0 or current[0] >= self.maze.n or current[1] >= self.maze.m:
                print("maze dışı öldü")
                flag = False
            elif tmpMap[current[0]][current[1]] == 1:
                print("Engel var öldü")
                flag = False
            elif current == self.end:
                flag = False

            tmpMap[current[0]][current[1]] = 2
        plt.imshow(self.maze.Map)
        plt.show()
        plt.imshow(tmpMap)
        plt.show()

    # returns the coordinates of given state

    def getCor(self,state):
        tmpMap = copy.deepcopy(self.maze.Map)
        current = self.start.copy()
        i = 0
        flag = True
        pathCor = []
        pathCor.append(current.copy())
        amaze = True
        while flag and i < len(state[0]):

            if(state[0][i] == 1):
                current[0] -= 1
            elif(state[0][i] == 2):
                current[0] += 1
            elif(state[0][i] == 3):
                current[1] -= 1
            else:
                current[1] += 1
            i+=1
            pathCor.append(current.copy())

            if current[0] < 0 or current[1] < 0 or current[0] >= self.maze.n or current[1] >= self.maze.m:
                print("maze dışı öldü")
                amaze = False
                flag = False
            elif tmpMap[current[0]][current[1]] == 1:
                print("Engel var öldü")
                flag = False
            elif current == self.end:
                flag = False

            if(amaze):
                tmpMap[current[0]][current[1]] = 2

        return self.TrimPath(pathCor)

    # Following theree methods used for shortening path
    # if the same coordinate reached before it removes the middle coordinates

    def search(self,liste,index):
        i = index + 1
        size = len(liste)
        while(i < size and liste[i] != liste[index]):
            i += 1
        if (i < size):
            return i
        else:
            False

    def delete(self,liste,index1,index2):

        for i in range(index1,index2):
            liste.pop(index1)
        return liste

    def TrimPath(self,liste):
        size = len(liste)

        k = 0

        while k < size:
            index2 = self.search(liste,k)
            if index2:
                if(index2 < len(liste)):
                    liste = self.delete(liste,k,index2)
            k += 1
            size = len(liste)
        return liste

    # Shows the png's of given coordinates

    def ShowMapCor(self,path):
        tmpMap = copy.deepcopy(self.maze.Map)
        if(path == -1 or path == 0):
            return
        print("Path that found by GeneticAlgorithm ")
        for i in path:
            a = i[0]
            b = i[1]
            if not(i[0] >= self.maze.n or i[1] >= self.maze.m or i[0] < 0 or i[1] < 0):
                tmpMap[a][b] = 2
        plt.imshow(tmpMap)
        plt.show()

    # creates the all reasonable moves for 4 moves by eliminateing unnecessary moves
    # reduces all 256 moves to 100 moves

    def getMoves(self):

        ihtimaller = []

        for i in range(1,5):
            for ii in range(1,5):
                for iii in range(1,5):
                    for iiii in range(1,5):
                        if not(i + ii == 3 or i + ii == 7 or ii + iii == 3 or ii + iii == 7 or iii + iiii == 3 or iii + iiii == 7):
                            tmp = []
                            tmp.append(i)
                            tmp.append(ii)
                            tmp.append(iii)
                            tmp.append(iiii)
                            ihtimaller.append(tmp)

        def ara(ihtimaller,sayı):
            for i in ihtimaller:
                if i == sayı:
                    return True
            return False

        silinecek = []
        for j in ihtimaller:
            sum = 0
            for i in range(1,5):
                if ara(j,i):
                    sum += 1
            if sum == 4:
                silinecek.append(j)

        for j in ihtimaller:
            if j in silinecek:
                ihtimaller.remove(j)

        son = []
        for j in ihtimaller:
            son.append(j[0])
            son.append(j[1])
            son.append(j[2])
            son.append(j[3])

        return son

    # Following 4 method shortens the path even more
    # it's logic: if any coordinates can be reach with one move but its reach more than one move
    # it deletes the middle koordinates and go these new coordinates with one movement

    def manEqNew(self,cor1,cor2):
        sum = abs(cor1[0] - cor2[0]) + abs(cor1[1] - cor2[1])
        if sum == 1:
            return True
        else:
            return False

    def searchNew(self,liste,index):
            i = index + 2
            size = len(liste)
            while(i < size and not(self.manEqNew(liste[i],liste[index]))):
                i += 1
            if (i < size):
                return i
            else:
                False

    def deleteNew(self,liste,index1,index2):
        for i in range(index1+1,index2):
            liste.pop(index1+1)
        return liste

    def TrimPathNew(self,liste):
        size = len(liste)

        k = 0

        while k < size:
            index2 = self.searchNew(liste,k)
            if index2:
                if(index2 < len(liste)):
                    liste = self.deleteNew(liste,k,index2)
            k += 1
            size = len(liste)
        return liste
