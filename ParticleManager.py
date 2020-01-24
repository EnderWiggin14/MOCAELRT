# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 19:06:28 2019

@author: Michael Vander Wal
"""

import Electron
import Source
import Geometry
import TransportConstants as TC


class ParticleManager:

    allParticles = []
    geoManager = None
    matManager = None
    tally = None
    iterationLimit = 10

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

    def setIterationLimit(self, limit = 10):
        self.iterationLimit = limit

    def transportParticles(self):
        j=0
        if not self.tally is None:
            while len(self.allParticles)>0 and j < self.iterationLimit:
                print("Loop iteration : ", j, "-- Particles Left : ",len(self.allParticles))
                for i in self.allParticles:
                    i.transport(self.geoManager,self.matManager)
                self.tallyParticles()
                self.cleanUpParticles()
                j +=1
        else:
            while len(self.allParticle) > 0 and j < self.iterationLimit:
                for i in self.allParticles:
                    i.transport(self.geoManager,self.matManager)
                self.cleanUpParticles()
                j+=1
        return

    def tallyParticles(self):
        self.tally.score(self.allParticles)

    def cleanUpParticles(self):
        limit = len(self.allParticles)
        i=0
        while i < limit:
            if not self.allParticles[i].track or self.allParticles[i].E < 30*TC._eV_Erg:
                del self.allParticles[i]
                limit -= 1
            else:
                i+=1

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