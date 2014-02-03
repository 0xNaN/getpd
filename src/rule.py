import re

"""
A class to handle Rule as pair of RegEX and Interval
"""
class Rule:
    _regex = ""
    _slice = None

    def __init__(self, strrule):

        if not self._checkPattern(strrule):
            raise 'Malformed Rule'

        self._regex = self._regexFromRule(strrule)
        self._slice = self._sliceFromRule(strrule)

        if not self._isCorrectRegex(self._regex):
            raise 'Malformed RegEX'

    def _regexFromRule(self, strrule):
        """ Get the RegEX inside a rule """

        rule = strrule[1:-1].rsplit('][')

        return rule[0]

    def _sliceFromRule(self, strrule):
        """ Build a slice object from a Rule """

        start = None
        stop = None
        step = None

        # split Interval from Rule, obataining: x:x:x
        slicedata = strrule[1:-1].rsplit('][')
        slicedata = slicedata[1]

        # find start, stop and step
        slicedata = slicedata.split(':')

        #
        try:
            start = slicedata[0]
            stop = slicedata[1]
            step = slicedata[2]
        except:
            if start == None and stop == None:
                raise 'Malformed Interval'
        return slice(start, stop, step)



    def _checkPattern (self, strrule):
        """ Check if a Rule has a correct form """

        match = re.match('^\[.*\]\[[0-9:+-]*\]', strrule)

        if match:
            return True
        return False

    def _isCorrectRegex(self, regex):
        """ Compile a RegEX to check if it is correct """
        correct = False

        try:
            re.compile(regex)
            correct = True
        except re.error as E:
            correct = False

        return correct


