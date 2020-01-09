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
    testType = None


    def __init__(self):
        return

    @abc.abstractmethod
    def score(self):
        pass

class HeatMap(Tally):

    def __init__(self):
        Tally.__init__(self)

    def score(self):
        return


def main():
    return


if __name__ == "__main__":
    main()