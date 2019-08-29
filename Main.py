# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 09:57:25 2019

@author: toprak.kesgin
"""


import matplotlib.pyplot as plt
from Environment import Environment
from GeneticAlgorithm import GenetikAlgorithm


harita = Environment(30,30)
harita.randomMap()
a = harita.Map
start = [2,5]
end =  [25,29]
harita.showMap()

Genetik = GenetikAlgorithm(start,end,harita,100)
Cor = Genetik.genetic()
Genetik.ShowMapCor(Cor)

