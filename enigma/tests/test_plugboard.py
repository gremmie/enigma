# Copyright (C) 2012 by Brian Neal.
# This file is part of Py-Enigma, the Enigma Machine simulation.
# Py-Enigma is released under the MIT License (see License.txt).

"""Tests for the Plugboard class."""

import unittest

from ..plugboard import Plugboard, PlugboardError


class PlugboardTestCase(unittest.TestCase):

    def test_bad_settings(self):

        # too many
        self.assertRaises(PlugboardError, Plugboard,
                settings='AB CD EF GH IJ KL MN OP QR ST UV')

        # duplicate
        self.assertRaises(PlugboardError, Plugboard,
                settings='AB CD EF GH IJ KL MN OF QR ST')

        self.assertRaises(PlugboardError, Plugboard,
                settings='AB CD EF GH IJ KL MN FP QR ST')

        # invalid
        self.assertRaises(PlugboardError, Plugboard,
                settings='A2 CD EF GH IJ KL MN FP QR ST')
        self.assertRaises(PlugboardError, Plugboard,
                settings='AB CD EF *H IJ KL MN FP QR ST')
        self.assertRaises(PlugboardError, Plugboard,
                settings='ABCD EF GH IJKLMN OP')
        self.assertRaises(PlugboardError, Plugboard, settings='A-D EF GH OP')
        self.assertRaises(PlugboardError, Plugboard, settings='A')

    def test_valid_settings(self):

        # these should be valid settings and should not raise
        p = Plugboard()
        p = Plugboard(None)
        p = Plugboard(settings=None)
        p = Plugboard(settings='')
        p = Plugboard('')
        p = Plugboard(settings='AB CD EF GH IJ KL MN OP QR ST')
        p = Plugboard(settings='CD EF GH IJ KL MN OP QR ST')
        p = Plugboard(settings='EF GH IJ KL MN OP QR ST')
        p = Plugboard(settings=' GH ')

    def test_default_wiring(self):

        p = Plugboard()
        for n in range(26):
            self.assertEqual(n, p.signal(n))
      
    def test_wiring(self):

        p = Plugboard(settings='AB CD EF GH IJ KL MN OP QR ST')
        for n in range(26):

            if n < 20:
                if n % 2 == 0:
                    self.assertEqual(p.signal(n), n + 1)
                else:
                    self.assertEqual(p.signal(n), n - 1)
            else:
                self.assertEqual(n, p.signal(n))
