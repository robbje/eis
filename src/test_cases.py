#!/usr/bin/env python2

import unittest

from system.spectrum import Spectrum
from system.parameterset import ParameterSet
from eqc.eqc import CircuitTree
from eqc.parser import Parser

simplecases = [{'specfile':'cases/trilayer.json', 'eqc':'(R|C)+Warb', 'p0':[0.025,1e-4,0.025,10]}]

class TestParser(unittest.TestCase):
    def testSimpleCases(self):
        for case in simplecases:
            p = case['p0']
            parser = Parser(CircuitTree)
            parsetree = parser.parse(case['eqc']).collapseCircuit()
            s = Spectrum.fromJSON(file(case['specfile']).read())
            pset = ParameterSet.fromTree(parsetree, p)
            eqc_fn, jac_fn = parsetree.getCircuit()
            e = Spectrum.fromCircuit(s.omega, eqc_fn, p)
            p, rmsd = e.fit(s, pset)
            self.assertLess(rmsd, 1e-3,
                msg='Could not fit {} to rmsd 1e-3: got {}'.format(case['specfile'], rmsd))

    def testZholkovskij(self):
        p = [0.03, 3e-5, 75.0, 0.5, 0.1, 375.0, 0.0002, 0.01, 375.0, 0.97, 1.0, 75.0, 0.5, 0.1]
        parser = Parser(CircuitTree)
        parsetree = parser.parse('(R|C)+Quadlayer').collapseCircuit()
        s = Spectrum.fromJSON(file('cases/zholkovskij.json').read())
        pset = ParameterSet.fromTree(parsetree, p)
        pset.setParameterMapping('R_2{C}', pset.T_MICRO)
        pset.setParameterMapping('Quadlayer_1{t2}', pset.T_MICRO)
        pset.setParameterMapping('Quadlayer_1{t3}', pset.T_MICRO)
        pset.unmaskAll()
        pset.maskParameter('Quadlayer_1{t2}')
        pset.maskParameter('Quadlayer_1{t3}')
        pset.maskParameter('R_2{R}')
        pset.maskParameter('C_2{C}')
        pset.invertMask()
        eqc_fn, jac_fn = parsetree.getCircuit()
        e = Spectrum.fromCircuit(s.omega, eqc_fn, p)
        p, rmsd = e.fit(s, pset)
        self.assertLess(rmsd, 2e-3)

suite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
unittest.TextTestRunner(verbosity=2).run(suite)
