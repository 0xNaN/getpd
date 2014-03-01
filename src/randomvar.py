import random

class RandomVar:
    """A simple class to handle Random Variable.
    """

    name = None
    samples = None
    weights = None

    _dmf = None
    _tot_weight = 0

    def __init__(self, name = ''):
        """Init a new Random Variable.

        Arguments:
        name -- a name for the Random Variable
        """
        self.name = name

        self.samples = []
        self.weights = []
        self._dmf = []

    def add(self, value, weight = 1):
        """Add a weighted value to the Random Variable.

        Arguments:
        value  -- the value to add (or refer to, if it is
                  already present)
        weight -- the weight of this addition
        """
        n_samples = len(self.samples)

        try:
            i = self.samples.index(value)
            self.weights[i] += weight
        except ValueError:
            self.samples.insert(n_samples, value)
            self.weights.insert(n_samples, 1)
            self._dmf.insert(n_samples, None)

        self._tot_weight += weight

    def value(self):
        """Simulate the Random Variable.

        Return:
        A sample, result of the simultaion
        """
        rnd = random.randint(0, self._tot_weight - 1)

        n_samples = len(self.samples)
        lower = 0
        for i in range(n_samples):
            upper = lower + self.weights[i] - 1
            if(lower <= rnd <= upper):
                return self.samples[i]
            lower = upper + 1

    def dmf(self, accurancy=16, verbosity=False):
        """Generate the Distribution Mass Function (DMF).

        Return:
        A list where the i-th element contains the
        probability to obtaining the i-th sample in
        the Samples list.
        """
        n_samples = len(self.samples)
        dmf = []
        for i in range(n_samples):
            p = self.weights[i]/self._tot_weight
            self._dmf[i] = round(p, accurancy)

            elem = p
            if verbosity:
                elem = str(samples[i]) + ":" + str(p)
            dmf.insert(i, elem)
        return dmf

    def __int__(self):
        return int(self.value())

    def __str__(self):
        return str(self.value())

    def __float__(self):
        return float(self.value())
