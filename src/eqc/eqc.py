#!/usr/bin/env python2

from parser import Node
from copy import deepcopy
import numpy as np
from eqclib import getClassDefinition


class CircuitTree(Node):

    def __init__(
            self,
            params=[],
            eqc=lambda w,
            p: 0,
            name="",
            pNames="",
            jac=[]):
        """Constructor for a CircuitTree node

            params: a list of numerical values
            eqc: frequency dependent equivalent circuit function
            name: name of the element
            pNames: names of the elements' parameters
            jac: elements jacobian vector of parameters
            """

        Node.__init__(self)
        self.p = params
        self.eqc = eqc
        self.name = name
        self.pNames = pNames
        self.jac = jac

    def collapseCircuit(self):
        """Builds the function describing the frequency dependence of circuit

            Returns the root node of the parser tree, with all equivalent
            circuit functions generated.
            """

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
        self.jac = deepcopy(new.jac)
        return self

    def __add__(self, other):
        pu = len(self.p)
        self.p = np.append(self.p, other.p)
        self.pNames += other.pNames
        f = self.eqc
        self.name = "(%s+%s)" % (self.name, other.name)
        self.eqc = lambda w, p: f(w, p) + other.eqc(w, p[pu:])
        self.jac += [lambda w, p: j(w, p[pu:]) for j in other.jac]
        return self

    def __or__(self, other):
        pu = len(self.p)
        self.p = np.append(self.p, other.p)
        self.pNames += other.pNames
        f = self.eqc
        self.name = "(%s|%s)" % (self.name, other.name)
        self.eqc = lambda w, p: \
            1.0 / (1.0 / f(w, p) + 1.0 / other.eqc(w, p[pu:]))
        for i, jac in enumerate(self.jac):
            self.jac[i] = lambda w, p: np.power(other.eqc(
                w, p[pu:]), 2.0) * jac(w, p) / np.power(other.eqc(w, p[pu:]) + f(w, p), 2.0)
        for jac in other.jac:
            self.jac.append(lambda w, p: np.power(f(w, p), 2.0) *
                            jac(w, p[pu:]) /
                            np.power(other.eqc(w, p[pu:]) +
                                     f(w, p), 2.0))
        return self
