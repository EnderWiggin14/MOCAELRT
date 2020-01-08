# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 10:45:49 2019

@author: Michael Vander Wal
"""
import numpy as np
class GeometryManager():
    meshList = []
    namedMeshes = []
    nextRegionID = 1
    cellDict = {-1:'Placeholder'}

    def __init__(self):
        return

    def addGeometry(self,geo):
        if isinstance(geo,Geometry):
            self.meshList.append(geo)
            self.meshList[-1].regionID = self.nextRegionID
            for i in self.meshList[-1].cellList:
                i.cellID = int(i.cellID+self.nextRegionID*1e9)
                self.cellDict[i.cellID] = i
                print(self.cellDict[i.cellID].cellID)
            self.meshList[-1].mesh += int(self.nextRegionID*1e9)
            self.meshList[-1].resetHashMap()
            self.nextRegionID += 1

        if not self.cellDict[-1] is None:
            del self.cellDict[-1]




class Geometry:
    coordSys = 'cartesian'
    mesh = []
    cellList = []
    cellMap = None
    dim = 3
    regionID = None
    internalHashMap = {-1:'Placeholder'}
    binEdges = []
    iEdgesFine = None
    jEdgesFine = None
    kEdgesFine = None
    def __init__(self,dim=3,coordSys = 'cartesian', iLimits = (0.,1.), jLimits = (0.,1.), kLimits = (0.,1.), coarseMesh=(1,1,1),fineI=None,fineJ=None,fineK=None):
        self.coordSys = coordSys
        self.dim = dim
        iEdgesCoarse = np.linspace(iLimits[0],iLimits[1],coarseMesh[0]+1)
        jEdgesCoarse = np.linspace(jLimits[0],jLimits[1],coarseMesh[1]+1)
        kEdgesCoarse = np.linspace(kLimits[0],kLimits[1],coarseMesh[2]+1)

        if not fineI is None:
            #this is here just to get folding
            self.iEdgesFine = np.array([iEdgesCoarse[0]])
            for i in range(0,iEdgesCoarse.size-1):
                self.iEdgesFine = np.hstack((self.iEdgesFine,np.linspace(iEdgesCoarse[i],iEdgesCoarse[i+1],fineI[i]+1)[1:]))
            # print(self.iEdgesFine)

        if not fineJ is None:
            self.jEdgesFine = np.array([jEdgesCoarse[0]])
            for i in range(0,jEdgesCoarse.size-1):
                self.jEdgesFine = np.hstack((self.jEdgesFine,np.linspace(jEdgesCoarse[i],jEdgesCoarse[i+1],fineJ[i]+1)[1:]))
            # print(self.jEdgesFine)

        if not fineK is None:
            self.kEdgesFine = np.array([kEdgesCoarse[0]])
            for i in range(0,kEdgesCoarse.size-1):
                self.kEdgesFine = np.hstack((self.kEdgesFine,np.linspace(kEdgesCoarse[i],kEdgesCoarse[i+1],fineK[i]+1)[1:]))
            # print(self.kEdgesFine)
        # self.makeCellList()
        self.mesh = np.zeros((self.iEdgesFine.size-1,self.jEdgesFine.size-1,self.kEdgesFine.size-1),dtype='longlong')
        self.makeCellMap()
        return

    def makeCellMap(self):
        for k in range(0,self.kEdgesFine.size-1):
            for j in range(0,self.jEdgesFine.size-1):
                for i in range(0,self.iEdgesFine.size-1):
                    self.cellList.append(Cell(self.iEdgesFine[i:i+2],self.jEdgesFine[j:j+2],self.kEdgesFine[k:k+2]))

                    if self.coordSys == 'cartesian':
                        if i==self.iEdgesFine.size-2:
                            self.cellList[-1].setBoundaryFace(face=1)
                        if i==0:
                            self.cellList[-1].setBoundaryFace(face=2)
                        if j==self.iEdgesFine.size-2:
                            self.cellList[-1].setBoundaryFace(face=3)
                        if j==0:
                            self.cellList[-1].setBoundaryFace(face=4)
                        if k==self.kEdgesFine.size-2:
                            self.cellList[-1].setBoundaryFace(face=5)
                        if k==0:
                            self.cellList[-1].setBoundaryFace(face=6)

                    self.cellList[-1].cellID = int(i+j*1e3+k*1e6+1e11)
                    self.mesh[i,j,k] = self.cellList[-1].cellID
                    self.internalHashMap[self.cellList[-1].cellID]=self.cellList[-1]
        del self.internalHashMap[-1]

    # def cellSearch(self,iCoord,jCoord,kCoord):
    #     for i in range()

    def coordinateSystem(self):
        return self.coordSys

    def dimension(self):
        return self.dim

    def setMaterial(self,matList = 0):
        if type(matList) == 'int':
            for i in self.cellList:
                i.matID = matList
        elif type(matList) == 'list':
            for i in range(len(matList)):
                self.cellList[i].matID = matList[i]
        self.setNeighborMat()

    def setNeighborMat(self):
        for i in self.cellList:
            if not i.getBoundaryFace(face=1):
                (self.internalHashMap[i.cellID+1]).neighborMat[1]=i.matID
            else:
                i.neighborMat[0]=None

            if not i.getBoundaryFace(face=2):
                (self.internalHashMap[i.cellID-1]).neighborMat[0]=i.matID
            else:
                i.neighborMat[1]=None

            if not i.getBoundaryFace(face=3):
                (self.internalHashMap[i.cellID+1000]).neighborMat[3]=i.matID
            else:
                i.neighborMat[2]=None

            if not i.getBoundaryFace(face=4):
                (self.internalHashMap[i.cellID-1000]).neighborMat[2]=i.matID
            else:
                i.neighborMat[3]=None

            if not i.getBoundaryFace(face=5):
                (self.internalHashMap[i.cellID+1000000]).neighborMat[1]=i.matID
            else:
                i.neighborMat[4]=None

            if not i.getBoundaryFace(face=6):
                (self.internalHashMap[i.cellID-1000000]).neighborMat[0]=i.matID
            else:
                i.neighborMat[5]=None

    def  resetHashMap(self):
        A = {v.cellID:v for i,v in enumerate(self.internalHashMap.values())}
        self.internalHashMap = A
        # B = {i: v for i, v in enumerate(A.values())}


class Cell():
    cellID = None
    iBounds = np.array([0.,0.])
    jBounds = np.array([0.,0.])
    kBounds = np.array([0.,0.])
    boundaryFaces = [False,False,False,False,False,False]
    matID = None
    neighborMat = np.array([0,0,0,0,0,0])
    def __init__(self,i,j,k):
        self.iBounds[0] = i[0]
        self.iBounds[1] = i[1]
        self.jBounds[0] = j[0]
        self.jBounds[1] = j[1]
        self.kBounds[0] = k[0]
        self.kBounds[1] = k[1]
        # print(self.getBounds())
        # print(self.getIBounds())
        return
    def getMatID(self):
        return self.matID
    def getBounds(self):
        return np.hstack((self.iBounds,self.jBounds,self.kBounds))
    def getIBounds(self):
        return self.iBounds
    def getJBounds(self):
        return self.jBounds
    def getKBounds(self):
        return self.kBounds
    def setBoundaryFace(self,face = None,value = True):
        if not face is None:
            self.boundaryFaces[face-1]=value
        return
    def getBoundaryFace(self,face = None,output = "indices"):
        if face is None:
            if output == "indices":
                indices = []
                for i in range(0,len(self.boundaryFaces)):
                    if self.boundaryFaces[i]:
                        indices.append(i)
                return indices
            elif output =="values":
                return self.boundaryFaces
            else:
                return None
        elif type(face) == 'int':
            return self.boundaryFaces[face-1]
        return None

def doesIntersect(loc,direc,dist,p1,p2,p3):
    mat = np.ndarray((3,3))
    mat[:,0] = -dist*direc[0:3]
    mat[:,1] = p2[0:3]-p1[0:3]
    mat[:,2] = p3[0:3]-p1[0:3]
    b = loc-p1
    ans = np.lingalg.inv(mat)*b

    return (ans[0] > 0 and ans[0] < 1 )

def intersectionPoint(loc,direc,dist,p1,p2,p3):
    mat = np.ndarray((3,3))
    mat[:,0] = -dist*direc[0:3]
    mat[:,1] = p2[0:3]-p1[0:3]
    mat[:,2] = p3[0:3]-p1[0:3]
    b = loc-p1
    ans = np.lingalg.inv(mat)*b

    return loc+ans[0]*mat[:,0]

def getTransitDistance(p1,p2):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2+(p1[2]-p2[2])**2)**.5

if __name__=="__main__":
    a = GeometryManager()
    b = Geometry(dim=3,coordSys = 'cartesian', iLimits = (0.,5.), jLimits = (0.,1.), kLimits = (0.,1.),
                 coarseMesh=(5,1,1),fineI=[1,2,5,2,1],fineJ=[2],fineK=[3])
    print(type(b))
    # print(b.cellList)
    # main()
    print(b.mesh[3,1,0])
    a.addGeometry(b)
    print(len(a.meshList))
    print((a.meshList[0]).mesh[3,0,0])
    key = (a.meshList[0]).mesh[3,0,0]
    print(a.cellDict[key].cellID)
    print("Successfully completed \a")