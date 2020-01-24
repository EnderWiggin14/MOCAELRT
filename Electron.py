# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 19:04:56 2019

@author: Michael Vander Wal
"""

from Particle import *
# import Particle
import TransportConstants as TC
import numpy as np
import Distribution

class Electron(Particle):
# class Electron(Particle.Particle):

    def __init__(self, loc = [0.,0.,0.], direc = [0.,0.,1.], enrg = 100.,pid = np.random.randint(0,9999999) ):
        Particle.__init__(self,'electron',loc,direc,enrg)
        return

    def energyConvert(self,enrg):
        return enrg*TC._eV_Erg

    def getVelocity(self):
        return TC._c*(1-((self.E/(TC._eMass*TC._c**2))+1)**(-2))**.5

    def sampleCollisionDistance(self,matMan):
        # mfpInv = (self.matID.atomicDensity)/self.xs
        mat = matMan.matDict[self.getMaterial()]
        # mfpInv = mat.atomicDensity*mat.sampleElectronXS(self.getEnergy())
        mfpInv = mat.atomicDensity*mat.sampleElectronXS(self.E)
        return Distribution.exponential(1/mfpInv)

    def sampleScatterAngle(self,matMan):
        # return Distribution.ElasticElectron(self.E)
        # print("______E_______ ",self.E)
        angle, locationWeight, deltaEnergy = matMan.matDict[self.matID].sampleElectronScatterAngle(self.E)
        return angle, locationWeight, deltaEnergy




if __name__=="__main__":
    p = Electron()
    print(p.getEnergy())
    print(p.getVelocity())
    # print(TC._eMass)