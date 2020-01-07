   # -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 11:34:53 2019

@author: Michael Vander Wal
"""
import numpy as np

class SourceManager():
    sourceList = None
    def __init__(self):
        return

    def addSource(self,source):
        self.sourceList.append(source)

class Source():
    sourceType = 'point'
    sourceLocation = None
    sourceDirection = None
    E = None
    def __init__(self):
        return

    def setType(self,sourceType = "point"):
        self.sourceType = sourceType

    def setLocation(self,location = np.array([0.,0.,0.])):
        self.sourceLocation = np.array(location)

    def setCenter(self,location):
        self.setLocation(location)

    def setDirection(self,direction = np.array([0.,0.,1.])):
        self.sourceDirection = direction

    def setEnergy(self,energy=1000):
        self.E = energy

if __name__=="__main__":
    a = SourceManager()
    b = Source()
    b.setLocation()
    b.setEnergy()
    b.setDirection()
    print(b.sourceType, '\t', b.sourceLocation,'\t',b.sourceDirection,'\t',b.E)
    print("Successfully Completed \a")