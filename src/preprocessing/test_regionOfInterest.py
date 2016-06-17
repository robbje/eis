#!/usr/bin/env python2
import numpy as np
import unittest
import sys

#from regionOfInterest import  PlotRegion
from roi_amplitude import ROI_Amplitude
from roi_maximaAndMinima import ROI_MaximaAndMinima


class TestRegionOfInterest(unittest.TestCase):

    def testFindingInterestingAmplitudePartsEmpty(self):
        freq = np.power(10, np.arange(-6, 6, 0.01))
        region = ROI_Amplitude()
        indices = region.Process(freq, np.zeros(freq.size))
        self.assertTrue((np.equal(indices, False)).all())

    def testFindingInterestingAmplitudePartsFull(self):
        freq = np.power(10, np.arange(-6, 6, 0.01))
        region = ROI_Amplitude()
        indices = region.Process(freq, 1j * np.ones(freq.size))
        self.assertTrue((np.equal(indices, True)).all())

    def testFindingInterestingAmplitudePartsMixedSimple(self):
        freq = np.power(10, np.arange(-6, 6, 0.01))
        HALF_ELEMENTS = freq.size / 2
        region = ROI_Amplitude()
        impd = np.append(1j * np.ones(HALF_ELEMENTS), np.zeros(HALF_ELEMENTS))
        indices = region.Process(freq, impd)

        # second half
        self.assertEqual(
            np.bincount(np.equal(indices, False))[0], HALF_ELEMENTS)
        # first half
        self.assertEqual(
            np.bincount(np.equal(indices, False))[1], HALF_ELEMENTS)
        for i in xrange(0, HALF_ELEMENTS):
            self.assertEqual(indices[i], True)
            self.assertEqual(indices[HALF_ELEMENTS + i], False)

    def testDefinitionOfRegionOfInterestAmplitude(self):
        freq = np.power(10, np.arange(-6, 6, 0.01))
        region = ROI_Amplitude()
        R = 10.0
        tau = 1.0
        impedance = R / (1.0 + 1j * 2.0 * freq * np.pi * tau)

        indices = region.Process(freq * 2 * np.pi, impedance)
        self.assertTrue((freq[indices] * 2 * np.pi > 0.01).all())
        self.assertTrue((freq[indices] * 2 * np.pi < 100).all())

    def test_MaximaAndMinimaPeakBoundaries(self):

        omega = np.power(10, np.arange(-6, 6, 0.01)) * 2.0 * np.pi
        region = ROI_MaximaAndMinima()
        R = 10.0
        tau = 0.01
        impedance = R / (1.0 + 1j * omega * tau)
        indices = region.Process(omega, impedance)
        #PlotRegion( omega, impedance, indices)
        self.assertTrue((1.0 / (omega[indices]) >= tau / 100.0).all())
        self.assertTrue((1.0 / (omega[indices]) <= tau * 101.0).all())

    def test_MaximaAndMinimaWithInduction(self):

        omega = np.power(10, np.arange(-6, 6, 0.01)) * 2 * np.pi
        region = ROI_MaximaAndMinima()
        R = 10.0
        tau = 0.01
        L = 1000
        impedance = R / (1.0 + 1j * omega * tau)
        impedance += (1.0 / R + 1.0 / (1j * omega * L)) ** -1.0
        indices = region.Process(omega, impedance)

        self.assertTrue((1.0 / (omega[indices]) >= tau / 100.0).all())
        self.assertTrue((1.0 / (omega[indices]) <= L / R * 101.0).all())
        #PlotRegion(omega, impedance, indices)

if __name__ == '__main__':
    unittest.main()
