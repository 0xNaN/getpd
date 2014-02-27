import sys
import unittest

sys.path.insert(0, '../src')

from randomvar import RandomVar

class RandomVarTests(unittest.TestCase):

    def testNewRandomVar(self):
        rnd = RandomVar()

        self.assertIsInstance(rnd.samples, list)
        self.assertIsInstance(rnd.weights, list)
        self.assertIsInstance(rnd._dmf, list)

        self.assertEqual('', rnd.name)
        self.assertEqual(0, len(rnd.samples))
        self.assertEqual(0, len(rnd.weights))
        self.assertEqual(0, len(rnd._dmf))

        rnd = RandomVar('var_name')
        self.assertEqual('var_name', rnd.name)

    def testAdd(self):
        rnd = RandomVar()

        rnd.add(42)
        rnd.add(24)

        self.assertEqual(42, rnd.samples[0])
        self.assertEqual(24, rnd.samples[1])

        rnd.add(42)

        self.assertEqual(2, rnd.weights[0])
        self.assertEqual(1, rnd.weights[1])

    def testDmf(self):
        rnd = RandomVar()
        rnd.add(0)
        rnd.add(1)

        dmf = rnd.dmf()
        self.assertEqual(1/2, dmf[0])
        self.assertEqual(1/2, dmf[1])

        rnd.add(0)

        dmf = rnd.dmf()
        self.assertEqual(2/3, dmf[0])
        self.assertEqual(1/3, dmf[1])

    def testTrials(self):
        rnd = RandomVar()

        rnd.add(0)
        rnd.add(1)
        rnd.add(1)

        # stupid and simple statistical check
        eps = 1.02
        ntrials = 30000
        c = 0
        for i in range(ntrials):
            if(int(rnd) == 0):
                c += 1
        freq = c/ntrials
        self.assertTrue(freq <= (1/3 * eps))

def main():

    # Make the test suite & load all tests
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    randvarTests = loader.loadTestsFromTestCase(RandomVarTests)

    suite.addTests(randvarTests)

    # Run tests
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    main()
