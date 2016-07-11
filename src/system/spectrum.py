#!/usr/bin/env python2

import json
import numpy as np
import scipy.signal
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
from copy import deepcopy


class Spectrum(object):
    def __init__(self):
        self.omega = []
        self.Z = []

    @classmethod
    def fromExperiments(cls, data):
        s = cls()
        """ data: List of Experiment-objects
            """
        if len(data) < 2:
            raise ValueError(
                "Too little experiments in spectrum: %i" %
                len(data))
        data.sort(key=lambda e: e.w)
        w, z = map(list, map(None, *[d.impedance() for d in data]))
        s.omega = np.array(w)
        s.Z = np.array(z)
        return s

    @classmethod
    def fromCircuit(cls, omega, eqc, p):
        """ omega: list of angular frequencies for this spectrum
            eqc: equivalent circuit function returning the impedance
            p: parameters to be used for the equivalent circuit function
            """
        s = cls()
        s.omega = np.array(omega)
        s.Z = np.array([eqc(w, p) for w in omega])
        s.eqc = eqc
        return s

    @classmethod
    def fromRawData(cls, omega, Z):
        """ omega: list of angular frequencies for this spectrum
            Z: list of impedances for this spectrum
            """
        s = cls()
        s.omega = deepcopy(np.array(omega))
        s.Z = deepcopy(np.array(Z))
        return s


    @classmethod
    def fromJSON(cls, jsonstring):
        d = json.loads(jsonstring)
        s = cls()
        s.omega = d['omega']
        s.Z = np.array(d['Re']) + 1j * np.array(d['Im'])
        return s

    def toJSON(self):
        return json.dumps({'omega':list(self.omega),
                           'Re':list(np.real(self.Z)),
                           'Im':list(np.imag(self.Z))})

    def fit(self, spectrum, pset):
        # TODO: utilize jacobian, if possible
        def residuals(p, spectrum, pset):
            pset.updateUnmaskedTransformedValues(np.abs(p))
            pset.applyConstraints()
            res = []
            for i, w in enumerate(spectrum.omega):
                z = self.eqc(w, pset._values)
                res.append(np.real(z) - np.real(spectrum.Z[i]))
                res.append(np.imag(z) - np.imag(spectrum.Z[i]))
            return np.array(res)

        p0 = pset.getUnmaskedTransformedValues()
        plsq = leastsq(residuals, p0, args=(spectrum, pset), \
                full_output = True,
                xtol = 1e-20,
                ftol = 1e-12,
                factor = 1)
        pset.updateUnmaskedTransformedValues(np.abs(plsq[0]))
        r = residuals(plsq[0], spectrum, pset)
        rmsd = np.sqrt(np.sum(np.power(r,2.0))/len(r))
        return pset, rmsd

    def updateParameter(self, p):
        self.p = np.array(p)
        self.Z = np.array([self.eqc(w, p) for w in self.omega])

    def interpolate(
            self, new_omega=2 * np.pi * np.power(10, np.arange(-5, 10, 0.1))):
        re = np.interp(new_omega, self.omega, np.real(self.Z))
        im = np.interp(new_omega, self.omega, np.imag(self.Z))
        self.Z = re + 1j * im
        self.omega = np.array(new_omega)

    def getImaginaryMaxima(self):
        return scipy.signal.argrelmax(np.imag(self.Z))

    def getImaginaryMinima(self):
        return scipy.signal.argrelmin(np.imag(self.Z))

    def cropFrequencyRange(self, wRange):
        newZ = []
        newOmega = []
        for i, w in enumerate(self.omega):
            if (wRange[0] == None or w > wRange[0]) and \
               (wRange[1] == None or w <= wRange[1]):
                newOmega.append(w)
                newZ.append(self.Z[i])
        self.Z = np.array(newZ)
        self.omega = np.array(newOmega)

    def plot_bode(self, style=['b+-', 'g+-']):
        re, = plt.semilogx(self.omega, np.real(self.Z), style[0])
        im, = plt.semilogx(self.omega, np.imag(self.Z), style[1])
        plt.legend([re, im], ['Re(Z)', 'Im(Z)'])
        return re, im

    def plot_nyquist(self, style='rx-'):
        plt.gca().set_aspect('equal')
        return plt.plot(np.real(self.Z), np.imag(self.Z), style)

    def do_kkr(self, change=False):
        ng = 1
        absZ = np.abs(self.Z)
        phiZ = np.angle(self.Z)
        linF = np.log(self.omega)
        int_term = np.zeros(self.Z.shape)
        diff_term = np.zeros(self.Z.shape)
        for k in xrange(ng, phiZ.shape[0] - ng):
            int_term[k] = -np.trapz(phiZ[k:], linF[k:])
            diff_term[k] = np.mean(
                np.diff(
                    phiZ[
                        k -
                        1:k +
                        2]) /
                np.diff(
                    linF[
                        k -
                        1:k +
                        2]))
        gamma = -np.pi / 6.0
        lnH = 2.0 / np.pi * int_term + gamma * diff_term
        err_lnH = np.log(absZ[ng:-ng]) - lnH[ng:-ng]
        constOffset = np.mean(err_lnH)
        abszhit = np.zeros(absZ.shape)
        abszhit[ng:-ng] = np.exp(constOffset + lnH[ng:-ng])
        z = abszhit * np.exp(1j * phiZ)
        w = self.omega
        if change:
            self.omega = w[ng:-ng]
            self.Z = z[ng:-ng]
        return Spectrum.fromRawData(w[ng:-ng], z[ng:-ng])
