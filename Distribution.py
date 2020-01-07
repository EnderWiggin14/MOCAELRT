# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 10:28:56 2019

@author: Michael Vander Wal
"""
import numpy as np
import abc


"""Create hash table directory for distributions"""

class Distribution(metaclass=abc.ABCMeta):
    name = "unnamed"
    dist = None
    def __init__(self):
        return

    def setDiscreteDifferential(self,func=None):
        if func is None:
            print("error handling needs to be added")
            return
        self.diffCont = func
        return

    def setContinuousDistribution(self,func=None):
        if func is None:
            print("error handling needs to be added")
            return
        self.distCont = func
        return

    def getName(self):
        return self.name

    @abc.abstractmethod
    def sample(self):
        pass

class DiscreteDist(metaclass=abc.ABCMeta):

    def __init__(self):
        Distribution.__init__(self)
        return

    def sample(self,x):
        print("Need to add sample method")
        return;

class ContinuousDist(metaclass=abc.ABCMeta):
    direct = True
    pdfCoefs = None
    cdfCoefs = None
    inv = None
    def __init__(self,inv=None):
        Distribution.__init__(self)
        self.inv = inv
        return

    @abc.abstractmethod
    def sample(self):
        pass



    def invCdf(self,x):
        if not self.inv is None:
            return self.inv(self,x)
        return 0


class Normal(Distribution):
    sigma = 1
    mean = 0
    def __init__(self,mean=0.0,sigma=1.):
        Distribution.__init__(self)
        self.sigma = sigma
        self.mean = mean
        return

    def sample(self):
        return np.random.normal(self.mean,self.sigma)



class ElasticElectron(ContinuousDist):

    def __init__(self,enrg = 0):
        ContinuousDist.__init__(self,inv = lambda self,thet : np.arctanh(thet))

    def sample(self,x=1):
        if x > 0:
            if self.direct:
                return self.invCdf(np.random.rand(x))
        else:
            return None

def exponential(scale = 1.0):
    return np.random.exponential(scale)

if __name__=="__main__":
    # a = DiscreteDist()
    # b = ContinuousDist()
    c = ElasticElectron()
    print(c.sample())
    print("Successfully completed \a")



