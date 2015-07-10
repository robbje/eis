#!/usr/bin/env python2

from eqclib import get_eqc
from parser import Node, Parser

class EqcNode(Node):
    def __init__(self, *args, **kwargs):
        Node.__init__(self)
        self.p = []
        self.eqc = lambda omega,p=self.p: 0
        self.name = ""

    def getCircuitFunc(self):
        if self.value.type == 'SYMBOL':
            ln, eqc, p = get_eqc(self.value.value)
            self.p = p
            self.name = ln
            self.eqc = lambda w,p: eqc(w,p)
            return self
        elif self.value.type == 'PARALLEL':
            a = self.left.getCircuitFunc()
            a |= self.right.getCircuitFunc()
            return a
        elif self.value.type == 'SERIES':
            a = self.left.getCircuitFunc()
            a += self.right.getCircuitFunc()
            return a
        # This will result in an error, probably
        return None

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
    p = Parser(EqcNode)
    root = p.parse('R_4+(R_5|R_4)')
    f = root.getCircuitFunc()
    print f.name
    print f.eqc(1, [2,1,4])
