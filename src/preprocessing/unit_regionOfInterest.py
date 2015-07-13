#!/usr/bin/env python2
import numpy as np
import unittest
import sys

from regionOfInterest import RegionOfInterest

class TestRegionOfInterest(unittest.TestCase):

    def testFindingInterestingPartsEmpty(self):
        freq = np.power(10, np.arange(-6,6,0.01) )
        region = RegionOfInterest()
        indices = region.Process(freq, np.zeros(freq.size))
        self.assertTrue( (np.equal(indices, False)).all() )

    def testFindingInterestingPartsFull(self):
        freq = np.power(10, np.arange(-6,6,0.01) )
        region = RegionOfInterest()
        indices = region.Process(freq, 1j * np.ones(freq.size))
        self.assertTrue( (np.equal(indices, True)).all() )

    def testFindingInterestingPartsMixedSimple(self):
        freq = np.power(10, np.arange(-6,6,0.01) )
        HALF_ELEMENTS = freq.size / 2
        region = RegionOfInterest()
        impd = np.append(1j * np.ones(HALF_ELEMENTS), np.zeros(HALF_ELEMENTS))
        indices = region.Process(freq, impd)

        self.assertEqual( np.bincount( np.equal(indices, False))[0], HALF_ELEMENTS ) #second half
        self.assertEqual( np.bincount( np.equal(indices, False))[1], HALF_ELEMENTS ) #first half
        for i in xrange(0,HALF_ELEMENTS):
            self.assertEqual( indices[i], True)
            self.assertEqual( indices[ HALF_ELEMENTS+ i], False)

    def testDefinitionOfRegionOfInterest(self):
        freq = np.power(10, np.arange(-6,6,0.01) )
        region = RegionOfInterest()
        R = 10.0
        tau = 1.0
        impedance = R / ( 1.0 + 1j * 2.0 * freq* np.pi * tau)

        indices = region.Process(freq, impedance)
        self.assertTrue( (freq[indices] * 2 * np.pi).all() > 0.01)
        self.assertTrue( (freq[indices] * 2 * np.pi).all() < 100)

if __name__ == '__main__':
    unittest.main()
