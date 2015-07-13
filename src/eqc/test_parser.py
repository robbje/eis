#!/usr/bin/env python2

import unittest

from parser import Node, Parser

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser(Node)
    def testParsetree(self):
        # Test some non-ambiguous examples
        testcases = {
            'R+R':'+(R, R)',
            'R|C':'|(R, C)',
            'R+(R|C)':'+(R, |(R, C))',
            'R_1+R_2':'+(R_1, R_2)',
            'R_longname|R':'|(R_longname, R)',
            'R+(R|C)+(R|L)+(R|L)+Warb': \
                '+(+(+(+(R, |(R, C)), |(R, L)), |(R, L)), Warb)',
        }
        for case in testcases:
            a = str(self.parser.parse(case))
            b = testcases[case]
            self.assertEqual(a,b,msg=case)
    def tearDown(self):
        self.parser = None

suite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
unittest.TextTestRunner(verbosity=2).run(suite)
