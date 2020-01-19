# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 21:41:00 2019

@author: Michael Vander Wal
"""

import numpy as np
import Particle
from ParticleManager import *
import Electron
import Distribution
import Geometry
import Material
import Source
import DataGenerators
import TransportConstants
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
    diffXS.setDomain([0,2*np.pi])
    diffXS.setPdfData(partial(Distribution.diffElasticElectronXS,10))


    # Step 3: Add Materials
    matMan = Material.MaterialManager()
    mat = Material.Material(14)
    mat.setZNumber(10)
    mat.setElectronScatterDistribution(diffXS.sample)
    mat.setElectronTotalXSHandle(xsec.getXSection)
    matMan.addMaterial(mat)

    PM.addMaterials(matMan)
    # Step 4: Add Geometry
    geoMan = Geometry.GeometryManager()
    geo = Geometry.Geometry()
    geo.setMaterial(14)
    geoMan.addGeometry(geo)

    PM.addGeometry(geoMan)
    # print(PM.matManager.matDict[14].zNumber)

    # Step 5: Add Source Particles
    soMan = Source.SourceManager()
    so = Source.Source()
    so.setLocation()
    so.setEnergy()
    so.setDirection(np.array([1.,0.,0.]))
    so.setParticleType()
    so.setPopulation()
    soMan.addSource(so)

    PM.addParticles(source = soMan)

    # Step 6: Create and add Tally
    tal = Tally.HeatMap(geo)
    PM.addTally(tal)

    PM.transportParticles()

    return


if __name__=='__main__':
    main()
    print("Successfully completed \a")