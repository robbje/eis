#!/usr/bin/env python2

import unittest

from parameterset import ParameterSet


class TestParser(unittest.TestCase):

    def testPset(self):
        pset = ParameterSet(['p1', 'p2', 'p3'], [(0,1),(0,1),(0,1)], [1,2,3])

        pset.maskAll()
        self.assertEqual([], pset.getUnmaskedValues())

        pset.unmaskAll()
        self.assertEqual([1,2,3], pset.getUnmaskedValues())

        pset.maskParameter('p2')
        self.assertEqual([1,3], pset.getUnmaskedValues())

    def testTransform(self):
        pset = ParameterSet(['p1', 'p2', 'p3'], [(0,1),(0,1),(0,1)], [1,2,3])

        pset.setParameterMapping('p2', pset.T_MICRO)
        pset.updateValues([1,1,1])
        pset.maskParameter('p2')
        pset.invertMask()
        x = pset.getUnmaskedTransformedValues()[0]
        self.assertAlmostEqual(1e6, x, msg='{} != {}'.format(1e6, x))

        pset.unmaskAll()
        pset.setParameterMapping('p2', pset.T_POWER)
        pset.updateValues([1,4,1])
        pset.maskParameter('p2')
        pset.invertMask()
        x = pset.getUnmaskedTransformedValues()[0]
        self.assertAlmostEqual(1e4, x, msg='{} != {}'.format(1e4, x))

suite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
unittest.TextTestRunner(verbosity=2).run(suite)
