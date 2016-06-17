import numpy as np

# Implements parts of the analytical transmission line models found in
# "Irreversible Thermodynamics and Impedance Spectroscopy of Multilayer Membranes" - E. Zholkovskij
# http://dx.doi.org/10.1006/jcis.1995.1034

def tanh(x):
    np.seterr(all='raise')
    try:
        y = np.tanh(x)
    except:
        y = 1.0 if np.real(x) > 0.0 else -1.0
    np.seterr(all='warn')
    return y

Zr = lambda w,wk: np.complex128(np.sqrt(0.5*w/wk)*(1+1j))
Zd = lambda w,g,t,r: np.complex128(g*t*(1-t)*r/tanh(r))

def Bilayer(w, p):
    (g1, t1, w1) = p[0:3]
    (g2, t2, w2) = p[3:6]

    r1 = Zr(w,w1)
    r2 = Zr(w,w2)

    nom = (t2 - t1)**2
    denom = Zd(w,g1,t1,r1) + Zd(w,g2,t2,r2)

    Z = 1/g1 + 1/g2 + nom/denom
    return Z

def trilambda(w, p):
    (g1, t1, w1) = p[0:3]
    (g2, t2, w2) = p[3:6]
    (g3, t3, w3) = p[6:9]
    r1 = Zr(w,w1)
    r2 = Zr(w,w2)
    r3 = Zr(w,w3)

    nom = g2*t2*(1-t2)*r2**2
    denom = (Zd(w,g1,t1,r2)+Zd(w,g2,t2,r2))*(Zd(w,g2,t2,r2)+Zd(w,g3,t3,r3))*(np.sinh(r2)**2)
    result = nom/denom
    if np.isnan(np.real(result)): result = 0.0
    return result

def Trilayer(w, p):
    (g1, t1, w1) = p[0:3]
    (g2, t2, w2) = p[3:6]
    (g3, t3, w3) = p[6:9]

    Z12 = Bilayer(w, p[0:6]) - 1/g1 - 1/g2
    Z23 = Bilayer(w, p[3:9]) - 1/g2 - 1/g3

    h123  = trilambda(w,p)

    nom = Z12 + Z23 + 2 * h123 * np.sqrt(Z12*Z23)
    denom = 1 - h123**2

    return 1/g1 + 1/g2 + 1/g3 + nom/denom

def Quadlayer(w, p):
    (g1, t1, w1) = p[0:3]
    (g2, t2, w2) = p[3:6]
    (g3, t3, w3) = p[6:9]
    (g4, t4, w4) = p[9:12]
    r1 = Zr(w,w1)
    r2 = Zr(w,w2)
    r3 = Zr(w,w3)
    r4 = Zr(w,w4)
    Z12 = Bilayer(w, p[0:6]) - 1/g1 - 1/g2
    Z23 = Bilayer(w, p[3:9]) - 1/g2 - 1/g3
    Z34 = Bilayer(w, p[6:12]) - 1/g3 - 1/g4
    h123 = trilambda(w,p[0:9])
    h234 = trilambda(w,p[3:12])
    nom = (1-h234**2)*Z12 + (1-h123**2)*Z34 + Z23
    nom += 2*h123*np.sqrt(Z12*Z23) + 2*h234*np.sqrt(Z23*Z34)
    nom += 2*h123*h234*np.sqrt(Z12*Z34)
    denom = 1-(h123**2+h234**2)
    return 1/g1 + 1/g2 + 1/g3 + 1/g4 + nom/denom
