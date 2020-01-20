# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 15:31:09 2020

@author: Michael Vander Wal
"""

import numpy as np
import Geometry
# import ParticleManager
# import Particle
# import Electron
import matplotlib.pyplot as plt
from pylab import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.ticker as tick
from matplotlib.colors import LogNorm,BoundaryNorm
from matplotlib.ticker import MaxNLocator,LogLocator
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
                flag = True
                while x < self.iEdges.size and self.iEdges[x] <= i.loc[0]:
                    x +=1
                if x == self.iEdges.size:
                    flag = False
                x-=1

                while flag and y < self.jEdges.size and self.jEdges[y] <= i.loc[1]:
                    y +=1

                if y == self.jEdges.size:
                    flag = False
                y-=1

                while flag and z < self.kEdges.size and self.kEdges[z] <= i.loc[2]:
                    z +=1

                if z == self.kEdges.size:
                    flag = False
                z-=1

                if flag:
                    self.mesh[x,y,z] += i.wgt
    # def printObjectToFile(self,fileName = "HeatMap.npy"):
    #     np.save(fileName,self)

    def printEdgesToFile(self,fileName = "HeatMapMesh.npy"):
        sep = fileName.rpartition('.')
        np.save(sep[0]+'_iMesh'+sep[1]+sep[2],self.iEdges)
        np.save(sep[0]+'_jMesh'+sep[1]+sep[2],self.jEdges)
        np.save(sep[0]+'_kMesh'+sep[1]+sep[2],self.kEdges)

    def printHeatMapToFile(self,fileName = "HeatMapResults.npy"):
        np.save(fileName,self.mesh)

    def plotPrep2D(self,projection=None,x=None,y=None,z=None):
        if projection == 'xy':
            htMp = np.zeros((self.jEdges.size-1,self.iEdges.size-1))
            for i in range(0,self.iEdges.size-1):
                for j in range(0,self.jEdges.size-1):
                    htMp[j,i] = self.mesh[i,j,:].sum()/(self.kEdges.size-1)

        elif projection == 'xz':
            htMp = np.zeros((self.kEdges.size-1,self.iEdges.size-1))
            for i in range(0,self.iEdges.size-1):
                for j in range(0,self.kEdges.size-1):
                    htMp[j,i] = self.mesh[i,:,j].sum()/(self.jEdges.size-1)

        elif projection == 'yz':
            htMp = np.zeros((self.kEdges.size-1,self.jEdges.size-1))
            for i in range(0,self.jEdges.size-1):
                for j in range(0,self.kEdges.size-1):
                    htMp[j,i] = self.mesh[:,i,j].sum()/(self.iEdges.size-1)
        else:
            return
        return htMp

    def createGraphic(self,projection = 'xy',x=None,y=None,z=None):
        """projection can be equal to '3d' , 'xy', 'yz', or 'xz' """
        if projection == 'xy' or projection == 'yz' or projection == 'xz':
            flatHeatMap = self.plotPrep2D(projection=projection,x=x,y=y,z=z)
            fig = plt.figure(figsize=(11,8.5))
            ax = fig.add_subplot(111)
            cmap = plt.get_cmap('plasma')
            if int(flatHeatMap.max()) > 100:
                nLevels = 100
            else:
                nLevels = int(flatHeatMap.max())
            # levels = MaxNLocator(nbins=100).tick_values(flatHeatMap.min(), flatHeatMap.max())
            # norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
            vlocs = LogLocator(base=10.0,subs=(1.0,2.0,5.0),numdecs=3)
#            print(vlocs.__call__())
#            return
            norm = LogNorm()
            if projection == 'xy':
                yg = ax.pcolormesh(self.iEdges,self.jEdges,flatHeatMap,cmap=cmap,norm=norm)
            elif projection == 'xz':
                yg = ax.pcolormesh(self.iEdges,self.kEdges,flatHeatMap,cmap=cmap,norm=norm)
            elif projection == 'yz':
                yg = ax.pcolormesh(self.jEdges,self.kEdges,flatHeatMap,cmap=cmap,norm=norm)

            fig.colorbar(yg, ax=ax)
            fig.tight_layout()
            plt.show()
            if projection == 'xy':
                fig.savefig('collision_heatMap_xy.png',format='png',dpi=300)
            elif projection == 'xz':
                fig.savefig('collision_heatMap_xz.png',format='png',dpi=300)
            elif projection == 'yz':
                fig.savefig('collision_heatMap_yz.png',format='png',dpi=300)
            return

        return

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