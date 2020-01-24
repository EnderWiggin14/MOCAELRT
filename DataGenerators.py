# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 13:57:14 2020

@author: Michael Vander Wal
"""

import numpy as np
import TransportConstants as TC
import matplotlib.pyplot as plt
import scipy as sci
eMass = TC._eMass
c = TC._c
mc2 = 1/c**2
# e = 1.602176634e-19
e = TC._eCharge
eV_Erg = TC._eV_Erg
x0 = -1/np.sqrt(3)
x1 = -x0

def electronElastXS(E,Z):
    # EJ = E*eV_Erg
    EJ = E
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
    # EJ = E*eV_Erg
    EJ = E
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
        # energyEV.append(temp)
        energyEV.append(temp*eV_Erg)

    for i in range(0,nSteps+1):
        crossSections.append(electronElastXS(energyEV[i],Z))

    totalCrossSections = [energyEV,crossSections]


    differentialXSections = []
    for i in range(len(energyEV)):
        output = diffXS(energyEV[i],Z)
        differentialXSections.append(output)
    return totalCrossSections,differentialXSections

def generateIonizationElectronData(E):
    vel = c*(1-((E/(eMass*c**2))+1)**(-2))**.5
    k = (2*np.pi*TC._eCharge/(TC._eMass*vel*vel))
    omega = lambda gamma: -2*(E-gamma)+(2*E*(2*E-gamma))**.5
    F = lambda a,b: a+b
    s = lambda a: (1-2*a)**.5
    phi = lambda gamma: 1
    f = lambda gamma: 1
    M1 = lambda a,b: (np.log(((b-a)*(1-b+a)*(1+a-s(a))*(1-a+s(a)))/(b*(1-b)*(1-a-s(a))*(1+a+s(a))))/a)+(2/(1+a))*(sci.special.ellipkinc(np.asin((1+a-2*b)/(1-a)),((1-a)/(1+a)))-sci.special.ellipkinc(np.asin((s(a))/(1-a)),((1-a)/(1+a))))
    M2 = lambda a,b: (np.log(((b-a)*(1-b+a))/(b*(1-b)))/a)+(2/(1+a))*(sci.special.ellipkinc(np.asin((1+a-2*b)/(1-a)),((1-a)/(1+a))))
    L = lambda a:(np.log(((1+a-s(a))*(1-a+s(a)))/((1-a-s(a))*(1+a+s(a))))/a)-(2/(1+a))*(sci.special.ellipkinc(np.asin((s(a))/(1-a)),((1-a)/(1+a))))
    MeanFreeIon = lambda gamma: k*f(gamma)*phi(gamma)*L(gamma/E)/E
    ion1 = lambda gamma: k*f(gamma)*phi(gamma)*M1()
    # print(M1(3,4))

    return

def generateExcitationElectronData():
    return

def generateVibrationElectronData():
    return

def fakeInelasticElectronXS(E):
    EJ = E
    k = (2*np.pi)**.5
    # print(1e4*pow(10,-19-2*np.log10(E)))
    diffIon = lambda gamma: pow(10,(-18-2.33*np.log10(EJ)))*(gamma*.1*EJ*k)*sci.stats.norm.pdf(gamma,.25*EJ,.1*EJ)
    # print(diffIon(.5*E))
    nIntegrals = 1000
    results = np.zeros((nIntegrals))
    intLimits = np.linspace(0,E,nIntegrals+1)
    # intLimits = np.linspace(-1,1.,nIntegrals+1)
    for i in range(0,nIntegrals):
        results[i] = gaussQuad(diffIon,intLimits[i:i+2])

    return results.sum()

def generateFakeInelasticElectronXS():
    energyEV = []
    crossSections = []
    nSteps = 100
    stepSize = 4./nSteps
    for i in range(0,nSteps+1):
        temp = 10**(stepSize*i)
        energyEV.append(temp*eV_Erg)
    # print(energyEV)
    for i in range(0,nSteps+1):
        a = fakeInelasticElectronXS(energyEV[i])
        # print('a = ',a)
        crossSections.append(a)

    totalCrossSections = [energyEV,crossSections]

    return totalCrossSections

def main():
    xs,difXS= generateElasticElectronData(10)
    xs = np.array(xs)
    difXS = np.array(difXS)
    print(xs[0,50])
    print(difXS[50,0,:])
    plt.loglog(xs[0,:],xs[1,:])
    plt.show()
    plt.semilogy(difXS[50,0,:],difXS[50,1,:])
    generateIonizationElectronData()

if __name__ == "__main__":
    main()


