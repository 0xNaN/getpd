import random

class RandVar:

    name = None
    samples_space = None
    samples_weight = None
    total_weight = 0

    dmf = None

    def __init__(self, name = ''):
        self.samples_space = []
        self.samples_weight = []
        self.dmf = []
        self.name = name

    def value(self):
        value = None

        n_samples = len(self.samples_weight)
        rnd = random.randint(0, self.total_weight - 1)

        # XXX: Extremely important to check
        low_bound = up_bound = 0
        for i in range(n_samples):
            up_bound = low_bound + self.samples_weight[i] - 1
            if(low_bound <= rnd <= up_bound):
                value = self.samples_space[i]
                break
            low_bound = up_bound + 1

        return value

    def insertValue(self, value):
        try:
            index = self.samples_space.index(value)
            self.samples_weight[index] += 1
        except ValueError:
            self.samples_space.insert(len(self.samples_space), value)
            self.samples_weight.insert(len(self.samples_weight), 1)
            self.dmf.insert(len(self.dmf), None)

        self.total_weight += 1

    def updateDmf(self):
        n_samples = len(self.samples_weight)

        for i in range(n_samples):
            self.dmf[i] = self.samples_weight[i]/self.total_weight

    def __str__(self):
        return str(self.value())

    def __int__(self):
        return int(self.value())

    def __float__(self):
        return float(self.value())

