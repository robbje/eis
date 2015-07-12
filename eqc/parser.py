#!/usr/bin/env python2
import ply.lex as lex

class Node(object):
    def __init__(self):
        self.right = None
        self.left = None
        self.value = None
        self.parent = None
    def is_terminal(self):
        return self.value.type == 'SYMBOL'
    def __str__(self):
        if not self.value: return "None"
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
        self.lexer = lex.lex(object=self)
        self.nodeobj = nodeobj
    def parse(self, string):
        self.lexer.input(string)
        self.root = self.nodeobj()
        self.current = self.root
        self.indent = 0
        while True:
            t = self.lexer.token()
            if not t: break
            self.handleToken(t)
        return self.root

    def handleToken(self,t):
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
            # It is an error if that leaf exists, because then a symbol
            # was followed by a parenthesis
            self.indent += 1
            if self.current.left:
                raise Exception("Unexpected parenthesis at pos %i" % t.lexpos)
            self.current.left = self.nodeobj()
            self.current.left.parent = self.current
            self.current = self.current.left
        elif t.type == 'RPAREN':
            # Right parenthesis
            # Decrease indentation level. It is an error if it drops negative.
            # If the right leaf doesn't exist yet, collapse current node
            self.indent -= 1
            if self.indent < 0:
                raise Exception("Unbalanced parenthesis at pos %i" % t.lexpos)
            #if not self.current.right:
            #    # TODO: There is a bug here, triggered by '()'
            #    self.current.value = self.current.left.value
            #    self.current.left = None
            #    if not self.current.parent:
            #        raise Exception("How did you do that?")
            #    self.current = self.current.parent
        elif t.type in ['SERIES','PARALLEL']:
            # Series or parallel token
            # If the current node has a value, we need to make a new root.
            # If not, set this nodes value to the operator and move to
            # the right leaf. It is an error if we don't have a left leaf.
            if not self.current.left:
                raise Exception("Syntax error at pos %i" % t.lexpos)
            if self.current.value:
                tmp = self.nodeobj()
                tmp.value = t
                self.current.parent = tmp
                tmp.left = self.current
                self.root = tmp
                self.current = tmp
            else:
                self.current.value = t
            self.current.right = self.nodeobj()
            self.current.right.parent = self.current
            self.current = self.current.right

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print "Usage: %s [string]"
        sys.exit(0)
    p = Parser(Node)
    print p.parse(sys.argv[1])
