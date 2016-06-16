#!/usr/bin/env python2
import ply.lex as lex


class Node(object):

    """Base class to be used in a parsertree
        """

    def __init__(self):
        self.right = None
        self.left = None
        self.value = None
        self.parent = None

    def is_terminal(self):
        return self.value.type == 'SYMBOL'

    def __str__(self):
        if not self.value:
            # only a single element in circuit
            if self.left: return str(self.left)
            return "Empty"
        if self.is_terminal():
            return "%s" % self.value.value
        return "%s(%s, %s)" % (self.value.value, self.left, self.right)


class Parser(object):
    tokens = (
        'SYMBOL',
        'SERIES',
        'PARALLEL',
        'LPAREN',
        'RPAREN',
    )
    t_SERIES = r'\+'
    t_PARALLEL = r'\|'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_SYMBOL = r'[a-zA-Z]+(_[a-zA-Z0-9]*|$^)*'

    def t_error(self, t):
        pass

    def __init__(self, nodeobj):
        """Constructor

            Requires an implementation of a binary node object.
            It has to have the properties right,left,parent,value.
            """

        self.lexer = lex.lex(object=self)
        self.nodeobj = nodeobj

    def parse(self, string):
        """Parses a string according to a simple language

            Operators: + | ( )
            Symbols: [a-zA-Z]+(_[a-zA-Z0-9]*|$^)*
            """

        self.line = string
        self.lexer.input(string)
        self.root = self.nodeobj()
        self.current = self.root
        self.indent = 0
        while True:
            t = self.lexer.token()
            if not t:
                break
            self.handleToken(t)
        return self.root

    def genError(self, msg, pos):
        pos += 1
        exception = "%s at pos %i\n" % (msg, pos)
        exception += "%s\n" % self.line
        exception += "%s" % "^".rjust(pos, " ")
        raise Exception(exception)

    def handleToken(self, t):
        if t.type == 'SYMBOL':
            # Symbol
            # Set the value of the current node and return to
            # parent node. If it doesn't exist, make a new root.
            self.current.value = t
            if not self.current.parent:
                tmp = self.nodeobj()
                self.current.parent = tmp
                tmp.left = self.current
                self.root = tmp
            self.current = self.current.parent
        elif t.type == 'LPAREN':
            # Left parenthesis
            # Increase indentation level. Create a new left leaf.
            self.indent += 1
            if self.current.left:
                self.genError("Unexpected parenthesis", t.lexpos)
            tmp = self.nodeobj()
            tmp.parent = self.current
            self.current.left = tmp
            self.current = self.current.left
        elif t.type == 'RPAREN':
            # Right parenthesis
            # Decrease indentation level. It is an error if it drops negative.
            self.indent -= 1
            if self.indent < 0:
                self.genError("Unbalanced parenthesis", t.lexpos)
            if self.current.parent:
                self.current = self.current.parent
            if not self.current.left.value:
                self.genError("Empty brackets", t.lexpos)
                self.current.left = None
        elif t.type in ['SERIES', 'PARALLEL']:
            # Series or parallel token
            # If the current node has a value, we need to make a new root.
            # If not, set this nodes value to the operator and move to
            # the right leaf.
            if not self.current.left:
                raise Exception("Syntax error at pos %i" % t.lexpos)
            if self.current.value:
                tmp = self.nodeobj()
                self.current.parent = tmp
                tmp.left = self.current
                self.root = tmp
                self.current = tmp
            self.current.value = t
            # New right node
            tmp = self.nodeobj()
            tmp.parent = self.current
            self.current.right = tmp
            self.current = self.current.right
