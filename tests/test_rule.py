import sys, unittest


sys.path.insert(0, '../src')

from rule import Rule

class RuleTests(unittest.TestCase):

    #def setUp(self):

    def testGiveCompleteCorrectRule(self):
        rule = Rule("[..][1:2:3]")

        self.assertEqual("..", rule._regex)

        self.assertEqual(slice, type(rule._slice))
        self.assertEqual('1', rule._slice.start)
        self.assertEqual('2', rule._slice.stop)
        self.assertEqual('3', rule._slice.step)

    def testGiveCorrectRuleWithoutStep(self):
        rule = Rule("[..][1:2]")

        self.assertEqual("..", rule._regex)

        self.assertEqual(slice, type(rule._slice))
        self.assertEqual('1', rule._slice.start)
        self.assertEqual('2', rule._slice.stop)

    def testWithSomeFormOfCorrectSlice(self):
        rule = Rule("[][1:]")

def main():

    # Make the test suite & load all tests
    suite = unittest.TestSuite()

    loader = unittest.TestLoader()
    rangeTests = loader.loadTestsFromTestCase(RuleTests)

    suite.addTests(rangeTests)

    # Run tests
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    main()
