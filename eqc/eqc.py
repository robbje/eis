#!/usr/bin/env python2

from eqclib import getClassDefinition
from parser import Node
from copy import deepcopy
import numpy as np

class CircuitTree(Node):
    def __init__(self, params=[], eqc=lambda w,p: 0, name="", pNames = ""):
        Node.__init__(self)
        self.p = params
        self.eqc = eqc
        self.name = name
        self.pNames = pNames

    def collapseCircuit(self):
        if self.value.type == 'SYMBOL':
            cdef = getClassDefinition(self.value.value)
            new = CircuitTree(**cdef)
        elif self.value.type == 'PARALLEL':
            new = self.left.collapseCircuit()
            new |= self.right.collapseCircuit()
        elif self.value.type == 'SERIES':
            new = self.left.collapseCircuit()
            new += self.right.collapseCircuit()
        else:
            raise ValueError('BUG: Unknown type in parse tree')
            return None
        self.eqc = deepcopy(new.eqc)
        self.p = deepcopy(new.p)
        self.name = deepcopy(new.name)
        self.pNames = deepcopy(new.pNames)
        return self

    def __add__(self,other):
        pu = len(self.p)
        self.p = np.append(self.p, other.p)
        self.pNames += other.pNames
        f = self.eqc
        self.name = "(%s+%s)" % (self.name, other.name)
        self.eqc = lambda w,p: f(w,p) + other.eqc(w,p[pu:])
        return self

    def __or__(self,other):
        pu = len(self.p)
        self.p = np.append(self.p, other.p)
        self.pNames += other.pNames
        f = self.eqc
        self.name = "(%s|%s)" % (self.name, other.name)
        self.eqc = lambda w,p: \
            1.0/(1.0/f(w,p)+1.0/other.eqc(w,p[pu:]))
        return self

if __name__ == "__main__":
    from parser import Parser
    p = Parser(CircuitTree)
    circuit = p.parse('R+(R|Warb)+(R|L)+(R|L)')
    print circuit
    circuit = circuit.collapseCircuit()
    print circuit.name
    print circuit.pNames
    print circuit.eqc(1,[2,1,4,1,2,3,4,10])
