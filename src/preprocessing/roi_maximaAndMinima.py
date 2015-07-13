#!/usr/bin/env python2

from regionOfInterest import RegionOfInterest
import numpy as np

class ROI_MaximaAndMinima(RegionOfInterest):
    """A region of interest is defined by the following rule:
    The region around a locale maxima or minima of the imaginary part, where the peak is larger than a cutoff value"""
    def __init__(self):
        self.SMALLEST_VALUE_CUTOFF_IN_PERCENT = 0.001
        self.PROTECTION_ARRAY_IN_DECADES = 2
        self.ResetToInitValues()

    def ResetToInitValues(self):

        self.localeMaxima = []
        self.localeMaximaIndices = []

        self.localeMinima = []
        self.localeMinimaIndices = []


    def Process(self, frequency, impedance):
        """This function returns all indices for the regions that are of interest."""
        indices = self.FindMaximaAndMinima(frequency, impedance)
        return indices

    def FindMaximaAndMinima(self, frequency, impedance):
        self.ResetToInitValues()
        imag= np.imag(impedance)

        for i in xrange(1,imag.size - 1):
        ##    print "imag[i] ", type(imag[i])
        ##    print "i ", type(i)
            if imag[i - 1] < imag[i] and imag[i] > imag[i + 1]:
                self.localeMaxima.append(imag[i])
                self.localeMaximaIndices.append(i)
            if imag[i - 1] > imag[i] and imag[i] < imag[i + 1]:
                self.localeMinima.append(imag[i])
                self.localeMinimaIndices.append(i)

        #for i in self.localeMaximaIndices:
        #    print "self.localeMaxima", type( self.localeMinimaIndices), type(i)

        #for i in self.localeMinimaIndices:
        #    print "self.localeMinima", type( self.localeMinimaIndices) ,  type(i)
        #print "self.localeMinimaIndices.size", type(self.localeMinimaIndices) #, len(self.localeMinimaIndices)

        #print "imag[self.localeMinimaIndices]",  imag[self.localeMinimaIndices], type(imag[])
        #print "imag[self.localeMinimaIndices]",  imag[self.localeMinimaIndices], type(imag[self.localeMinimaIndices])

        maxAmplitude = np.max( np.append (np.abs(imag[self.localeMaximaIndices]), np.abs(imag[self.localeMinimaIndices])) ) * self.SMALLEST_VALUE_CUTOFF_IN_PERCENT

        [self.localeMinimaIndices, self.lcoaleMinima ]  = self.NeglectSmallAmplitudes(self.localeMinimaIndices, self.localeMinima, maxAmplitude)
        [self.localeMaximaIndices, self.lcoaleMaxima ]  = self.NeglectSmallAmplitudes(self.localeMaximaIndices, self.localeMaxima, maxAmplitude)

        return self.CalculateProtectedRegions(frequency, np.append(self.localeMinimaIndices, self.localeMaximaIndices))

    def CalculateProtectedRegions(self, frequency, indices):
        protectedRegion = np.zeros(frequency.size, dtype=np.bool)
        for i in indices:
            middleFreq = frequency[i]
            counter = i-1
            decades = np.power(10, self.PROTECTION_ARRAY_IN_DECADES)
            while counter > 0:
                if middleFreq / decades > frequency[counter]:
                    break
                counter -= 1

            counter +=1
            protectedRegion[counter: i] = True
            counter = i+1

            while counter < frequency.size:
                if middleFreq * decades < frequency[counter]:
                    break
                counter += 1

            counter -=1
            protectedRegion[ i: counter] = True
        return protectedRegion

    def NeglectSmallAmplitudes(self, indices, amplitude, maxAmplitude):
        deleteIndices = []
        for i,j in enumerate( np.abs(amplitude) ):
            if j < maxAmplitude:
                deleteIndices.append(i)

        ## delete list from list by deleting from the back
        for i in deleteIndices[::-1]:
            del indices[i]
            del amplitude[i]

        return [indices, amplitude]

