# Copyright (C) 2012 by Brian Neal.
# This file is part of Py-Enigma, the Enigma Machine simulation.
# Py-Enigma is released under the MIT License (see License.txt).

"""This module contains the top-level EnigmaMachine class for the Enigma Machine
simulation.

"""
import string

from .rotors.factory import create_rotor, create_reflector
from .plugboard import Plugboard
from .keyfile import get_daily_settings


class EnigmaError(Exception):
    pass

# The Enigma keyboard consists of the 26 letters of the alphabet, uppercase
# only:
KEYBOARD_CHARS = string.ascii_uppercase
KEYBOARD_SET = set(KEYBOARD_CHARS)


class EnigmaMachine:
    """Top-level class for the Enigma Machine simulation."""

    def __init__(self, rotors, reflector, plugboard):
        """Configures the Enigma Machine. Parameters are as follows:

        rotors - a list containing 3 or 4 (for the Kriegsmarine M4 version)
        Rotor objects. The order of the list is important. The first rotor is
        the left-most rotor, and the last rotor is the right-most (from the
        operator's perspective sitting at the machine).

        reflector - a rotor object to represent the reflector (UKW)

        plugboard - a plugboard object to represent the state of the plugboard

        Note that on the military Enigma machines we are simulating, the entry
        wheel is a simple straight-pass through and is not simulated here. It
        would not be too hard to add a parameter for the entry wheel and pass a
        Rotor object for it if it is desired to simulate a non-military Enigma
        machine.

        """
        if len(rotors) not in [3, 4]:
            raise EnigmaError("Must supply 3 or 4 rotors")

        self.rotors = rotors
        self.rotor_count = len(rotors)
        self.reflector = reflector
        self.plugboard = plugboard

    @classmethod
    def from_key_sheet(cls, rotors='I II III', ring_settings=None,
            reflector='B', plugboard_settings=None):

        """Convenience function to build an EnigmaMachine from the data as you
        might find it on a key sheet:

        rotors: either a list of strings naming the rotors from left to right
        or a single string:
            e.g. ["I", "III", "IV"] or "I III IV"

        ring_settings: either a list/tuple of integers, a string, or None to
        represent the ring settings to be applied to the rotors in the rotors
        list. The acceptable values are:
            - A list/tuple of integers with values between 0-25
            - A string; either space separated letters or numbers, e.g. 'B U L'
              or '2 21 12'. If numbers are used, they are 1-based to match
              historical key sheet data.
            - None means all ring settings are 0.

        reflector: a string that names the reflector to use

        plugboard_settings: a string of plugboard settings as you might find
        on a key sheet; e.g. 
            'PO ML IU KJ NH YT GB VF RE DC' 
        or
            '18/26 17/4 21/6 3/16 19/14 22/7 8/1 12/25 5/9 10/15'

            A value of None means no plugboard connections are made.

        """
        # validate inputs
        if isinstance(rotors, str):
            rotors = rotors.split()

        num_rotors = len(rotors)
        if num_rotors not in (3, 4):
            raise EnigmaError("invalid rotors list size")

        if ring_settings is None:
            ring_settings = [0] * num_rotors
        elif isinstance(ring_settings, str):
            strings = ring_settings.split()
            ring_settings = []
            for s in strings:
                if s.isalpha():
                    ring_settings.append(ord(s.upper()) - ord('A'))
                elif s.isdigit():
                    ring_settings.append(int(s) - 1)
                else:
                    raise EnigmaError('invalid ring setting: %s' % s)

        if num_rotors != len(ring_settings):
            raise EnigmaError("# of rotors doesn't match # of ring settings")

        # assemble the machine
        rotor_list = [create_rotor(r[0], r[1]) for r in zip(rotors, ring_settings)]

        return cls(rotor_list, 
                   create_reflector(reflector),
                   Plugboard.from_key_sheet(plugboard_settings))

    @classmethod
    def from_key_file(cls, fp, day=None):
        """Convenience function to read key parameters from a file.

        fp - a file-like object that contains daily key settings
        day - the line labeled with the day number (1-31) will be used for the
        settings. If day is None, the day number will be determined from today's
        date. 

        For more information on the file format, see keyfile.py.

        """
        args = get_daily_settings(fp, day)
        return cls.from_key_sheet(**args)

    def set_display(self, val):
        """Sets the rotor operator windows to 'val'.

        'val' must be a string or iterable containing values for each window
        from left to right.

        """
        if len(val) != self.rotor_count:
            raise EnigmaError("Incorrect length for display value")

        for i, rotor in enumerate(reversed(self.rotors)):
            rotor.set_display(val[-1 - i])

    def get_display(self):
        """Returns the operator display as a string."""

        return "{}{}{}".format(self.rotors[-3].get_display(),
                               self.rotors[-2].get_display(),
                               self.rotors[-1].get_display())

    def key_press(self, key):
        """Simulate a front panel key press. 

        key - a string representing the letter pressed

        The rotors are stepped by simulating the mechanical action of the
        machine. 
        Next a simulated current is run through the machine.
        The lamp that is lit by this key press is returned as a string.

        """
        if key not in KEYBOARD_SET:
            raise EnigmaError('illegal key press %s' % key)

        # simulate the mechanical action of the machine
        self._step_rotors()

        # simulate the electrical operations:
        signal_num = ord(key) - ord('A')
        lamp_num = self._electric_signal(signal_num)
        return KEYBOARD_CHARS[lamp_num]

    def _step_rotors(self):
        """Simulate the mechanical action of pressing a key."""
        
        # The right-most rotor's right-side ratchet is always over a pawl, and
        # it has no neighbor to the right, so it always rotates.
        #
        # The middle rotor will rotate if either:
        #   1) The right-most rotor's left side notch is over the 2nd pawl
        #       or
        #   2) It has a left-side notch over the 3rd pawl
        #
        # The third rotor (from the right) will rotate only if the middle rotor
        # has a left-side notch over the 3rd pawl.
        #
        # Kriegsmarine model M4 has 4 rotors, but the 4th rotor (the leftmost)
        # does not rotate (they did not add a 4th pawl to the mechanism).

        rotor1 = self.rotors[-1]
        rotor2 = self.rotors[-2]
        rotor3 = self.rotors[-3]

        # decide which rotors can move
        rotate2 = rotor1.notch_over_pawl() or rotor2.notch_over_pawl()
        rotate3 = rotor2.notch_over_pawl()

        # move rotors
        rotor1.rotate()
        if rotate2:
            rotor2.rotate()
        if rotate3:
            rotor3.rotate()

    def _electric_signal(self, signal_num):
        """Simulate running an electric signal through the machine in order to
        perform an encrypt or decrypt operation

        signal_num - the wire (0-25) that the simulated current occurs on

        Returns a lamp number to light (an integer 0-25).

        """
        pos = self.plugboard.signal(signal_num)

        for rotor in reversed(self.rotors):
            pos = rotor.signal_in(pos)

        pos = self.reflector.signal_in(pos)

        for rotor in self.rotors:
            pos = rotor.signal_out(pos)

        return self.plugboard.signal(pos)

    def process_text(self, text, replace_char='X'):
        """Run the text through the machine, simulating a key press for each
        letter in the text.

        text - the text to process. Note that the text is converted to upper
        case before processing.

        replace_char - if text contains a character not on the keyboard, replace
        it with replace_char; if replace_char is None the character is dropped
        from the message

        """
        result = []
        for key in text:
            c = key.upper()

            if c not in KEYBOARD_SET: 
                if replace_char:
                    c = replace_char
                else:
                    continue    # ignore it

            result.append(self.key_press(c))

        return ''.join(result)

    def get_rotor_counts(self):
        """Return the rotor rotation counts as a list of integers."""
        return [r.rotations for r in self.rotors]
