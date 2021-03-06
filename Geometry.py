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
                # print(self.cellDict[i.cellID].cellID)
            self.meshList[-1].mesh += int(self.nextRegionID*1e9)
            self.meshList[-1].resetHashMap()
            self.nextRegionID += 1

        if not self.cellDict[-1] is None:
            del self.cellDict[-1]

    def findCell(self,loc):
        for i in self.meshList:
            x = 0
            y = 0
            z = 0
            while i.iEdgesFine[x] <= loc[0] and x < i.iEdgesFine.size:
                x +=1

            if x == i.iEdgesFine.size:
                print('failed')
                break
            x-=1
            while i.jEdgesFine[y] <=loc[1] and y < i.jEdgesFine.size:
                y +=1

            if y == i.jEdgesFine.size:
                print('failed')
                break
            y-=1
            while i.kEdgesFine[z] <= loc[2] and z < i.kEdgesFine.size:
                z +=1

            if z == i.kEdgesFine.size:
                print('failed')
                break
            z-=1
            return self.cellDict[i.mesh[x,y,z]]



class Geometry:
    coordSys = 'cartesian'
    mesh = []
    cellList = []
    cellMap = None
    dim = 3
    regionID = None
    internalHashMap = {-1:'Placeholder'}
    # binEdges = []
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
        else:
            self.iEdgesFine = iEdgesCoarse


        if not fineJ is None:
            self.jEdgesFine = np.array([jEdgesCoarse[0]])
            for i in range(0,jEdgesCoarse.size-1):
                self.jEdgesFine = np.hstack((self.jEdgesFine,np.linspace(jEdgesCoarse[i],jEdgesCoarse[i+1],fineJ[i]+1)[1:]))
            # print(self.jEdgesFine)
        else:
            self.jEdgesFine = jEdgesCoarse

        if not fineK is None:
            self.kEdgesFine = np.array([kEdgesCoarse[0]])
            for i in range(0,kEdgesCoarse.size-1):
                self.kEdgesFine = np.hstack((self.kEdgesFine,np.linspace(kEdgesCoarse[i],kEdgesCoarse[i+1],fineK[i]+1)[1:]))
            # print(self.kEdgesFine)
        else:
            self.kEdgesFine = iEdgesCoarse

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
                        if j==self.jEdgesFine.size-2:
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
                    # print(self.internalHashMap.keys())
        del self.internalHashMap[-1]

    # def cellSearch(self,iCoord,jCoord,kCoord):
    #     for i in range()

    def coordinateSystem(self):
        return self.coordSys

    def dimension(self):
        return self.dim

    def setMaterial(self,matList = 0):
        if isinstance(matList,int):
            for i in self.cellList:
                i.matID = matList
        elif isinstance(matList,list):
            for i in range(len(matList)):
                self.cellList[i].matID = matList[i]
        self.setNeighborMat()

    def setNeighborMat(self):
        for i in self.cellList:
            # print(i.boundaryFaces, "   ", i.cellID)
            if not i.getBoundaryFace(face=1):
                (self.internalHashMap[i.cellID+1]).neighborMat[1]=i.matID
            else:
                i.neighborMat[0]= -1

            if not i.getBoundaryFace(face=2):
                (self.internalHashMap[i.cellID-1]).neighborMat[0]=i.matID
            else:
                i.neighborMat[1]= -1

            if not i.getBoundaryFace(face=3):
                (self.internalHashMap[i.cellID+1000]).neighborMat[3]=i.matID
            else:
                i.neighborMat[2]= -1

            if not i.getBoundaryFace(face=4):
                (self.internalHashMap[i.cellID-1000]).neighborMat[2]=i.matID
            else:
                i.neighborMat[3]= -1

            if not i.getBoundaryFace(face=5):
                (self.internalHashMap[i.cellID+1000000]).neighborMat[1]=i.matID
            else:
                i.neighborMat[4]= -1

            if not i.getBoundaryFace(face=6):
                (self.internalHashMap[i.cellID-1000000]).neighborMat[0]=i.matID
            else:
                i.neighborMat[5]= -1

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
        if isinstance(face,int):
            self.boundaryFaces[face-1]=value
        else:
            raise TypeError('The function argument face must of type int.')
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
        elif isinstance(face,int):
            return self.boundaryFaces[face-1]
        return None

def doesIntersect(loc,direc,dist,p1,p2,p3):
    mat = np.ndarray((3,3))
    mat[:,0] = -dist*direc[0:3]
    mat[:,1] = p2[0:3]-p1[0:3]
    mat[:,2] = p3[0:3]-p1[0:3]

    b = loc-p1
    if np.linalg.det(mat) == 0:
        return False
    ans = np.dot(np.linalg.inv(mat),b)
    return (ans[0] > 0 and ans[0] < 1 )

def intersectionPoint(loc,direc,dist,p1,p2,p3):
    mat = np.ndarray((3,3))
    mat[:,0] = -dist*direc[0:3]
    mat[:,1] = p2[0:3]-p1[0:3]
    mat[:,2] = p3[0:3]-p1[0:3]
    b = loc-p1
    ans = np.dot(np.linalg.inv(mat),b)

    return loc+ans[0]*mat[:,0]

def getTransitDistance(p1,p2):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2+(p1[2]-p2[2])**2)**.5

if __name__=="__main__":
    a = GeometryManager()
    b = Geometry(dim=3,coordSys = 'cartesian', iLimits = (0.,5.), jLimits = (0.,1.), kLimits = (0.,1.),
                 coarseMesh=(5,2,2),fineI=[1,2,5,2,1],fineJ=[2,1],fineK=[3,2])
    print(type(b))
    b.setMaterial(14)
    # print(b.cellList)
    # main()
    print(b.mesh[3,1,0])

    a.addGeometry(b)
    print(len(a.meshList))
    print("Cell Map type :" , type(a.cellDict))
    print((a.meshList[0]).mesh[3,0,0])
    key = (a.meshList[0]).mesh[3,0,0]
    print(a.cellDict[key].cellID)
    print("Successfully completed \a")