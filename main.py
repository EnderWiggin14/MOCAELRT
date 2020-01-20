# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 21:41:00 2019

@author: Michael Vander Wal
"""

import numpy as np
# import Particle
from ParticleManager import *
# import Electron
import Distribution
import Geometry
import Material
import Source
import DataGenerators
import TransportConstants as TC
import XSections
import Tally
from functools import partial




def main():
    # Step 1: Initialize ParticleManager
    PM = ParticleManager()

    # Step 2: Generate Data
    # This step will hopefully not be explicityly needed in the future
    totalXS,scatterXS = DataGenerators.generateElasticElectronData(10)
    xsec = XSections.XSection(totalXS[1],totalXS[0])
    diffXS = Distribution.Distribution()
    diffXS.setDomain([-np.pi,np.pi])
    diffXS.setPdfData(partial(Distribution.diffElasticElectronXS,10))

    # Step 3: Add Materials
    matMan = Material.MaterialManager()
    mat = Material.Material(14)
    mat.setZNumber(10)
    mat.setAtomicDensity(1.0*(1/18.01)*TC._nAvogad)
    mat.setElectronScatterDistribution(diffXS.sample)
    mat.setElectronTotalXSHandle(xsec.getXSection)
    matMan.addMaterial(mat)

    PM.addMaterials(matMan)
    # Step 4: Add Geometry
    geoMan = Geometry.GeometryManager()
    geo = Geometry.Geometry(dim=3,coordSys = 'cartesian', iLimits = (-1e-5,1e-5), jLimits = (-1e-5,1e-5), kLimits = (0,1e-5), coarseMesh=(1,1,1),fineI=[100],fineJ=[100],fineK=[100])
    geo.setMaterial(14)
    geoMan.addGeometry(geo)

    PM.addGeometry(geoMan)
    # print(PM.matManager.matDict[14].zNumber)

    # Step 5: Add Source Particles
    soMan = Source.SourceManager()
    so = Source.Source()
    so.setLocation()
    so.setEnergy(1000)
    so.setDirection(np.array([0.,0.,1.]))
    so.setParticleType()
    so.setPopulation(1000)
    soMan.addSource(so)

    PM.addParticles(source = soMan)

    # Step 6: Create and add Tally
    tal = Tally.HeatMap(geo)
    PM.addTally(tal)

    PM.transportParticles()

    tal.createGraphic(projection = 'xy')
    tal.createGraphic(projection = 'yz')
    tal.createGraphic(projection = 'xz')
    tal.printEdgesToFile()
    tal.printHeatMapToFile()

    return


if __name__=='__main__':
    main()
    print("Successfully completed \a")