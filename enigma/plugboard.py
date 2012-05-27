# Copyright (C) 2012 by Brian Neal.
# This file is part of Py-Enigma, the Enigma Machine simulation.
# Py-Enigma is released under the MIT License (see License.txt).

"""Contains the Plugboard class for simulating the plugboard component."""

import collections
import string


# Like the keyboard, the plugboard has plugs for each upper case letter of the
# alphabet:
PLUGBOARD_LABELS = string.ascii_uppercase

# The number of plugboard cables supplied with a machine:
MAX_PAIRS = 10


class PlugboardError(Exception):
    pass


class Plugboard:
    """The plugboard allows the operator to swap letters before and after the
    entry wheel. This is accomplished by connecting cables between pairs of
    plugs that are marked with letters. Ten cables were issued with each
    machine; thus up to 10 of these swappings could be used as part of a machine
    setup.

    Each cable swaps both the input and output signals. Thus if A is connected
    to B, A crosses to B in the keyboard to entry wheel direction and also in
    the entry wheel to lamp direction.

    """

    def __init__(self, settings=''):
        """Configure the plugboard according to a settings string:

        settings - a string consisting of pairs of letters separated by
        whitespace. This is the format used in the key sheets (code books) to
        specify daily settings for the Enigma Machine.
        E.g. 'PO ML IU KJ NH YT GB VF RE DC' 

        To specify no plugboard connections, settings can be None or an empty
        string.

        A PlugboardError will be raised if the settings string is invalid, or if
        it contains more than MAX_PAIRS pairs. Each plug should be present at
        most once in the settings string.

        """
        # construct wiring mapping table with default 1-1 mappings
        self.wiring_map = list(range(len(PLUGBOARD_LABELS)))

        # use settings if provided
        self.settings = []
        pairs = settings.split() if settings is not None else []

        if len(pairs) > MAX_PAIRS:
            raise PlugboardError('too many connections')
        elif len(pairs) == 0:
            return      # we are done, no mappings to perform

        # convert to upper case
        pairs = [pair.upper() for pair in pairs]

        # validate pairings
        for pair in pairs:
            if len(pair) != 2:
                raise PlugboardError('invalid pair length: %s' % pair)
            for c in pair:
                if c not in PLUGBOARD_LABELS:
                    raise PlugboardError('invalid letter: %s' % c)
        
        # validate each letter appears at most once
        counter = collections.Counter(''.join(pairs))
        letter, count = counter.most_common(1)[0]
        if count != 1:
            raise PlugboardError('duplicate connection: %s' % letter)

        # settings seems valid, make the internal wiring changes now:
        for pair in pairs:
            m, n = ord(pair[0]) - ord('A'), ord(pair[1]) - ord('A')
            self.wiring_map[m] = n
            self.wiring_map[n] = m

        self.settings = ' '.join(pairs)

    def signal(self, n):
        """Simulate a signal entering the plugboard on wire n, where n must be
        an integer between 0 and 25.

        Returns the wire number of the output signal (0-25).

        Note that since the plugboard always crosses pairs of wires, it doesn't
        matter what direction (keyboard -> entry wheel or vice versa) the signal
        is coming from.

        """
        return self.wiring_map[n]
