# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 15:31:09 2020

@author: Michael Vander Wal
"""

import numpy as np
import Geometry
import ParticleManager
import Particle
import Electron
import abc


class TallyManager():



    def __init__(self):
        return



class Tally(metaclass=abc.ABCMeta):
    # might want to use binary sort on non-uniform meshes as opposed to using algebraic indexing
    data = None
    mesh = None
    iEdges = None
    jEdges = None
    kEdges = None
    xMin = None # may end up being a list or ndarray for variable division sizes
    xMax = None
    yMin = None
    yMax = None
    zMin = None
    zMax = None
    unifDivSizes = [] # will be used if uniform == True
    varDivSizes = None # will be used if uniform == False
    uniform = None # will be true or false

    def __init__(self,mesh,uniform):
        if isinstance(mesh,Geometry.Geometry):
            self.mesh = mesh # preferably a Geometry class object
            self.uniform = uniform
            self.xMin = mesh.iEdgesFine[0]
            self.xMax = mesh.iEdgesFine[-1]
            self.yMin = mesh.jEdgesFine[0]
            self.yMax = mesh.jEdgesFine[-1]
            self.zMin = mesh.kEdgesFine[0]
            self.zMax = mesh.kEdgesFine[-1]
            self.iEdges = mesh.iEdgesFine
            self.jEdges = mesh.jEdgesFine
            self.kEdges = mesh.kEdgesFine
            self.mesh = np.zeros((self.iEdges.size-1,self.jEdges.size-1,self.kEdges.size-1))
        else:
            raise TypeError("The mesh type currently supported is a Geometry Object.")
        return

    def generateTallyMesh(self):
        return

    @abc.abstractmethod
    def score(self):
        pass


class HeatMap(Tally):

    def __init__(self,mesh = None,uniform = False):
        Tally.__init__(self,mesh,uniform)

    def score(self,particleList):
        if self.uniform:
            invXDivSize = 1/self.unifDivSizes[0]
            invYDivSize = 1/self.unifDivSizes[1]
            invZDivSize = 1/self.unifDivSizes[2]
            for i in particleList:
                if i.loc[0] >= self.xMin and i.loc[0] <= self.xMax and i.loc[1] >= self.yMin and i.loc[1] <= self.yMax and i.loc[2] >= self.zMin and i.loc[2] <= self.zMax:
                    x = int((i.loc[0]-self.xMin)*invXDivSize)
                    y = int((i.loc[1]-self.yMin)*invYDivSize)
                    z = int((i.loc[2]-self.zMin)*invZDivSize)
                    self.mesh[x,y,z] = i.wgt
        else:
            for i in particleList:
                x = 0
                y = 0
                z = 0
                while self.iEdges[x] <= i.loc[0] and x < self.iEdges.size:
                    x +=1

                if x == self.iEdges.size:
                    print('failed')
                    break
                x-=1
                while self.jEdges[y] <=i.loc[1] and y < self.jEdges.size:
                    y +=1

                if y == self.jEdges.size:
                    print('failed')
                    break
                y-=1
                while self.kEdges[z] <= i.loc[2] and z < self.kEdges.size:
                    z +=1

                if z == self.kEdges.size:
                    print('failed')
                    break
                z-=1


class TrackLength(Tally):

    def __init__(self):
        Tally.__init__(self)

    def score(self):
        return

def main():
    a = Geometry.Geometry()
    b = HeatMap(a)
    print(type(b))
    print("Successfully completed \a")


if __name__ == "__main__":
    main()