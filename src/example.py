#!/usr/bin/env python2

from system.spectrum import Spectrum
from system.parameterset import ParameterSet
from eqc.eqc import CircuitTree
from eqc.parser import Parser
import matplotlib.pyplot as plt
import numpy as np

class MySpectrum(Spectrum):
    @classmethod
    def fromCSV(cls, filename):
        s = cls()
        for line in file(filename).readlines():
            val = line.split(',')
            s.omega.append(float(val[0]))
            s.Z.append(float(val[1]) + 1j * float(val[2]))

parser = Parser(CircuitTree)
p = [0.03, 3e-5, 75.0, 0.5, 0.1, 375.0, 0.0002, 0.01, 375.0, 0.97, 1.0, 75.0, 0.5, 0.1]
parsetree = parser.parse('(R|C)+Quadlayer').collapseCircuit()
eqc_fn, jac_fn = parsetree.getCircuit()

s = Spectrum.fromJSON(file('cases/zholkovskij.json').read())
#s = MySpectrum.fromCSV('MyCSVDataFile')

e = Spectrum.fromCircuit(s.omega, eqc_fn, p)
pset = ParameterSet.fromTree(parsetree, p)

# Scale transport number t3
pset.setParameterMapping('Quadlayer_1{t2}', pset.T_MICRO)
pset.setParameterMapping('Quadlayer_1{t3}', pset.T_MICRO)

# Fit only t2, t3, R and C:
pset.unmaskAll()
pset.maskParameter('Quadlayer_1{t2}')
pset.maskParameter('Quadlayer_1{t3}')
pset.maskParameter('R_1{R}')
pset.maskParameter('C_1{C}')
pset.invertMask()
p, rmsd = e.fit(s, pset)

plt.figure()
s.plot_bode(['kx', 'kx'])       # Experimental values
e.plot_bode(['r-', 'r-'])       # Values pre fit: red
e.updateParameter(p._values)
e.plot_bode(['g-', 'g-'])       # Values post fit: green
plt.show()

plt.figure()
plt.gca().invert_yaxis()
s.plot_nyquist('kx')
e.plot_nyquist('g-')
plt.show()
