# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 13:57:14 2020

@author: Michael Vander Wal
"""

import numpy as np
import TransportConstants as TC
eMass = TC._eMass
c = TC._c
mc2 = 1/c**2
# e = 1.602176634e-19
e = TC._eCharge
eV_Erg = TC._eV_Erg
x0 = -1/np.sqrt(3)
x1 = -x0

def electronElastXS(E,Z):
    EJ = E*eV_Erg
    vel = c*(1-((EJ/(eMass*c**2))+1)**(-2))**.5
    lightFrac = vel/c
    gamma = (1-lightFrac**2)**(-.5)
    p = eMass*gamma*vel
    # KE = p**2/(2*eMass)
    KE = eMass*c*c*(gamma-1)

    T = KE*mc2/(eMass)


    etaC = 1.64-0.0825*np.log(T)
    eta = etaC*1.7e-5*Z**(2./3.)*(T**-1)*(T+2)**-1

    xsElast = lambda theta: np.sin(theta)*((Z**2+Z)*e**4)/((p*vel*(1-np.cos(theta)+2*eta))**2)
    # xsElast = lambda mu: ((Z**2+Z)*e**4)/((p*vel*(1-mu+2*eta))**2)



    nIntegrals = 1000
    results = np.zeros((nIntegrals))
    intLimits = np.linspace(0,np.pi,nIntegrals+1)
    # intLimits = np.linspace(-1,1.,nIntegrals+1)
    for i in range(0,nIntegrals):
        results[i] = gaussQuad(xsElast,intLimits[i:i+2])


    return results.sum()*2*np.pi

def gaussQuad(func,endPoints):
    # print(type(endPoints))
    # print(endPoints)
    a = endPoints[0]
    b = endPoints[1]
    # x0 = -(3**(-2))
    # x1 = -(x0)
    f0 = func(((b-a)*x0+(b+a))*.5)
    f1 = func(((b-a)*x1+(b+a))*.5)
    return .5*(b-a)*(f0+f1)

def diffXS(E,Z):
    EJ = E*eV_Erg
    vel = c*(1-((EJ/(eMass*c**2))+1)**(-2))**.5
    lightFrac = vel/c
    gamma = (1-lightFrac**2)**(-.5)
    p = eMass*gamma*vel
    # KE = p**2/(2*eMass)
    KE = eMass*c*c*(gamma-1)

    T = KE*mc2/(eMass)

    etaC = 1.64-0.0825*np.log(T)
    eta = etaC*1.7e-5*Z**(2./3.)*(T**-1)*(T+2)**-1

    xs = []
    angle = []
    xsElastPrime = lambda theta: ((Z*Z+Z)*e**4)/((p*vel*(1-np.cos(theta)+2*eta))**2)
    # xsElastPrime = lambda mu: ((Z*Z+Z)*e**4)/((p*vel*(1-mu+2*eta))**2)

    angleStepSize = np.pi/100
    # angleStepSize = 2.0/100

    for i in range(0,101):
        xs.append(xsElastPrime(angleStepSize*i))
        angle.append(angleStepSize*i)
        # xs.append(xsElastPrime(angleStepSize*i-1))
        # angle.append(angleStepSize*i-1)

    # print(xs)
    # plt.semilogy(angle,xs)
    # plt.show()

    return angle,xs

def generateElasticElectronData(Z):
    # Z = 10 # number of electrons in a water molecule
    energyEV = []
    crossSections = []
    nSteps = 100
    stepSize = 6./nSteps
    for i in range(0,nSteps+1):
        temp = 10**(stepSize*i)
        energyEV.append(temp)

    for i in range(0,nSteps+1):
        crossSections.append(electronElastXS(energyEV[i],Z))

    totalCrossSections = [energyEV,crossSections]


    differentialXSections = []
    for i in range(len(energyEV)):
        output = diffXS(energyEV[i],Z)
        differentialXSections.append(output)
    return totalCrossSections,differentialXSections