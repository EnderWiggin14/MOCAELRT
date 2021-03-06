# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 10:08:24 2019

@author: Michael Vander Wal
"""


"""
Need to add a getMeanFreePath function to add increased abstraction/separation of tasks
"""
import numpy as np
import TransportConstants as TC
# import Distribution
# import DataGenerators
# import XSections


class MaterialManager():
    matDict = {-1:'placeHolder'}
    def __init__(self):
        return

    def addMaterial(self,mat):
        if not mat.matID in self.matDict.keys():
            self.matDict[mat.matID] = mat

            if not self.matDict[-1] is None:
                del self.matDict[-1]
        else:
            raise Exception("Duplicate material ID.")



class Material():
    comp = []
    matID = None
    electronDiffCrossHandle = None
    electronTotalCrossHandle = None
    electronElasticCrossHandle = None
    electronIonizationCrossHandle = None
    electronEnergyLossHandle = None
    name = None
    zNumber = None
    atomicDensity = 1.0
    electronPhysics = "elastic"
    def __init__(self,matID):
        self.matID = matID
        return

    def setElectronScatterDistribution(self,handle):
        self.diffCrossHandle = handle

    def setElectronTotalXSHandle(self,handle):
        self.electronTotalCrossHandle = handle

    def setElectronElasticXSHandle(self,handle):
        self.electronElasticCrossHandle = handle

    def setElectronIonizationXSHandle(self,handle):
        self.electronIonizationCrossHandle = handle

    def setElectronEnergyLossHandle(self,handle):
        self.electronEnergyLossHandle = handle

    def getComposition(self):
        return self.comp

    def setName(self,name=None):
        if name is None:
            self.name=str(self.matID)
        else:
            self.name = name

    def setZNumber(self,z):
        self.zNumber = z

    def setComposition(self,comp):
        # format is [ [z-IDs] , [number density] ]
        assert len(comp[0])==len(comp[1]), "The number z-IDs must math the number of atomic percentages"

        self.comp = comp

    def setAtomicDensity(self,density):
        self.atomicDensity = density

    def sampleElectronXS(self,energy):
        if self.electronPhysics == "inelastic":
            ionXS = self.electronIonizationCrossHandle(energy)
            elastXS = self.electronElasticCrossHandle(energy)
            return ionXS + elastXS
        else:
            return self.electronElasticCrossHandle(energy)

    def setElectronPhysics(self,physics = 'elastic'):
        self.electronPhysics = physics

    def sampleElectronEnergyLoss(self,energy):
        return self.electronEnergyLossHandle(energy)


    def sampleElectronScatterAngle(self,energy):
        elastXS = self.electronElasticCrossHandle(energy)
        ionXS = self.electronIonizationCrossHandle(energy)
        # print("ionXS  : ",ionXS)
        totalCross = ionXS + elastXS
        deltaEnergy = 0.
        energyWeight = 1.
        if self.electronPhysics == "inelastic":
            u = np.random.uniform(0.,1.)

            if u <= ionXS/totalCross:
                deltaEnergy,energyWeight = self.electronEnergyLossHandle([energy])
                # print("sampling for energy loss :: ",deltaEnergy/energy)
                energyWeight = energyWeight/totalCross
            else:
                deltaEnergy = 0.
                energyWeight = 1.
        angle, locationWeight = self.diffCrossHandle([energy])
        locationWeight = locationWeight/totalCross*energyWeight
        return angle, locationWeight, deltaEnergy




if __name__=="__main__":
    print("Successfully completed \a")