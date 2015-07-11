#!/usr/bin/env python2

from eqclib import getClassDefinition
from parser import Node
from copy import deepcopy

class CircuitTree(Node):
    def __init__(self, params=[], eqc=lambda w,p: 0, name=""):
        Node.__init__(self)
        self.p = params
        self.eqc = eqc
        self.name = name

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
            # Something that should not happen and
            # probably raise some exception
            return None
        self.eqc = deepcopy(new.eqc)
        self.p = deepcopy(new.p)
        self.name = deepcopy(new.name)
        return self

    def __add__(self,other):
        pu = len(self.p)
        self.p += other.p
        f = self.eqc
        self.name = "(%s+%s)" % (self.name, other.name)
        self.eqc = lambda w,p: f(w,p) + other.eqc(w,p[pu:])
        return self

    def __or__(self,other):
        pu = len(self.p)
        self.p += other.p
        f = self.eqc
        self.name = "(%s|%s)" % (self.name, other.name)
        self.eqc = lambda w,p: \
            1.0/(1.0/f(w,p)+1.0/other.eqc(w,p[pu:]))
        return self

if __name__ == "__main__":
    from parser import Parser
    p = Parser(CircuitTree)
    circuit = p.parse('R_4+(R_5|R_4)').collapseCircuit()
    print circuit.name
    print circuit.eqc(1,[2,1,4])
