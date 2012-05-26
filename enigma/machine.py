# Copyright (C) 2012 by Brian Neal.
# This file is part of Py-Enigma, the Enigma Machine simulation.
# Py-Enigma is released under the MIT License (see License.txt).

"""This module contains the top-level EnigmaMachine class for the Enigma Machine
simulation.

"""
import string

class EnigmaError(Exception):
    pass


class EnigmaMachine:
    """Top-level class for the Enigma Machine simulation."""

    def __init__(self, rotors, reflector):
        """Configures the Enigma Machine. Parameters are as follows:

        rotors - a list containing 3 or 4 (for the Kriegsmarine M4 version)
        Rotor objects. The order of the list is important. The first rotor is
        the left-most rotor, and the last rotor is the right-most (from the
        operator's perspective sitting at the machine).

        reflector - a rotor object to represent the reflector

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


    def set_display(self, val):

        for i, rotor in enumerate(self.rotors):
            self.rotors[i].set_display(val[i])


    def cipher(self, plaintext):

        # TODO: This is just placeholder code until I can figure out what I am
        # doing...!

        if len(plaintext) != 1:
            raise EnigmaError("not implemented yet")
        if plaintext[0] not in string.ascii_uppercase:
            raise EnigmaError("invalid input: %s" % plaintext)

        x = ord(plaintext[0]) - ord('A')

        x = self.rotors[-1].signal_in(x)
        print(chr(x + ord('A')))
        x = self.rotors[-2].signal_in(x)
        print(chr(x + ord('A')))
        x = self.rotors[-3].signal_in(x)
        print(chr(x + ord('A')))

        if self.rotor_count == 4:
            x = self.rotors[-4].signal_in(x)
            print(chr(x + ord('A')))

        x = self.reflector.signal_in(x)
        print(chr(x + ord('A')))

        x = self.rotors[0].signal_out(x)
        print(chr(x + ord('A')))
        x = self.rotors[1].signal_out(x)
        print(chr(x + ord('A')))
        x = self.rotors[2].signal_out(x)
        print(chr(x + ord('A')))

        if self.rotor_count == 4:
            x = self.rotors[3].signal_out(x)
            print(chr(x + ord('A')))

        ciphertext = chr(x + ord('A'))

        print("%s => %s" % (plaintext, ciphertext))

