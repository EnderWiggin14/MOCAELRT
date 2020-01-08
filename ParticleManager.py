# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 19:06:28 2019

@author: Michael Vander Wal
"""


import Particle
import TransportConstants
import Electron
import numpy as np


class ParticleManager:

    nParticles = None
    allParticles = []
    geoManager = None

    def __init__(self,geoMan,types = ['electron'],nPart = [1]):
        self.nParticles = sum(nPart)
        self.geoManager = geoMan
        for i in types:
            if i == 'electron':
                for j in range(nPart[0]):
                    self.allParticles.append(Electron.Electron(loc=[0.,0.,0.],direc=[0.,0.,1.],enrg=j+1))
            if i == 'proton':
                pass
            if i == 'neutron':
                pass

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


            #physics
            #cutoff point