# Copyright (C) 2012 by Brian Neal.
# This file is part of Py-Enigma, the Enigma Machine simulation.
# Py-Enigma is released under the MIT License (see License.txt).

"""test_rotor.py - Unit tests for the Rotor class for the Enigma simulation."""

import unittest
import collections
import string

from rotors.rotor import Rotor, RotorError, ALPHA_LABELS, NUMERIC_LABELS


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

        for alpha in True, False:
            self.assertRaises(RotorError, Rotor, 'I', WIRING,
                    alpha_labels=alpha, stepping="0")
            self.assertRaises(RotorError, Rotor, 'I', WIRING,
                    alpha_labels=alpha, stepping="A0")
            self.assertRaises(RotorError, Rotor, 'I', WIRING,
                    alpha_labels=alpha, stepping=[1])
            self.assertRaises(RotorError, Rotor, 'I', WIRING,
                    alpha_labels=alpha, stepping=['A', '%', '14'])
            self.assertRaises(RotorError, Rotor, 'I', WIRING,
                    alpha_labels=alpha, stepping=('A', '%', '14'))
    
    def test_alpha_display(self):

        for r in range(26):
            rotor = Rotor('I', WIRING, ring_setting=r, alpha_labels=True)
            for s in ALPHA_LABELS:
                rotor.set_display(s)
                self.assertEqual(s, rotor.get_display())

    def test_numeric_display(self):

        for r in range(26):
            rotor = Rotor('I', WIRING, ring_setting=r, alpha_labels=False)
            for s in NUMERIC_LABELS:
                rotor.set_display(s)
                self.assertEqual(s, rotor.get_display())

    def test_wiring(self):

        for r in range(26):
            rotor = Rotor('I', WIRING, ring_setting=r, alpha_labels=True)

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
