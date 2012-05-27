# Copyright (C) 2012 by Brian Neal.
# This file is part of Py-Enigma, the Enigma Machine simulation.
# Py-Enigma is released under the MIT License (see License.txt).

"""This module contains the top-level EnigmaMachine class for the Enigma Machine
simulation.

"""
import string

from .rotors.factory import create_rotor, create_reflector
from .plugboard import Plugboard


class EnigmaError(Exception):
    pass

# The Enigma keyboard consists of the 26 letters of the alphabet, uppercase
# only:
KEYBOARD_CHARS = string.ascii_uppercase


class EnigmaMachine:
    """Top-level class for the Enigma Machine simulation."""

    def __init__(self, rotors, reflector, plugboard):
        """Configures the Enigma Machine. Parameters are as follows:

        rotors - a list containing 3 or 4 (for the Kriegsmarine M4 version)
        Rotor objects. The order of the list is important. The first rotor is
        the left-most rotor, and the last rotor is the right-most (from the
        operator's perspective sitting at the machine).

        reflector - a rotor object to represent the reflector

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
    def from_key_sheet(cls, rotors, ring_settings=(0, 0, 0), reflector='B',
            plugboard_settings=''):
        """Convenience function to build an EnigmaMachine from the data as you
        might find it on a key sheet:

        rotors: a list of strings naming the rotors from left to right;
            e.g. ["I", "III", "IV"]

        ring_settings: an iterable of integers representing the ring settings to
        be applied to the rotors in the rotors list

        reflector: a string that names the reflector to use

        plugboard: a string of plugboard settings as you might find on a key
        sheet; e.g. 'PO ML IU KJ NH YT GB VF RE DC' 

        """
        # validate inputs
        num_rotors = len(rotors)
        if num_rotors not in (3, 4):
            raise EnigmaError("invalid rotors list size")

        if num_rotors != len(ring_settings):
            raise EnigmaError("please provide %d ring settings" % num_rotors)

        # assemble the machine
        rotor_list = [create_rotor(r[0], r[1]) for r in zip(rotors, ring_settings)]

        return cls(rotor_list, 
                   create_reflector(reflector),
                   Plugboard(plugboard_settings))


    def set_display(self, val):
        """Sets the rotor operator windows to 'val'.

        'val' must be a string or iterable containing 3 values, one for each
        window from left to right.

        """
        if len(val) != 3:
            raise EnigmaError("Bad display value")

        start = 0 if self.rotor_count == 3 else 1
        for i, r in enumerate(range(start, self.rotor_count)):
            self.rotors[r].set_display(val[i])

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
        if key not in KEYBOARD_CHARS:
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

    def process_text(self, text):
        """Run the text through the machine, simulating a key press for each
        letter in the text.

        """
        # TODO: if there is a character not on the keyboard, perform a
        # substitution or skip it.
        result = []
        for key in text:
            result.append(self.key_press(key))

        return ''.join(result)
