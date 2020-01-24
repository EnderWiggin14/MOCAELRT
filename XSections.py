# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 14:04:49 2020

@author: Michael Vander Wal
"""
import numpy as np
# import TransportConstants as TC

class XSection():
    xSection = None
    energyValues = None
    discrete = True
    def __init__(self,crossSection,energy,discrete = True):
        self.xSection = np.array(crossSection)
        self.energyValues = np.array(energy)
        self.discrete = discrete


    def getXSection(self,energy):
        if self.discrete:
            return self.interp(energy)
        else:
            return self.interp(energy) #need to change to a function in future
        return

    def interp(self,xStar): # should replace while loop with numpy.searchsort()
        i = np.searchsorted(self.energyValues,xStar,side='right')
        x1 = self.energyValues[i-1]
        x2 = self.energyValues[i]
        y1 = self.xSection[i-1]
        y2 = self.xSection[i]
        ystar = ((xStar-x1)/(x2-x1))*(y2-y1)+y1
        return ystar