import sys
import unittest

sys.path.insert(0, '../src')

from randvar import RandVar

class RandVarTests(unittest.TestCase):

    def testNewRandVar(self):
        rnd = RandVar()

        self.assertIsInstance(rnd.samples_space, list)
        self.assertIsInstance(rnd.samples_weight, list)
        self.assertIsInstance(rnd.dmf, list)

        self.assertEqual('', rnd.name)
        self.assertEqual(0, len(rnd.samples_space))
        self.assertEqual(0, len(rnd.samples_weight))
        self.assertEqual(0, len(rnd.dmf))

        rnd = randVar('var_name')
        self.assertEqual('var_name', rnd.name)

    def testInsertValue(self):
        rnd = RandVar()

        rnd.insertValue(42)
        rnd.insertValue(24)

        self.assertEqual(42, rnd.samples_space[0])
        self.assertEqual(24, rnd.samples_space[1])

        rnd.insertValue(42)

        self.assertEqual(2, rnd.samples_weight[0])
        self.assertEqual(1, rnd.samples_weight[1])

    def testUpdateDmf(self):
        rnd = RandVar()
        rnd.insertValue(0)
        rnd.insertValue(1)

        rnd.updateDmf()
        self.assertEqual(1/2, rnd.dmf[0])
        self.assertEqual(1/2, rnd.dmf[1])

        rnd.insertValue(0)

        rnd.updateDmf()
        self.assertEqual(2/3, rnd.dmf[0])
        self.assertEqual(1/3, rnd.dmf[1])

    def testTrials(self):
        rnd = RandVar()

        rnd.insertValue(0)
        rnd.insertValue(1)
        rnd.insertValue(1)

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

    randvarTests = loader.loadTestsFromTestCase(RandVarTests)

    suite.addTests(randvarTests)

    # Run tests
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    main()
