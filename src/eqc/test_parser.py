#!/usr/bin/env python2

import unittest

from parser import Node, Parser


class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = Parser(Node)

    def testParsetree(self):
        # Test some non-ambiguous examples
        testcases = [
            ('', 'Empty'),
            ('R', 'R'),
            ('(R|C)+R', '+(|(R, C), R)'),
            ('R+R', '+(R, R)'),
            ('R|C', '|(R, C)'),
            ('R+(R|C)', '+(R, |(R, C))'),
            ('R_1+R_2', '+(R_1, R_2)'),
            ('R_longname|R', '|(R_longname, R)'),
            ('R+(R|C)+(R|L)+(R|L)+Warb',
                '+(+(+(+(R, |(R, C)), |(R, L)), |(R, L)), Warb)')
        ]
        for case, target in testcases:
            result = str(self.parser.parse(case))
            self.assertEqual(result, target, msg='Case "{}": Expected "{}", got "{}"'.format(case, target, result))

    def tearDown(self):
        self.parser = None

suite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
unittest.TextTestRunner(verbosity=2).run(suite)
