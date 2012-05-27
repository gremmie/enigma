# Copyright (C) 2012 by Brian Neal.
# This file is part of Py-Enigma, the Enigma Machine simulation.
# Py-Enigma is released under the MIT License (see License.txt).

"""Tests for the EnigmaMachine class."""

import unittest

from ..rotors.factory import create_rotor, create_reflector
from ..machine import EnigmaMachine
from ..plugboard import Plugboard


class SteppingTestCase(unittest.TestCase):

    def test_double_stepping(self):
        """Ensure the rotors step realistically by testing for a "double-step"
        case.
        
        """
        # This example taken from 
        # http://users.telenet.be/d.rijmenants/en/enigmatech.htm
        # in the section on "The Stepping Mechanism."
        rotors = []
        rotors.append(create_rotor("III"))
        rotors.append(create_rotor("II"))
        rotors.append(create_rotor("I"))

        m = EnigmaMachine(rotors, create_reflector('B'), Plugboard())

        m.set_display('KDO')

        truth_data = ['KDP', 'KDQ', 'KER', 'LFS', 'LFT', 'LFU']
        for expected in truth_data:
            m.key_press('A')
            self.assertEqual(m.get_display(), expected)


class SimpleCipherTestCase(unittest.TestCase):
    """This example taken from Wikipedia"""

    PLAIN_TEXT = 'AAAAA'
    CIPHER_TEXT = 'BDZGO'

    def setUp(self):
        rotors = []
        rotors.append(create_rotor('I'))
        rotors.append(create_rotor('II'))
        rotors.append(create_rotor('III'))

        reflector = create_reflector('B')

        self.machine = EnigmaMachine(rotors=rotors, reflector=reflector,
                                     plugboard=Plugboard())
        self.machine.set_display('AAA')

    def test_simple_encrypt(self):

        cipher_text = self.machine.process_text(self.PLAIN_TEXT)
        self.assertEqual(cipher_text, self.CIPHER_TEXT)

    def test_simple_decrypt(self):

        plain_text = self.machine.process_text(self.CIPHER_TEXT)
        self.assertEqual(plain_text, self.PLAIN_TEXT)
