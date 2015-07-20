#!/usr/bin/env python2

import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
from copy import deepcopy

class Spectrum(object):

    def fromExperiments(self, data):
        if len(data) < 2:
            raise ValueError("Too little experiments in spectrum: %i" % len(data))
        data.sort(key = lambda e: e.w)
        w, z = map(list,map(None,*[d.impedance() for d in data])) 
        self.omega = np.array(w)
        self.Z = np.array(z)
        return self

    def fromCircuit(self, omega, eqc, p):
        self.omega = np.array(omega)
        self.Z = np.array([eqc(w,p) for w in self.omega])
        self.eqc = eqc
        self.p = p
        return self

    def updateParameter(self, p):
        self.p = np.array(p)
        self.Z = np.array([self.eqc(w,p) for w in self.omega])

    def fromRawData(self, omega, Z):
        self.omega = deepcopy(np.array(omega))
        self.Z = deepcopy(np.array(Z))
        return self

    def interpolate(self, new_omega=2*np.pi*np.power(10, np.arange(-5,10,0.1))):
        re = np.interp(new_omega, self.omega, np.real(self.Z))
        im = np.interp(new_omega, self.omega, np.imag(self.Z))
        self.Z = re+1j*im
        self.omega = np.array(new_omega)

    def getImaginaryMaxima(self):
        return scipy.signal.argrelmax(np.imag(self.Z))

    def getImaginaryMinima(self):
        return scipy.signal.argrelmin(np.imag(self.Z))

    def cropFrequencyRange(self, wRange):
        newZ = []
        newOmega = []
        for i,w in enumerate(self.omega):
            if (wRange[0] == None or w > wRange[0]) and \
               (wRange[1] == None or w <= wRange[1]):
                newOmega.append(w)
                newZ.append(self.Z[i])
        self.Z = np.array(newZ)
        self.omega = np.array(newOmega)

    def plot_bode(self,style=['b+-','g+-']):
        re, = plt.semilogx(self.omega, np.real(self.Z), style[0])
        im, = plt.semilogx(self.omega, np.imag(self.Z), style[1])
        plt.legend([re, im], ['Re(Z)', 'Im(Z)'])

    def plot_nyquist(self, style='rx-'):
        plt.gca().set_aspect('equal')
        plt.plot(np.real(self.Z), np.imag(self.Z), style)

    def do_kkr(self, change=False):
        ng = 1
        absZ = np.abs(self.Z)
        phiZ = np.angle(self.Z)
        linF = np.log(self.omega)
        int_term = np.zeros(self.Z.shape)
        diff_term = np.zeros(self.Z.shape)
        for k in xrange(ng, phiZ.shape[0] - ng):
            int_term[k] = -np.trapz(phiZ[k:], linF[k:])
            diff_term[k] = np.mean(np.diff(phiZ[k-1:k+2])/np.diff(linF[k-1:k+2]))
        gamma = -np.pi/6.0
        lnH = 2.0 / np.pi * int_term + gamma * diff_term
        err_lnH = np.log(absZ[ng:-ng]) - lnH[ng:-ng]
        constOffset = np.mean(err_lnH)
        abszhit = np.zeros(absZ.shape)
        abszhit[ng:-ng] = np.exp(constOffset + lnH[ng:-ng])
        z = abszhit * np.exp(1j*phiZ)
        w = self.omega
        if change:
            self.omega = w[ng:-ng]
            self.Z = z[ng:-ng]
        return w, z
