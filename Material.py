# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 10:08:24 2019

@author: Michael Vander Wal
"""
import numpy as np
import Distribution


class MaterialManager():
    matDict = {-1,'placeHolder'}
    def __init__(self):
        return

    def addMaterial(self,mat):
        if self.matDict[mat.matID] is None:
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
    name = None
    atomicDensity = 1.0
    def __init__(self,matID,angleDistHandle,totalCrossHandle):
        self.matID = matID
        self.diffCrossHandle = angleDistHandle
        self.totalCrossHandle = totalCrossHandle
        self.setName()
        return
    def composition(self):
        return self.comp

    def setName(self,name=None):
        if name is None:
            self.name=str(self.matID)
        else:
            self.name = name

    def setComposition(self,comp):
        # format is [ [z-IDs] , [number density] ]
        assert len(comp[0])==len(comp[1]), "The number z-IDs must math the number of atomic percentages"

        self.comp = comp

    def sampleElectronXS(self,energy):
         return self.totalCrossHandle(energy)

    def sampleElectronScatterAngle(self,energy):
        return self.diffCrossHandle(energy)



if __name__=="__main__":
    print("Successfully completed \a")