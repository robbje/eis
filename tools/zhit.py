#!/usr/bin/env python
## Created by Friedrich Hust
## W. Ehm, H. Gohr, R. Kaus, B. Roseler, C. A. Schiller: The evaluation of electrochemical impedance spectra using a modified logarithmic Hilbert transform. In: ACH-Models in Chemistry. 137, Nr. 2-3, 2000, S. 145–157.

import numpy as np

def ZHit( freq, Z):#, phiz = 0):
    if not np.iscomplex(Z).any():
        print "\033[1;31mZ is not a complex number\033[1;32m"
        exit(1)
    absZ = np.abs(Z)
    phiZ = np.angle(Z)
    omega = 2 * np.pi * freq
    linearFreq = np.log(omega)

    ng = 1 # number of Gamma terms
    int_term   = np.zeros(Z.shape)
    diff_term  = np.zeros(Z.shape)
    if ng == 2:
        diff_term3 = np.zeros(Z.shape)

    for k in xrange( ng , phiZ.shape[0] - ng ):
        int_term[k]  = - np.trapz(phiZ[k:], linearFreq[k:]) # WARNING !!ATTENTION THIS HAS DIFFERENT SYNTAX THAN IN MATLAB!!!
        diff_term[k] = np.mean( np.diff( phiZ[k-1:k+2]) / np.diff( linearFreq[ k-1:k+2 ] ) ) #Differential-Term
        if ng == 2:
             diff3_term[k] = np.mean( np.diff( phiZ[k-2:k+3], 3) / np.diff( linearFreq[k-1:k+2] ) ** 3) #Differential-Term, 3. Ableitung

    if ng == 1:
        gamma = - np.pi / 6.0 #Koeffizienten der Z-HIT= -2/pi*zeta(1+1)*2^(-1)
        lnH = 2.0 / np.pi * int_term  + gamma * diff_term
    elif ng == 2:
        gamma_3 = (-2.0 / np.pi*zeta(3+1)*2^(-3)) #Koeffizientbn der Z-HIT
        lnH = 2.0 / np.pi * int_term  + gamma * diff_term + gamma_3 * diff3_term
    else:
        print "\033[1;31mUnsupported gammavalue used\033[1;32m"

    err_lnH = np.log( absZ[ng : -ng ]) - lnH[ ng : -ng ]

    constOffset = np.mean (err_lnH)
    abszhit = np.zeros(absZ.shape)
    abszhit[ng:-ng] = np.exp( constOffset + lnH[ ng : -ng ] )

    return abszhit * np.exp( 1j * phiZ )
