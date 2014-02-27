import regex as re

from randvar import RandVar

class Rule:
    """ A class to handle Rule as pair of RegEX and Slice object. """
    rndvars = None

    _regex = None
    _slice = None

    # A string copy of the regex
    re_pattern = ""

    buff = ""

    def __init__(self, rule):
        if not self._checkPattern(rule):
            raise ValueError('Malformed Rule')

        self.re_pattern = self._patternFromRule(rule)

        self._slice = self._sliceFromRule(rule)
        self._regex = self._regexFromPattern(self.re_pattern)

        if not self._regex:
            raise ValueError('Malformed RegEX')
        self.rndvars = []

    def _patternFromRule(self, rule):
        """ Get the RegEX inside a rule. """
        rule = rule[1:-1].rsplit('][')
        return rule[0]

    def _sliceFromRule(self, rule):
        """ Build a slice object from a Rule.

            N.B: In according to slice class, if a slice
            is build only with an args it is the 'stop' value.
        """

        start = stop = step = None

        # split Slice from Rule, obataining: x:x:x
        slice_data = rule[1:-1].rsplit('][')
        slice_data = slice_data[1]

        # Make a list of int indexes
        slice_data = slice_data.split(':')
        slice_data = self._stringIndexToInt(slice_data)

        # assign indexes to right var
        ntoken = len(slice_data)
        if ntoken == 1:
            # When there is only an arg it describe a single
            # index. Such as [1], [-1].
            start = slice_data[0]
            if start >= 0:
                step = 1
            else:
                step = -1
            stop = start + step
        elif ntoken == 2:
            # start and stop, [:]
            start = slice_data[0]
            stop = slice_data[1]
        elif ntoken == 3:
            start = slice_data[0]
            stop = slice_data[1]
            step = slice_data[2]

            if step == 0: step = 1
            if(step != None and step < 0):
                raise ValueError("Malformed Slice: negative step doesn't supported")

        elif ntoken > 2:
            raise ValueError('Malformed Slice: too args')

        return slice(start, stop, step)

    def _checkPattern (self, rule):
        """ Check if a Rule has the correct form as [][x:x:x] """
        match = re.match('^\[.*\]\[[0-9:+-]*\]$', rule)

        if match:
            return True
        return False

    def _regexFromPattern(self, regex):
        """ If the regex is compilable return an RegEX object.
            Otherwise Null
        """
        regex_obj = None
        try:
            regex_obj = re.compile(regex)
        except:
            regex_obj = None

        return regex_obj

    def _stringIndexToInt(self, indexes):
        """ Cast a list of string index to a list of int index.

            N.B: If an index is equal to '' it is considered None.
        """
        for i in range(len(indexes)):
            try:
                if indexes[i] == '':
                    indexes[i] = None
                else:
                    indexes[i] = int(indexes[i])
            except:
                raise ValueError('Malformed Slice: check value')
        return indexes

    def sliceUp(self, data):
        """ Apply the Slice object inside the Rule """
        data = data.__getitem__(self._slice)
        return data

    def reverseSliceUp(self, data):
        """ Apply the complementary of the Slice inside the Rule """
        # FUTURE NOTE: indices(int) apply the modulo operator
        # to each index (excluse step) with the length of the data

        # Get the right indices inside data.
        length = len(data)
        start, stop, step = self._slice.indices(length)

        if(step < 0):
            start, stop = stop + 1, start + 1

        reverse = ''
        for i in range(0, length, abs(step)):
            if(i >= start and i < stop):
                reverse += '.'
            else:
                reverse += data[i]
        return reverse

    def searchRnd(self, name):
        for rndvar in self.rndvars:
            if(rndvar.name == name):
                return rndvar
        return None

    def put(self, data):
        self.buff += data

        matches = self._regex.finditer(self.buff, overlapped=True)

        match = None
        for match in matches:
            rnd = self.reverseSliceUp(match.group(0))
            det = self.sliceUp(match.group(0))

            # search rnd in rndvars
            rnd_ref = self.searchRnd(rnd)
            if(rnd_ref == None):
                # Create a new rndvar and add the
                # determination
                rnd = RandVar(rnd)
                rnd.insertValue(det)

                self.rndvars.insert(0, rnd)
            else:
                rnd_ref.insertValue(det)

        if match is not None:
            self.buff = self.buff[match.end(0) - 1:]
