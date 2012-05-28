# Copyright (C) 2012 by Brian Neal.
# This file is part of Py-Enigma, the Enigma Machine simulation.
# Py-Enigma is released under the MIT License (see License.txt).

"""Contains the Plugboard class for simulating the plugboard (Steckerbrett)
component of the Enigma Machine.

"""

import collections
from itertools import chain
import string


# On Heer & Luftwaffe (?) models, the plugs are labeled with upper case letters
HEER_LABELS = string.ascii_uppercase

# The number of plugboard cables supplied with a machine:
MAX_PAIRS = 10


class PlugboardError(Exception):
    pass


class Plugboard:
    """The plugboard allows the operator to swap letters before and after the 
    entry wheel. This is accomplished by connecting cables between pairs of
    plugs that are marked with letters (Heer & Luftwaffe models) or numbers
    (Kriegsmarine). Ten cables were issued with each machine; thus up to 10 of
    these swappings could be used as part of a machine setup.

    Each cable swaps both the input and output signals. Thus if A is connected
    to B, A crosses to B in the keyboard to entry wheel direction and also in
    the reverse entry wheel to lamp direction.

    """
    def __init__(self, wiring_pairs=None):
        """Configure the plugboard according to a list or tuple of integer
        pairs, or None.

        A value of None or an empty list/tuple indicates no plugboard
        connections are to be used (i.e. a straight mapping).

        Otherwise wiring_pairs must be an iterable of integer pairs, where each
        integer is between 0-25, inclusive. At most 10 such pairs can be
        specified. Each value represents an input/output path through the
        plugboard. It is invalid to specify the same path more than once in the
        list.

        If an invalid wiring_pairs parameter is given, a PlugboardError is
        raised.

        """
        # construct wiring mapping table with default 1-1 mappings
        self.wiring_map = list(range(26))

        # use settings if provided
        if not wiring_pairs:
            return

        if len(wiring_pairs) > MAX_PAIRS:
            raise PlugboardError('Please specify %d or less pairs' % MAX_PAIRS)

        # ensure a path occurs at most once in the list
        counter = collections.Counter(chain.from_iterable(wiring_pairs))
        path, count = counter.most_common(1)[0]
        if count != 1:
            raise PlugboardError('duplicate connection: %d' % path)

        # make the connections
        for pair in wiring_pairs:
            m = pair[0]
            n = pair[1]
            if not (0 <= m < 26) or not (0 <= n < 26):
                raise PlugboardError('invalid connection: %s' % str(pair))

            self.wiring_map[m] = n
            self.wiring_map[n] = m

    @classmethod
    def from_key_sheet(cls, settings=None):
        """Configure the plugboard according to a settings string as you may
        find on a key sheet.

        Two syntaxes are supported, the Heer/Luftwaffe and Kriegsmarine styles:

        In the Heer syntax, the settings are given as a string of
        alphabetic pairs. For example: 'PO ML IU KJ NH YT GB VF RE DC' 

        In the Kriegsmarine syntax, the settings are given as a string of number
        pairs, separated by a '/'. Note that the numbering uses 1-26, inclusive.
        For example: '18/26 17/4 21/6 3/16 19/14 22/7 8/1 12/25 5/9 10/15'

        To specify no plugboard connections, settings can be None or an empty
        string.

        A PlugboardError will be raised if the settings string is invalid, or if
        it contains more than MAX_PAIRS pairs. Each plug should be present at
        most once in the settings string.

        """
        if not settings:
            return cls(None)

        wiring_pairs = []
        
        # detect which syntax is being used
        if settings.find('/') != -1:
            # Kriegsmarine syntax
            pairs = settings.split()
            for p in pairs:
                try:
                    m, n = p.split('/')
                    m, n = int(m), int(n)
                except ValueError:
                    raise PlugboardError('invalid pair: %s' % p)

                wiring_pairs.append((m - 1, n - 1))
        else:
            # Heer/Luftwaffe syntax
            pairs = settings.upper().split()

            for p in pairs:
                if len(p) != 2:
                    raise PlugboardError('invalid pair: %s' % p)

                m = p[0]
                n = p[1]
                if m not in HEER_LABELS or n not in HEER_LABELS:
                    raise PlugboardError('invalid pair: %s' % p)

                wiring_pairs.append((ord(m) - ord('A'), ord(n) - ord('A')))

        return cls(wiring_pairs)

    def signal(self, n):
        """Simulate a signal entering the plugboard on wire n, where n must be
        an integer between 0 and 25.

        Returns the wire number of the output signal (0-25).

        Note that since the plugboard always crosses pairs of wires, it doesn't
        matter what direction (keyboard -> entry wheel or vice versa) the signal
        is coming from.

        """
        return self.wiring_map[n]
