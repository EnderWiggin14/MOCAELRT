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
    PM = ParticleManager(['electron'],[100])
    matMan = Material.MaterialManager()
    mat = Material.Material()
    distA = Distribution.DiscreteDist()
    distB = Distribution.ContinuousDist()
    geo = Geometry.Geometry()
    geoMan = Geometry.GeometryManager()
    soMan = Source.SourceManager()
    so = Source.Source()
    return


if __name__=='__main__':
    main()
    print("Successfully completed \a")