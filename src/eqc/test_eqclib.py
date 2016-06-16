#!/usr/bin/env python2

import unittest

from eqclib import eqcLib
import numpy as np


class TestEqcLib(unittest.TestCase):

    def testPartialDerivatives(self):
        finiteDelta = 1e-9
        maxDelta = 1e-6
        w = 1
        for element in ['R', 'L', 'C', 'Zarc', 'CPE', 'Warb']:
            cdef = eqcLib[element]['def']
            p = [1] * (len(cdef['pNames']))
            eqc0 = cdef['eqc'](w, p)
            jac = [x(w, p) for x in cdef['jac']]
            fd = []
            for i, v in enumerate(p):
                p[i] += finiteDelta
                fd.append((cdef['eqc'](w, p) - eqc0) / finiteDelta)
                p[i] -= finiteDelta

            for i, partial in enumerate(fd):
                diff = np.abs(jac[i] - partial)
                msg = "%s{%s} FD %r != %r Difference: %r" % (element,
                                                             cdef['pNames'][i],
                                                             partial,
                                                             jac[i],
                                                             diff
                                                             )
                self.assertAlmostEqual(diff, 0.0, msg=msg, delta=maxDelta)

suite = unittest.TestLoader().loadTestsFromTestCase(TestEqcLib)
unittest.TextTestRunner(verbosity=2).run(suite)
