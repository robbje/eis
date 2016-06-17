#!/usr/bin/env python2

import unittest

from system.spectrum import Spectrum
from system.parameterset import ParameterSet
from eqc.eqc import CircuitTree
from eqc.parser import Parser

cases = [{'specfile':'cases/trilayer.json', 'eqc':'(R|C)+Warb', 'p0':[0.025,1e-4,0.025,10]}]

class TestParser(unittest.TestCase):
    parser = Parser(CircuitTree)

    def testCases(self):
        for case in cases:
            p = case['p0']
            parsetree = self.parser.parse(case['eqc'])
            s = Spectrum.fromJSON(file(case['specfile']).read())
            pset = ParameterSet.fromTree(parsetree, p)
            eqc_fn, jac_fn = parsetree.getCircuit()
            e = Spectrum.fromCircuit(s.omega, eqc_fn, p)
            p, rmsd = e.fit(s, pset)
            self.assertLess(rmsd, 1e-3,
                msg='Could not fit {} to rmsd 1e-3'.format(case['specfile']))

suite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
unittest.TextTestRunner(verbosity=2).run(suite)
