import sys
import unittest
import regex as re

sys.path.insert(0, '../src')

from rule import Rule
from randvar import RandVar

class RuleTests(unittest.TestCase):

    def testGiveCompleteCorrectRule(self):
        rule = Rule("[..][1:2:3]")

        self.assertEqual("..", rule.re_pattern)
        # XXX: a better way to know the type ??
        self.assertIsInstance(rule._regex, type(re.compile('')))

        self.assertIsInstance(rule._slice, slice)
        self.assertEqual(1, rule._slice.start)
        self.assertEqual(2, rule._slice.stop)
        self.assertEqual(3, rule._slice.step)

    def testMalformedRule(self):
        # Incorrect form
        self.assertRaises(ValueError, Rule, "[]")
        self.assertRaises(ValueError, Rule, "[][")
        self.assertRaises(ValueError, Rule, "xxx")

        # Not allowed char in Slice
        self.assertRaises(ValueError, Rule, "[xx][x]")
        self.assertRaises(ValueError, Rule, "[xx][/1]")

    def testMalformedRegEx(self):
        self.assertRaises(ValueError,  Rule, "[((][1]")
        self.assertRaises(ValueError, Rule, "/")

    def testMalformedSlice(self):
        self.assertRaises(ValueError, Rule, "[.][a]")
        self.assertRaises(ValueError, Rule, "[.][+-1:]")
        self.assertRaises(ValueError, Rule, "[.][a1:b1:c1]")
        self.assertRaises(ValueError, Rule, "[.][+-1]")
        self.assertRaises(ValueError, Rule, "[.][1:2:-1]")

    def testSliceOnlyWithStart(self):
        rule = Rule("[][1:]")
        self.assertEqual(1, rule._slice.start)
        self.assertEqual(None, rule._slice.stop)
        self.assertEqual(None, rule._slice.step)


        rule = Rule("[][-1::]")
        self.assertEqual(-1, rule._slice.start)
        self.assertEqual(None, rule._slice.stop)
        self.assertEqual(None, rule._slice.step)

        rule = Rule("[][:]")
        self.assertEqual(None, rule._slice.start)
        self.assertEqual(None, rule._slice.stop)
        self.assertEqual(None, rule._slice.step)


    def testSliceOnlyWithStop(self):
        rule = Rule("[][:+1]")
        self.assertEqual(None, rule._slice.start)
        self.assertEqual(1, rule._slice.stop)
        self.assertEqual(None, rule._slice.step)


        rule = Rule("[][:-1:]")
        self.assertEqual(None, rule._slice.start)
        self.assertEqual(-1, rule._slice.stop)
        self.assertEqual(None, rule._slice.step)


    def testSliceOnlyWithStep(self):
        # Negative step doesn't supported
        # useless for statistical purposes

        rule = Rule("[][::]")
        self.assertEqual(None, rule._slice.start)
        self.assertEqual(None, rule._slice.stop)
        self.assertEqual(None, rule._slice.step)

        rule = Rule("[][::+1]")
        self.assertEqual(None, rule._slice.start)
        self.assertEqual(None, rule._slice.stop)
        self.assertEqual(1, rule._slice.step)

    def testSliceSuchAsIndex(self):
        # An index can be described through a
        # Slice Object".
        # For negative index is necessary a
        #  negative steps

        rule = Rule("[][1]")
        self.assertEqual(1, rule._slice.start)
        self.assertEqual(2, rule._slice.stop)
        self.assertEqual(1, rule._slice.step)

        rule = Rule("[][-1]")
        self.assertEqual(-1, rule._slice.start)
        self.assertEqual(-2, rule._slice.stop)
        self.assertEqual(-1, rule._slice.step)

    def testSliceObject(self):
        s = "lorem"

        rule = Rule("[][-1]")
        self.assertEqual(s[-1], rule.sliceUp(s))

        rule = Rule("[][+3]")
        self.assertEqual(s[3], rule.sliceUp(s))

        rule = Rule("[][:-1]")
        self.assertEqual(s[:-1], rule.sliceUp(s))

        rule = Rule("[][3:5:2]")
        self.assertEqual(s[3:5:2], rule.sliceUp(s))

        rule = Rule("[][:-4:1]")
        self.assertEqual(s[:-4:1], rule.sliceUp(s))

    def testReverseSliceUp(self):
        s = "lorem"

        rule = Rule("[][-1]")
        self.assertEqual("lore.", rule.reverseSliceUp(s))

        rule = Rule("[][-3]")
        self.assertEqual("lo.em", rule.reverseSliceUp(s))

        rule = Rule("[][1:4]")
        self.assertEqual("l...m", rule.reverseSliceUp(s))

        rule = Rule("[][1:4:2]")
        self.assertEqual("l.m", rule.reverseSliceUp(s))

    def testSearchRnd(self):
        rule = Rule("[(ab).][-1]")

        self.assertEqual(None, rule.searchRnd(''))

        # Manual populations of the rndvars array
        # of the aspecting result with this data:
        # "a1b1a2"
        rule.rndvars.insert(0, RandVar('a.'))
        rule.rndvars[0].insertValue(1)
        rule.rndvars[0].insertValue(2)

        rule.rndvars.insert(0, RandVar('b.'))
        rule.rndvars[0].insertValue(1)

        rndvar = rule.searchRnd('a.')
        self.assertEqual('a.', rndvar.name)
        self.assertEqual(2, rndvar.total_weight)

        rndvar = rule.searchRnd('b.')
        self.assertEqual('b.', rndvar.name)
        self.assertEqual(1, rndvar.total_weight)


    def testPutWithOneRndVar(self):
        rule = Rule("[t.][-1]")

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
        self.assertEqual(5, len(rndvar.samples_space))

        for w in rndvar.samples_weight:
            self.assertEqual(1, w)

        # The frequences are 1/5
        rndvar.updateDmf()

        for p in rndvar.dmf:
            self.assertEqual(1/5, p)

    def testPutWithPlusRndVar(self):
        rule = Rule("[..][-1]")

        s = "aabbccddeeff"

        # put a char at once only for fun
        for c in s:
            rule.put(c)

        self.assertEqual(6, len(rule.rndvars))

        # frequencies check
        rndvars = rule.rndvars
        for rnd in rndvars:
            rnd.updateDmf()

        self.assertEqual('f.', rndvars[0].name)
        self.assertEqual(1, rndvars[0].dmf[0]) #ff

        self.assertEqual('e.', rndvars[1].name)
        self.assertEqual(1/2, rndvars[1].dmf[0]) #ee
        self.assertEqual(1/2, rndvars[1].dmf[1]) #ef

        self.assertEqual('d.', rndvars[2].name)
        self.assertEqual(1/2, rndvars[2].dmf[0]) #dd
        self.assertEqual(1/2, rndvars[2].dmf[1]) #de

        self.assertEqual('c.', rndvars[3].name)
        self.assertEqual(1/2, rndvars[3].dmf[0]) #cc
        self.assertEqual(1/2, rndvars[3].dmf[1]) #cd

        self.assertEqual('b.', rndvars[4].name)
        self.assertEqual(1/2, rndvars[4].dmf[0]) #bb
        self.assertEqual(1/2, rndvars[4].dmf[1]) #bc

        self.assertEqual('a.', rndvars[5].name)
        self.assertEqual(1/2, rndvars[5].dmf[0]) #aa
        self.assertEqual(1/2, rndvars[5].dmf[1]) #ab

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
