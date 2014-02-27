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
        rule = Rule("[][::-1]")
        self.assertEqual(None, rule._slice.start)
        self.assertEqual(None, rule._slice.stop)
        self.assertEqual(-1, rule._slice.step)


        rule = Rule("[][::]")
        self.assertEqual(None, rule._slice.start)
        self.assertEqual(None, rule._slice.stop)
        self.assertEqual(None, rule._slice.step)

        rule = Rule("[][::+1]")
        self.assertEqual(None, rule._slice.start)
        self.assertEqual(None, rule._slice.stop)
        self.assertEqual(1, rule._slice.step)

    def testSliceSuchAsIndex(self):
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

        rule = Rule("[][3:5:-1]")
        self.assertEqual(s[3:5:-1], rule.sliceUp(s))

        rule = Rule("[][:-4:-1]")
        self.assertEqual(s[:-4:-1], rule.sliceUp(s))

    def testReverseSliceUp(self):
        s = "lorem"

        rule = Rule("[][1:4]")
        self.assertEqual("l...m", rule.reverseSliceUp(s))

        rule = Rule("[][-2:-4:-1]")
        self.assertEqual("m..ol", rule.reverseSliceUp(s))

        rule = Rule("[][1:4:2]")
        self.assertEqual("l.m", rule.reverseSliceUp(s))

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
