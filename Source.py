   # -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 11:34:53 2019

@author: Michael Vander Wal
"""
import numpy as np
import Particle
import Electron

class SourceManager():
    sourceList = None
    def __init__(self):
        return

    def addSource(self,source):
        self.sourceList.append(source)

    def generateParticles(self):
        particles = []
        for i in self.sourceList:
                if i.particle == "electron":
                    for j in range(i.population):
                        particles.append(Electron.Electron(loc=i.locationGenerator(),direc=i.directionGenerator,enrg=i.energyGenerator()))

        return particles

class Source():
    sourceType = 'point'
    sourceLocation = None
    sourceDirection = None
    population = None
    particle = "electron"
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

    def setPopulation(self, population=10):
        self.population = population

    def setParticleType(self,particleType = 'electron'):
        self.partice = particleType

    def setEnergy(self,energy=1000):
        self.E = energy

    def energyGenerator(self):
        if type(self.E) == 'int' or type(self.E) == 'float':
            return self.E
        elif type(self.E) == 'str':
            return self.E # temporary value, itended to be used for distributions

if __name__=="__main__":
    a = SourceManager()
    b = Source()
    b.setLocation()
    b.setEnergy()
    b.setDirection()
    print(b.sourceType, '\t', b.sourceLocation,'\t',b.sourceDirection,'\t',b.E)
    print("Successfully Completed \a")