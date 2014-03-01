import regex

from randomvar import RandomVar

class Rule:
    """A class to perform On-Line statistical analisys through
    a RegEX and a Slice Object.
    """

    rndvars = None
    buff = ""

    _regex = None
    _slice = None

    def __init__(self, re, sl):
        """Init a Rule Object.

        Arguments:
            re -- a string Regular Expression
            sl -- a string Slice
        """
        self.rndvars = []
        self._slice = self._slice_from_str(sl)
        self._regex = self._regex_from_str(re)


    def search_rndvar(self, name):
        """Search a specific Random Variable inside the list
        of all the Random Variables created.

        Arguments:
            name -- the name of the Random Variable to search
        Return:
            A reference to the Random Variable found, otherwise
            None
        """
        for rndvar in self.rndvars:
            if rndvar.name == name:
                return rndvar
        return None

    def put(self, data):
        """Put data inside the buffer of the rule and compute it.

        Arguments:
            data -- An information to add to the current buffer of
                    the rule
        """
        self.buff += data

        matches = self._regex.finditer(self.buff, overlapped=True)
        match = None
        for match in matches:
            # Name of this Random Var & Determination
            rnd = self._fill_slice(match.group(0))
            det = self._apply_slice(match.group(0))

            rnd_ref = self.search_rndvar(rnd)
            if(rnd_ref == None):
                rnd = RandomVar(rnd)
                self.rndvars.insert(0, rnd)
                rnd_ref = self.rndvars[0]
            rnd_ref.add(det)
        # Remove the used data
        if match is not None:
            start = match.end(0) - 1
            self.buff = self.buff[start:]

    def result(self, accurancy=16, verbosity=True):
        """Get a string that contains the result of the analisys.

        Arguments:
            accurancy -- an integer to specify the digit of the
                         frequencies
            verbosity -- a boolean if true each frequnce has the
                         symbol to which it refers
        Return:
            A string contains the formatted result
        """
        res = ""
        for rnd in self.rndvars:
            dmf = rnd.dmf(accurancy, verbosity)
            res += rnd.name + ":\t" + str(dmf) + "\n"
        return res

    def _slice_from_str(self, sl):
        """Build a slice object from a string.

        Arguments:
            sl -- string rappresentation of a Slice
                  i.e '1:2:1', '-1', '1:'
        Returns:
            A Slice object
        """
        if(sl == None or sl == ""):
            raise ValueError("Malformed Slice")

        start = stop = step = None

        # Make a list of int indexes
        sl = sl.split(':')
        sl = self._slist_to_int(sl)

        ntoken = len(sl)
        if ntoken > 3:
            raise ValueError("Malformed Slice: too args")
        elif ntoken == 1:
            # Only index. Such as [-1]
            start = sl[0]
            step = 1 if start >= 0 else -1
            stop = start + step
        elif ntoken == 2:
            # Start and stop. Such as [1:2]
            start = sl[0]
            stop = sl[1]
        elif ntoken == 3:
            # Start, Stop and Step. Such as [1:2:1]
            start = sl[0]
            stop = sl[1]
            step = sl[2] if sl[2] is not 0 else 1

            if(step != None and step < 0):
                raise ValueError("Malformed Slice: negative "
                                 "step doesn't supported")

        return slice(start, stop, step)

    def _regex_from_str(self, re):
        """Compile a regex and return a reference to it.

        Arguments:
            re -- the string regular expression
        Return:
            A reference to a regex compilated.
            If the string is uncompilable raise an Exception
        """
        regex_obj = None
        try:
            regex_obj = regex.compile(re)
        except regex.error:
            raise ValueError("Malformed regex: Uncompilable")
        return regex_obj

    def _slist_to_int(self, str_list):
        """Cast a list of string index to a list of int index.
        Note that '' is consired None

        Arguments:
            str_list -- the string list to convert

        Return:
            a new list contains the casted index
        """
        int_list = []
        for c in str_list:
            try:
                n = None if c is '' else int(c)
                int_list.append(n)
            except ValueError:
                raise ValueError('Malformed Slice: check value')
        return int_list

    def _apply_slice(self, data):
        """Apply the Slice object inside the Rule to a data.

        Arguments:
            data -- the data to be sliced
        Returns:
            the data sliced
        """
        return data.__getitem__(self._slice)

    def _fill_slice(self, data, symbol='.'):
        """Fill the portion of data inside the Slice obj with a
        symbol.
        i.e: Assuming the Slice 2:4, _fill_slice('hello') --> 'he..o'

        Argumets:
            data -- the data to be filled
            symbol -- the symbol to use (Default '.')
        Return:
            The string filled
        """
        # FUTURE NOTE: indices(int) apply the mod to each index
        # (but not step) with the arg passed
        length = len(data)
        start, stop, step = self._slice.indices(length)

        if(step < 0):
            # Negative step are useless in statistical purpose.
            # So a negative step indicate an index rather than
            # a slice, i.e [-1] --> slice(-1, -2, -1)
            start, stop = stop + 1, start + 1

        step = abs(step)
        filled = ''
        for i in range(0, length, step):
            if(start <= i < stop):
                filled += '.'
            else:
                filled += data[i]
        return filled
