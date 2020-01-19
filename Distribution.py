# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 10:28:56 2019

@author: Michael Vander Wal
"""
import numpy as np
import scipy.stats as sci
# import abc
import TransportConstants as TC
from functools import partial


def referenceFunction():
    pass
FUNC_TYPE = type(referenceFunction)
BUILTIN_FUNC_TYPE = type(pow)


def exponential(scale = 1.0):
    return np.random.exponential(scale)


# def interp2(self,xStar):
#     i = 0
#     length = len(self.energyValues)
#     while i < length and self.energyValues[i] <= xStar:
#         i += 1
#     x1 = self.energyValues[i-1]
#     x2 = self.energyValues[i]
#     X = ((xStar-x1)/(x2-x1))
#     yStar = []
#     for i in range(angles0):
#         y1 = angles0[i]
#         y2 = angles1[i]
#         yStar.append( X*(y2-y1)+y1)
#     return np.array(yStar)

class Distribution():
    proposalPdfHandle = None
    proposalSampleHandle = None
    domain = None
    pdfData = None

    def __init__(self):
        return

    def sample(self,param):
        weight = 1.0
        val = self.proposalSampleHandle()
        tempParam=[]
        tempParam +=param
        tempParam.append(val)
        if isinstance(self.pdfData,(FUNC_TYPE,BUILTIN_FUNC_TYPE,partial)):
            weight = self.pdf(tempParam)/self.proposalPdfHandle(val)
        elif isinstance(self.pdfData,(list,np.ndarray)):
            weight = self.pdf(tempParam)/self.proposalPdfHandle(val)
        else:
            raise Exception("The provided combination of object attributes is not valid for Distribution.handle and Distribution.pdfData.")
        return val, weight

    def pdf(self,x):
        if isinstance(self.pdfData,(list,np.ndarray)):
            return self.interp(x,self.pdfData)
        elif isinstance(self.pdfData,(FUNC_TYPE,partial)):
            if isinstance(x,list):
                handle = partial(self.pdfData,x[0])
                for i in range(1,len(x)):
                    handle = partial(handle,x[i])
                return handle()
            else:
                return self.pdfData(x)
        elif isinstance(self.pdfData,BUILTIN_FUNC_TYPE):
            if isinstance(x,list):
                handle = partial(self.pdfData,x[0])
                for i in range(1,len(x)):
                    handle = partial(handle,x[i])
                return handle()
            else:
                return self.pdfData(x)

    def setPdfData(self,data):
        if isinstance(data,(list,np.ndarray)):
            self.pdfData = np.array(data)
        else:
            self.pdfData = data

    def setDomain(self,domain):
        self.domain = np.array(domain)
        if self.proposalSampleHandle is None or self.proposalPdfHandle is None:
            unifSamp = partial(np.random.uniform,low = self.domain.min(), high = self.domain.max())
            unifPdf = partial(sci.uniform.pdf, loc = self.domain.min(), scale = self.domain.max())
            self.setProposalSampleHandle(unifSamp)
            self.setProposalPdfHandle(unifPdf)

    def setProposalPdfHandle(self,func):
        self.proposalPdfHandle = func

    def setProposalSampleHandle(self,func):
        self.proposalSampleHandle = func

    def interp(self,xStar,yVals): # should replace while loop with numpy.searchsort()
        # i = 0
        # length = len(self.domain)
        # while i < length and self.domain[i] <= xStar:
        #     i += 1
        i = np.searchsorted(self.domain,xStar,side='right')
        x1 = self.domain[i-1]
        x2 = self.domain[i]
        y1 = self.yVals[i-1]
        y2 = self.yVals[i]
        ystar = ((xStar-x1)/(x2-x1))*(y2-y1)+y1
        return ystar


def diffElasticElectronXS(Z,EJ,theta):
    vel = TC._c*(1-((EJ/(TC._eMass*TC._c**2))+1)**(-2))**.5
    lightFrac = vel/TC._c
    gamma = (1-lightFrac**2)**(-.5)
    p = TC._eMass*gamma*vel
    KE = TC._eMass*TC._c*TC._c*(gamma-1)

    T = KE*TC._mc2/(TC._eMass)
    etaC = 1.64-0.0825*np.log(T)
    eta = etaC*1.7e-5*Z**(2./3.)*(T**-1)*(T+2)**-1

    return ((Z*Z+Z)*TC._eCharge*TC._eCharge*TC._eCharge*TC._eCharge)/((p*vel*(1-np.cos(theta)+2*eta))**2)


if __name__=="__main__":
    a = Distribution()
    f = diffElasticElectronXS
    a.setPdfData(f)
    print(type(a.pdfData))
    print(a.pdf([10,100,.2*np.pi/180]))
    print("Successfully completed \a")
