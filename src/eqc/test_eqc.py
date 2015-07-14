#!/usr/bin/env python2

import unittest

from eqc import CircuitTree
from parser import Parser


class TestCircuitTree(unittest.TestCase):

    def setUp(self):
        self.parser = Parser(CircuitTree)

    def testCircuitTree(self):
        testcases = {
            'R+R': ([0.1, 1.5], 10, 0.1 + 1.5),
            'R|R': ([0.1, 1.5], 10, 1.0 / (1.0 / 0.1 + 1.0 / 1.5)),
            'R+C': ([0.1, 1.5], 10, 0.1 + 1 / (1j * 10 * 1.5)),
            'R|C': ([0.1, 1.5], 10, 0.1 / (1.0 + 1j * 10 * 0.1 * 1.5)),
            'R|L': ([0.1, 1.5], 10, 0.1 / (1.0 + 0.1 / (1j * 10 * 1.5))),
        }
        for case in testcases:
            circuit = self.parser.parse(case).collapseCircuit()
            p, w, res = testcases[case]
            self.assertAlmostEqual(circuit.eqc(w, p), res, msg=case)

    def testJacobian(self):
        testcases = {
            'R+R': ([2, 4], 10, [1, 1]),
            'R|R': ([2, 4], 10, [4**2 / (2.0 + 4.0)**2, 2**2 / (2.0 + 4.0)**2]),
        }
        for case in testcases:
            circuit = self.parser.parse(case).collapseCircuit()
            p, w, jac = testcases[case]
            for i, v in enumerate(jac):
                self.assertAlmostEqual(circuit.jac[i](w, p), v, msg=case)

    def tearDown(self):
        self.parser = None

suite = unittest.TestLoader().loadTestsFromTestCase(TestCircuitTree)
unittest.TextTestRunner(verbosity=2).run(suite)
