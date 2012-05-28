# Copyright (C) 2012 by Brian Neal.
# This file is part of Py-Enigma, the Enigma Machine simulation.
# Py-Enigma is released under the MIT License (see License.txt).

"""test_rotor.py - Unit tests for the Rotor class for the Enigma simulation."""

import unittest
import collections
import string

from ..rotors.rotor import Rotor, ALPHA_LABELS
from ..rotors import RotorError
from ..rotors.data import ROTORS
from ..rotors.factory import create_rotor


WIRING = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'


class SimpleRotorTestCase(unittest.TestCase):
    """Basic tests to verify Rotor functionality"""

    def test_bad_wiring(self):

        self.assertRaises(RotorError, Rotor, 'I', '')
        self.assertRaises(RotorError, Rotor, 'I', 'ABC')
        self.assertRaises(RotorError, Rotor, 'I', '123')

        w = string.punctuation[:26]
        self.assertRaises(RotorError, Rotor, 'I', w)

        w = 'ABCD' * 7
        self.assertRaises(RotorError, Rotor, 'III', w[:26])

    def test_bad_ring_setting(self):

        self.assertRaises(RotorError, Rotor, 'I', WIRING, ring_setting=-1)
        self.assertRaises(RotorError, Rotor, 'I', WIRING, ring_setting=26)
        self.assertRaises(RotorError, Rotor, 'I', WIRING, ring_setting='A')
        self.assertRaises(RotorError, Rotor, 'I', WIRING, ring_setting=None)

    def test_bad_stepping(self):

        self.assertRaises(RotorError, Rotor, 'I', WIRING, stepping="0")
        self.assertRaises(RotorError, Rotor, 'I', WIRING, stepping="A0")
        self.assertRaises(RotorError, Rotor, 'I', WIRING, stepping=[1])
        self.assertRaises(RotorError, Rotor, 'I', WIRING, stepping=['A', '%', '14'])
        self.assertRaises(RotorError, Rotor, 'I', WIRING, stepping=('A', '%', '14'))
    
    def test_display(self):

        for r in range(26):
            rotor = Rotor('I', WIRING, ring_setting=r)
            for s in ALPHA_LABELS:
                rotor.set_display(s)
                self.assertEqual(s, rotor.get_display())

    def test_wiring(self):
        """Loop through all ring settings & rotor positions and test the
        wiring.
        
        """
        for r in range(26):
            rotor = Rotor('I', WIRING, ring_setting=r)

            for n, d in enumerate(ALPHA_LABELS):
                rotor.set_display(d)

                wiring = collections.deque(WIRING)
                wiring.rotate(r - n)

                for i in range(26):
                    output = rotor.signal_in(i)

                    expected = (ord(wiring[i]) - ord('A') + r - n) % 26
                    self.assertEqual(output, expected)

                    output = rotor.signal_out(expected)
                    self.assertEqual(output, i)

    def test_notches(self):
        """For every rotor we simulate, ensure that the notch setting is correct
        regardless of the ring setting.

        """
        rotor_names = ROTORS.keys()
        for rotor_name in rotor_names:
            notches = ROTORS[rotor_name]['stepping']
            if notches is None:
                continue
            for r in range(26):
                rotor = create_rotor(rotor_name, r)
                rotor.set_display('A')

                for n in range(26):
                    over_notch = rotor.get_display() in notches
                    self.assertEqual(rotor.notch_over_pawl(), over_notch)
                    rotor.rotate()

    def test_rotate(self):

        for r in range(26):
            rotor1 = Rotor('X', WIRING, ring_setting=r)
            rotor2 = Rotor('Y', WIRING, ring_setting=r)

            rotor2.set_display('A')

            for i, d in enumerate(ALPHA_LABELS):
                rotor1.set_display(d)
                self.assertEqual(rotor1.get_display(), rotor2.get_display())
                rotor2.rotate()
