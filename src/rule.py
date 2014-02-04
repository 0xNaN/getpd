import re

"""
A class to handle Rule as pair of RegEX and Interval
"""
class Rule:
    _regex = ""
    _slice = None

    def __init__(self, strrule):
        """ Build Rule Object """

        if not self._checkPattern(strrule):
            raise ValueError('Malformed Rule')

        self._regex = self._regexFromRule(strrule)
        self._slice = self._sliceFromRule(strrule)

        if not self._isRegexCorrect(self._regex):
            raise ValueError('Malformed RegEX')


    def _regexFromRule(self, strrule):
        """ Get the RegEX inside a rule """

        rule = strrule[1:-1].rsplit('][')

        return rule[0]

    def _sliceFromRule(self, strrule):
        """ Build a slice object from a Rule
            NOTE: In according to slice class, if a slice
            is build only with a value it is the 'stop' value.
        """

        start = stop = step = None

        # split Slice from Rule, obataining: x:x:x
        slicedata = strrule[1:-1].rsplit('][')
        slicedata = slicedata[1]

        # find start, stop and step
        slicedata = slicedata.split(':')
        numtoken = len(slicedata)

        if numtoken > 3:
            raise ValueError('Malformed Slice: too args')

        # Converting in Int, '' must be consider 0
        for i in range(0, numtoken):
            try:
                slicedata[i] = int(slicedata[i])
            except:
                if slicedata[i] == '':
                    slicedata[i] = 0
                else:
                    raise ValueError('Malformed Slice: unallowed char')

        if numtoken == 1:
            # if only an arg given, it is 'stop'
            # with or without colon symbol
            stop = slicedata[0]

        elif numtoken == 2:
            start = slicedata[0]
            stop = slicedata[1]

        elif numtoken == 3:
            start = slicedata[0]
            stop = slicedata[1]
            step = slicedata[2]

            # N.B: step shouldn't be 0! if omitted is 1 or None
            if step == 0: step = 1

        return slice(start, stop, step)



    def _checkPattern (self, strrule):
        """ Check if a Rule has a correct form """

        match = re.match('^\[.*\]\[[0-9:+-]*\]$', strrule)

        if match:
            return True
        return False

    def _isRegexCorrect (self, regex):
        correct = True

        try:
            re.compile(regex)
        except:
            correct = False

        return correct
