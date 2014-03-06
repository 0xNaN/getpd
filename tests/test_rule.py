import sys
import unittest
import regex

sys.path.insert(0, '../src')

from rule import Rule
from randomvar import RandomVar

class RuleTests(unittest.TestCase):

    def testGiveCompleteCorrectRule(self):
        rule = Rule("..", "1:2:3")

        self.assertIsInstance(rule._regex, type(regex.compile('')))
        self.assertEqual("..", rule._regex.pattern)

        self.assertIsInstance(rule._slice, slice)
        self.assertEqual(1, rule._slice.start)
        self.assertEqual(2, rule._slice.stop)
        self.assertEqual(3, rule._slice.step)

    def testMalformedRule(self):
        # Incorrect form
        self.assertRaises(ValueError, Rule, None, None)
        self.assertRaises(ValueError, Rule, "", None)
        self.assertRaises(ValueError, Rule, None, "")

        # Not allowed char in Slice
        self.assertRaises(ValueError, Rule, ".", "a")
        self.assertRaises(ValueError, Rule, ".", "/1")

    def testMalformedRegEx(self):
        self.assertRaises(ValueError,  Rule, "((", "1")

    def testMalformedSlice(self):
        self.assertRaises(ValueError, Rule, ".","a")
        self.assertRaises(ValueError, Rule, ".","+-1:")
        self.assertRaises(ValueError, Rule, ".","a1:b1:c1")
        self.assertRaises(ValueError, Rule, ".","1:2:-1")

    def testSliceOnlyWithStart(self):
        rule = Rule("", "1:")
        self.assertEqual(1, rule._slice.start)
        self.assertEqual(None, rule._slice.stop)
        self.assertEqual(None, rule._slice.step)


        rule = Rule("", "-1::")
        self.assertEqual(-1, rule._slice.start)
        self.assertEqual(None, rule._slice.stop)
        self.assertEqual(None, rule._slice.step)

        rule = Rule("", ":")
        self.assertEqual(None, rule._slice.start)
        self.assertEqual(None, rule._slice.stop)
        self.assertEqual(None, rule._slice.step)


    def testSliceOnlyWithStop(self):
        rule = Rule("", ":+1")
        self.assertEqual(None, rule._slice.start)
        self.assertEqual(1, rule._slice.stop)
        self.assertEqual(None, rule._slice.step)


        rule = Rule("", ":-1:")
        self.assertEqual(None, rule._slice.start)
        self.assertEqual(-1, rule._slice.stop)
        self.assertEqual(None, rule._slice.step)


    def testSliceOnlyWithStep(self):
        # Negative step doesn't supported
        # useless for statistical purposes

        rule = Rule("", "::")
        self.assertEqual(None, rule._slice.start)
        self.assertEqual(None, rule._slice.stop)
        self.assertEqual(None, rule._slice.step)

        rule = Rule("", "::+1")
        self.assertEqual(None, rule._slice.start)
        self.assertEqual(None, rule._slice.stop)
        self.assertEqual(1, rule._slice.step)

    def testSliceSuchAsIndex(self):
        # An index can be described through a
        # Slice Object".
        # For negative index is necessary a
        #  negative steps

        rule = Rule("", "1")
        self.assertEqual(1, rule._slice.start)
        self.assertEqual(2, rule._slice.stop)
        self.assertEqual(1, rule._slice.step)

        rule = Rule("", "-1")
        self.assertEqual(-1, rule._slice.start)
        self.assertEqual(-2, rule._slice.stop)
        self.assertEqual(-1, rule._slice.step)

    def testSlice(self):
        s = "lorem"

        rule = Rule("", "-1")
        self.assertEqual(s[-1], rule._apply_slice(s))

        rule = Rule("", "+3")
        self.assertEqual(s[3], rule._apply_slice(s))

        rule = Rule("", ":-1")
        self.assertEqual(s[:-1], rule._apply_slice(s))

        rule = Rule("", "3:5:2")
        self.assertEqual(s[3:5:2], rule._apply_slice(s))

        rule = Rule("", ":-4:1")
        self.assertEqual(s[:-4:1], rule._apply_slice(s))

    def testFillSlice(self):
        s = "lorem"

        rule = Rule("", "-1")
        self.assertEqual("lore.", rule._fill_slice(s))

        rule = Rule("", "-3")
        self.assertEqual("lo.em", rule._fill_slice(s))

        rule = Rule("", "1:4")
        self.assertEqual("l...m", rule._fill_slice(s))

        rule = Rule("", "1:4:2")
        self.assertEqual("l.m", rule._fill_slice(s))

    def testSearchRndvar(self):
        rule = Rule("(ab).","-1")

        self.assertEqual(None, rule.search_rndvar(''))

        # Manual populations of the rndvars array
        # of the aspecting result with this data:
        # "a1b1a2"
        rule.rndvars.insert(0, RandomVar('a.'))
        rule.rndvars[0].add(1)
        rule.rndvars[0].add(2)

        rule.rndvars.insert(0, RandomVar('b.'))
        rule.rndvars[0].add(1)

        rndvar = rule.search_rndvar('a.')
        self.assertEqual('a.', rndvar.name)
        self.assertEqual(2, rndvar._tot_weight)

        rndvar = rule.search_rndvar('b.')
        self.assertEqual('b.', rndvar.name)
        self.assertEqual(1, rndvar._tot_weight)


    def testPutWithOneRndVar(self):
        rule = Rule("t.", "-1")

        s = "this text contains 5 't.'"

        rule.put(s[:5])
        rule.put(s[5:])

        # The rndvars array should contains
        # only ONE randvar.
        # This has only 5 different determinations:
        # 'h', 'e', 'a', ' ', '.'

        self.assertEqual(1, len(rule.rndvars))
        self.assertEqual('t.', rule.rndvars[0].name)

        rndvar = rule.rndvars[0]
        self.assertEqual(5, len(rndvar.samples))

        for w in rndvar.weights:
            self.assertEqual(1, w)

        # The frequences are 1/5
        dmf = rndvar.dmf()

        for p in dmf:
            self.assertEqual(1/5, p)

    def testPutWithPlusRndVar(self):
        rule = Rule("..","-1")

        s = "aabbccddeeff"

        # put a char at once only for fun
        for c in s:
            rule.put(c)

        self.assertEqual(6, len(rule.rndvars))

        # frequencies check
        rndvars = rule.rndvars
        for rnd in rndvars:
            rnd.dmf()

        self.assertEqual('f.', rndvars[0].name)
        self.assertEqual(1, rndvars[0]._dmf[0]) #ff

        self.assertEqual('e.', rndvars[1].name)
        self.assertEqual(1/2, rndvars[1]._dmf[0]) #ee
        self.assertEqual(1/2, rndvars[1]._dmf[1]) #ef

        self.assertEqual('d.', rndvars[2].name)
        self.assertEqual(1/2, rndvars[2]._dmf[0]) #dd
        self.assertEqual(1/2, rndvars[2]._dmf[1]) #de

        self.assertEqual('c.', rndvars[3].name)
        self.assertEqual(1/2, rndvars[3]._dmf[0]) #cc
        self.assertEqual(1/2, rndvars[3]._dmf[1]) #cd

        self.assertEqual('b.', rndvars[4].name)
        self.assertEqual(1/2, rndvars[4]._dmf[0]) #bb
        self.assertEqual(1/2, rndvars[4]._dmf[1]) #bc

        self.assertEqual('a.', rndvars[5].name)
        self.assertEqual(1/2, rndvars[5]._dmf[0]) #aa
        self.assertEqual(1/2, rndvars[5]._dmf[1]) #ab

    def testResult(self):
        r = Rule("..", "-1")
        s = "aaabbccddeeff"
        r.put(s)

        r1 = "f.:\t['f:1.0']\n"\
             "e.:\t['e:0.5', 'f:0.5']\n"\
             "d.:\t['d:0.5', 'e:0.5']\n"\
             "c.:\t['c:0.5', 'd:0.5']\n"\
             "b.:\t['b:0.5', 'c:0.5']\n"\
             "a.:\t['a:0.6666666666666666', 'b:0.3333333333333333']"
        self.assertEqual(r1, r.result())

        r2 = "f.:\t[1.0]\n"\
             "e.:\t[0.5, 0.5]\n"\
             "d.:\t[0.5, 0.5]\n"\
             "c.:\t[0.5, 0.5]\n"\
             "b.:\t[0.5, 0.5]\n"\
             "a.:\t[0.6666666666666666, 0.3333333333333333]"
        self.assertEqual(r2, r.result(verbosity=False))

        r3 = "f.:\t[1.0]\n"\
             "e.:\t[0.5, 0.5]\n"\
             "d.:\t[0.5, 0.5]\n"\
             "c.:\t[0.5, 0.5]\n"\
             "b.:\t[0.5, 0.5]\n"\
             "a.:\t[0.7, 0.3]"
        self.assertEqual(r3, r.result(1, verbosity=False))

def main():

    # Make the test suite & load all tests
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    ruleTests = loader.loadTestsFromTestCase(RuleTests)

    suite.addTests(ruleTests)

    # Run tests
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    main()
