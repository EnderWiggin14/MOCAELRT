# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 19:06:28 2019

@author: Michael Vander Wal
"""


import Particle
import TransportConstants
import Electron
import Source
import Geometry
import numpy as np


class ParticleManager:

    allParticles = []
    geoManager = None
    matManager = None
    tally = None

    def __init__(self):
        return

    def addGeometry(self,geoMan):
        self.geoManager = geoMan

    def addMaterials(self,matMan):
        self.matManager = matMan

    def addTally(self,tal):
        self.tally = tal

    def addParticles(self,pType=None,nPart=None,source=None):
        if not source is None:
            self.allParticles+=source.generateParticles()
        else:
            if pType == 'electron':
                for j in range(nPart[0]):
                    self.allParticles.append(Electron.Electron(loc=[0.,0.,0.],direc=[0.,0.,1.],enrg=j+1))
            if pType == 'proton':
                pass
            if pType == 'neutron':
                pass
        self.assignParticlesToCells()

    def assignParticlesToCells(self):
        for i in self.allParticles:
            i.curCell = self.geoManager.findCell(i.loc)


    def transportParticles(self):

        if not self.tally is None:
            for i in self.allParticles:
                i.transport(self.geoManager,self.matManager)
                self.tallyParticles()
                self.cleanUpParticles()
        else:
            for i in self.allParticles:
                i.transport(self.geoManager,self.matManager)
                self.cleanUpParticles()
        return

    def tallyParticles(self):
        self.tally.score(self.allParticles)

    def cleanUpParticles(self):
        for i in self.allParticles:
            if not i.track:
                del i

def main():
    geoMan = Geometry.GeometryManager()
    partMan = ParticleManager()
    partMan.addGeometry(geoMan)
    a = Source.SourceManager()
    b = Source.Source()
    b.setLocation()
    b.setEnergy()
    b.setDirection()
    b.setParticleType()
    b.setPopulation(100)
    a.addSource(b)
    partMan.addParticles(source=a)
    print("length of list of all particles :",len(partMan.allParticles))
    print(type(partMan.allParticles[0]))
    print("Successfully completed \a")


if __name__ == '__main__':
    main()
            #physics
            #cutoff point