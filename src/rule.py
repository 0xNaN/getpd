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
            # step shuldn't equal to 0
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


