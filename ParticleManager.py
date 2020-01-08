# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 19:06:28 2019

@author: Michael Vander Wal
"""


import Particle
import TransportConstants
import Electron
import Source
import numpy as np


class ParticleManager:

    allParticles = []
    geoManager = None

    def __init__(self,geoMan):
        self.geoManager = geoMan
        return

    def addParticles(self,pType,nPart,source=None):
        if source is None:
            self.allParticles+=source.generateParticles()
        else:
            if pType == 'electron':
                for j in range(nPart[0]):
                    self.allParticles.append(Electron.Electron(loc=[0.,0.,0.],direc=[0.,0.,1.],enrg=j+1))
            if pType == 'proton':
                pass
            if pType == 'neutron':
                pass


    def transportParticles(self):
        for i in self.allParticles:
            i.transport(self.geoManager)
        return


def main():
    partMan = ParticleManager()
    return


if __name__ == '__main__':
    main()
            #physics
            #cutoff point