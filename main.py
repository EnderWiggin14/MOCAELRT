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
import TransportConstants




def main():
    # Step 1: Initialize ParticleManager
    PM = ParticleManager()

    # Step 2: Generate Distributions

    # Step 2: Add Materials
    matMan = Material.MaterialManager()
    mat = Material.Material(14)

    # Step 3: Add Geometry
    geoMan = Geometry.GeometryManager()
    geo = Geometry.Geometry()
    geoMan.addGeometry(geo)

    PM.addGeometry(geoMan)

    # Step 4: Add Source Particles
    soMan = Source.SourceManager()
    so = Source.Source()
    so.setLocation()
    so.setEnergy()
    so.setDirection()
    so.setParticleType()
    so.setPopulation()
    soMan.addSource(so)

    PM.addParticles(source = soMan)




    return


if __name__=='__main__':
    main()
    print("Successfully completed \a")