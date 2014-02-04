import re

class Rule:
    """ A class to handle Rule as pair of RegEX and Slice object. """
    _regex = ""
    _slice = None

    def __init__(self, rule):
        if not self._checkPattern(rule):
            raise ValueError('Malformed Rule')

        self._regex = self._regexFromRule(rule)
        self._slice = self._sliceFromRule(rule)

        if not self._isRegexCorrect(self._regex):
            raise ValueError('Malformed RegEX')

    def _regexFromRule(self, rule):
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

        # split slice_data to find start, stop and step
        slice_data = slice_data.split(':')

        # convert slice_data to int
        slice_data = self._stringIndexToInt(slice_data)

        # assign index to right var
        ntoken = len(slice_data)

        if ntoken == 1:
            # if only an arg given, it is 'stop'
            # with, or without, colon symbol
            stop = slice_data[0]
        elif ntoken == 2:
            # start and stop, [:]
            start = slice_data[0]
            stop = slice_data[1]
        elif ntoken == 3:
            # start, stop and step [::]
            start = slice_data[0]
            stop = slice_data[1]
            step = slice_data[2]
            # step must != 0
            if step == 0: step = 1
        elif ntoken > 3:
            raise ValueError('Malformed Slice: too args')

        return slice(start, stop, step)

    def _checkPattern (self, rule):
        """ Check if a Rule has the correct form as [][x:x:x] """
        match = re.match('^\[.*\]\[[0-9:+-]*\]$', rule)

        if match:
            return True
        return False

    def _isRegexCorrect(self, regex):
        """ Check if a regex is compilable. """
        correct = True
        try:
            re.compile(regex)
        except:
            correct = False
        return correct

    def _stringIndexToInt(self, indexes):
        """ Cast a list of string index to a list of int index.

            N.B: If an index is equal to '' it is considered 0.
        """
        for i in range(0, len(indexes)):
            try:
                if indexes[i] == '':
                    indexes[i] = 0
                else:
                    indexes[i] = int(indexes[i])
            except:
                raise ValueError('Malformed Slice: check value')
        return indexes

