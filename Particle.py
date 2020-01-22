# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 18:45:54 2019

@author: Michael Vander Wal
"""


import numpy as np
import TransportConstants as TC
import abc
import Geometry

dummyDirection = np.array([0.,0.,1.])

class Particle(metaclass=abc.ABCMeta):
    particleType = None
    loc = None
    prevLoc = None
    direc = None
    E = None
    deltaE = None
    wgt = None
    ID = -1
    track = True
    matID = None
    curCell = None
    newWgt = 1.

    def __init__(self,species='electron',loc = [0.,0.,0.], direc = [0.,0.,1.], enrg = 100.,pid = -1):
        if isinstance(species,str):
            self.particleType = self.enumMap(species)
        else:
            self.particleType = species
        self.loc = np.array(loc)
        self.direc = np.array(direc)
        self.E = self.energyConvert(enrg)
        self.wgt = 1.
        self.ID = pid
        return

    def enumMap(self,toMap):
        switch={
                "electron": 0,
                "proton"  : 1,
                "neutron" : 2
                }

        return switch.get(toMap,'Invalid Particle')

    def getDirection(self):
        return self.direc

    def getLocation(self):
        return self.loc

    def getEnergy(self,unit ='eV'):
        if unit == 'eV':
            return self.E/TC._eV_Erg
        elif unit == 'ergs':
            return self.E
        else:
            raise Exception("Invalid option for function argument \'unit.\'")

    def getWeight(self):
        return self.wgt

    def getID(self):
        return self.ID

    def energyConvert(self,enrg):
        return enrg*TC._eV_Erg

    def setLocation(self,loc):
        self.loc = loc

    def setEnergy(self,energy):
        self.E = energy

    def setWeight(self,weight):
        self.wgt = weight

    def transport(self,geoManager,matManager):

        distance = self.sampleCollisionDistance(matManager)
        newLoc = self.intersectionHandler(self.loc,distance,geoManager)
        self.prevLoc = self.loc
        self.loc = newLoc
        # will need to add an energy update step for inelastic scattering
        self.matID = self.getMaterial()
        scatterAngle, weight, deltaEnergy, energyWeight = self.sampleScatterAngle(matManager)
        gammaAngle = np.random.uniform(0,np.pi)
        self.direc = getNewDirection(scatterAngle,gammaAngle,self.direc)
        self.deltaE = deltaEnergy
        self.E -= deltaEnergy
        self.wgt = self.newWgt
        self.newWgt = self.wgt*weight
        return

    def intersectionHandler(self,initLoc,distance,geoManager):
        flag = False
        while distance > 0:
            """Check for intersection with edges of cell"""
            if flag:
                distance = self.sampleCollisionDistance(self.getCrossSection())
                flag = False

            # Giving alternative name to curCell to decrease length of lines
            cell = self.getCurrentCell()
            p1 = np.array([cell.iBounds[1],cell.jBounds[1],cell.kBounds[0]])
            p2 = np.array([cell.iBounds[1],cell.jBounds[0],cell.kBounds[0]])
            p3 = np.array([cell.iBounds[1],cell.jBounds[0],cell.kBounds[1]])
            p4 = np.array([cell.iBounds[1],cell.jBounds[1],cell.kBounds[1]])
            p5 = np.array([cell.iBounds[0],cell.jBounds[1],cell.kBounds[0]])
            p6 = np.array([cell.iBounds[0],cell.jBounds[0],cell.kBounds[0]])
            p7 = np.array([cell.iBounds[0],cell.jBounds[1],cell.kBounds[1]])
            if Geometry.doesIntersect(initLoc,self.direc,distance,p1,p2,p4):# + i direction
                if cell.matID == cell.neighborMat[0]:
                    tempLoc = Geometry.intersectionPoint(initLoc,self.direc,distance,p1,p2,p4)
                    distance = distance - Geometry.getTransitDistance(initLoc,tempLoc)
                    self.curCell = geoManager.cellDict[self.curCell.cellID+1]
                elif cell.neighborMat[0] == -1:
                    # print("Leaving the trackable area")
                    # tempLoc = Geometry.intersectionPoint(initLoc,self.direc,distance,p1,p2,p4)
                    tempLoc = distance*self.direc+initLoc
                    self.track=False
                    break
                else:
                    flag = True

            elif Geometry.doesIntersect(initLoc,self.direc,distance,p5,p6,p7):# - i direction
                if cell.matID == cell.neighborMat[1]:
                    tempLoc = Geometry.intersectionPoint(self.loc,self.direc,distance,p5,p6,p7)
                    distance = distance - Geometry.getTransitDistance(initLoc,tempLoc)
                    self.curCell = geoManager.cellDict[self.curCell.cellID-1]
                elif cell.neighborMat[1] == -1:
                    # print("Leaving the trackable area")
                    # tempLoc = Geometry.intersectionPoint(self.loc,self.direc,distance,p5,p6,p7)
                    tempLoc = distance*self.direc+initLoc
                    self.track=False
                    break
                else:
                    flag = True

            elif Geometry.doesIntersect(initLoc,self.direc,distance,p1,p4,p5):# + j direction
                if cell.matID == cell.neighborMat[2]:
                    tempLoc = Geometry.intersectionPoint(self.loc,self.direc,distance,p1,p4,p5)
                    distance = distance - Geometry.getTransitDistance(initLoc,tempLoc)
                    self.curCell = geoManager.cellDict[self.curCell.cellID+1000]
                elif cell.neighborMat[2] == -1:
                    # print("Leaving the trackable area")
                    # tempLoc = Geometry.intersectionPoint(self.loc,self.direc,distance,p1,p4,p5)
                    tempLoc = distance*self.direc+initLoc
                    self.track=False
                    break
                else:
                    flag = True

            elif Geometry.doesIntersect(initLoc,self.direc,distance,p2,p6,p3):# - j direction
                if cell.matID == cell.neighborMat[3]:
                    tempLoc = Geometry.intersectionPoint(self.loc,self.direc,distance,p2,p6,p3)
                    distance = distance - Geometry.getTransitDistance(initLoc,tempLoc)
                    self.curCell = geoManager.cellDict[self.curCell.cellID-1000]
                elif cell.neighborMat[3] == -1:
                    # print("Leaving the trackable area")
                    # tempLoc = Geometry.intersectionPoint(self.loc,self.direc,distance,p2,p6,p3)
                    tempLoc = distance*self.direc+initLoc
                    self.track=False
                    break
                else:
                    flag = True

            elif Geometry.doesIntersect(initLoc,self.direc,distance,p1,p2,p5):# + k direction
                if cell.matID == cell.neighborMat[4]:
                    tempLoc = Geometry.intersectionPoint(self.loc,self.direc,distance,p1,p2,p5)
                    distance = distance - Geometry.getTransitDistance(initLoc,tempLoc)
                    self.curCell = geoManager.cellDict[self.curCell.cellID+1000000]
                elif cell.neighborMat[4] == -1:
                    # print("Leaving the trackable area")
                    # tempLoc = Geometry.intersectionPoint(self.loc,self.direc,distance,p1,p2,p5)
                    tempLoc = distance*self.direc+initLoc
                    self.track=False
                    break
                else:
                    flag = True

            elif Geometry.doesIntersect(initLoc,self.direc,distance,p3,p4,p7):# - k direction
                if cell.matID == cell.neighborMat[5]:
                    tempLoc = Geometry.intersectionPoint(self.loc,self.direc,distance,p3,p4,p7)
                    distance = distance - Geometry.getTransitDistance(initLoc,tempLoc)
                    self.curCell = geoManager.cellDict[self.curCell.cellID-1000000]
                elif cell.neighborMat[5] == -1:
                    # print("Leaving the trackable area")
                    # tempLoc = Geometry.intersectionPoint(self.loc,self.direc,distance,p3,p4,p7)
                    tempLoc = distance*self.direc+initLoc
                    self.track=False
                    break
                else:
                    flag = True
            else:
                tempLoc = distance*self.direc+self.loc
                distance = 0

            initLoc = tempLoc
            # print("New Location  :  ",tempLoc)


        return tempLoc



    def getCurrentCell(self):
        return self.curCell

    def getMaterial(self):
        return self.curCell.matID

    def getCrossSection(self):
        return self.matID.xs(self.E)


    @abc.abstractmethod
    def getVelocity(self):
        pass

    @abc.abstractmethod
    def sampleCollisionDistance(self):
        pass

    @abc.abstractmethod
    def sampleScatterAngle(self):
        pass


def getNewDirection(scatterAngle,gammaAngle,initDir):
    v = np.cross(a = initDir, b = dummyDirection)
    d = np.dot(initDir,dummyDirection)
    vSkew = np.array([[ 0., -v[2], v[1]],
                      [ v[2], 0., -v[0]],
                      [ -v[1], v[0], 0.]])
    R = np.identity(3)+vSkew+np.dot(vSkew,vSkew)*(1/(1+d))
    invR = np.linalg.inv(R)
    directionOperator = np.array([np.sin(scatterAngle)*np.cos(gammaAngle),
                                  np.sin(scatterAngle)*np.sin(gammaAngle),
                                  np.cos(scatterAngle)])
    newDirection = np.dot(invR,directionOperator)
    return newDirection

def materialChange(curCell,targCell,geoManager):
    return geoManager.cellDict[curCell].matID == geoManager.cellDict[targCell].matID

# if __name__ == "__main__":
#     p = Particle()
#     print(p.enumMap('electron'))