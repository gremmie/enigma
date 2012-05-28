# Copyright (C) 2012 by Brian Neal.
# This file is part of Py-Enigma, the Enigma Machine simulation.
# Py-Enigma is released under the MIT License (see License.txt).

"""Tests for the Plugboard class."""

import unittest

from ..plugboard import Plugboard, PlugboardError


class PlugboardTestCase(unittest.TestCase):

    def test_bad_settings(self):

        # too many
        self.assertRaises(PlugboardError, Plugboard.from_key_sheet,
                settings='AB CD EF GH IJ KL MN OP QR ST UV')
        self.assertRaises(PlugboardError, Plugboard.from_key_sheet,
                '18/26 17/4 21/6 3/16 19/14 22/7 8/1 12/25 5/9 10/15 2/20')

        # duplicate
        self.assertRaises(PlugboardError, Plugboard.from_key_sheet,
                settings='AB CD EF GH IJ KL MN OF QR ST')

        self.assertRaises(PlugboardError, Plugboard.from_key_sheet,
                settings='AB CD EF GH IJ KL MN FP QR ST')

        self.assertRaises(PlugboardError, Plugboard.from_key_sheet,
                '18/26 17/4 21/6 3/16 19/14 22/3 8/1 12/25')

        # invalid
        self.assertRaises(PlugboardError, Plugboard.from_key_sheet,
                settings='A2 CD EF GH IJ KL MN FP QR ST')
        self.assertRaises(PlugboardError, Plugboard.from_key_sheet,
                settings='AB CD EF *H IJ KL MN FP QR ST')
        self.assertRaises(PlugboardError, Plugboard.from_key_sheet,
                settings='ABCD EF GH IJKLMN OP')
        self.assertRaises(PlugboardError, Plugboard.from_key_sheet,
                settings='A-D EF GH OP')
        self.assertRaises(PlugboardError, Plugboard.from_key_sheet,
                settings='A')
        self.assertRaises(PlugboardError, Plugboard.from_key_sheet,
                settings='9')
        self.assertRaises(PlugboardError, Plugboard.from_key_sheet,
                '1*/26 17/4 21/6 3/16 19/14 22/3 8/1 12/25')
        self.assertRaises(PlugboardError, Plugboard.from_key_sheet,
                '18/26 17/4 2A/6 3/16 19/14 22/3 8/1 12/25')
        self.assertRaises(PlugboardError, Plugboard.from_key_sheet,
                '100/2')
        self.assertRaises(PlugboardError, Plugboard.from_key_sheet,
                '100')
        self.assertRaises(PlugboardError, Plugboard.from_key_sheet,
                settings='T/C')

    def test_valid_settings(self):

        # these should be valid settings and should not raise
        p = Plugboard()
        p = Plugboard(None)
        p = Plugboard(wiring_pairs=None)
        p = Plugboard(wiring_pairs=[])
        p = Plugboard([])
        p = Plugboard.from_key_sheet('AB CD EF GH IJ KL MN OP QR ST')
        p = Plugboard.from_key_sheet('CD EF GH IJ KL MN OP QR ST')
        p = Plugboard.from_key_sheet('EF GH IJ KL MN OP QR ST')
        p = Plugboard.from_key_sheet(' GH ')
        p = Plugboard.from_key_sheet('18/26 17/4 21/6 3/16 19/14 22/7 8/1 12/25'
                ' 5/9 10/15')
        p = Plugboard.from_key_sheet('18/26 17/4')
        p = Plugboard.from_key_sheet(' 18/26 ')
        p = Plugboard.from_key_sheet()
        p = Plugboard.from_key_sheet('')
        p = Plugboard.from_key_sheet(None)

    def test_default_wiring(self):

        p = Plugboard()
        for n in range(26):
            self.assertEqual(n, p.signal(n))
      
    def test_wiring(self):
        settings =['AB CD EF GH IJ KL MN OP QR ST',
                   '1/2 3/4 5/6 7/8 9/10 11/12 13/14 15/16 17/18 19/20']

        for setting in settings:
            p = Plugboard.from_key_sheet(setting)
            for n in range(26):

                if n < 20:
                    if n % 2 == 0:
                        self.assertEqual(p.signal(n), n + 1)
                    else:
                        self.assertEqual(p.signal(n), n - 1)
                else:
                    self.assertEqual(n, p.signal(n))

    def test_wiring2(self):
    
        stecker='AV BS CG DL FU HZ IN KM OW RX'

        wiring = {}
        pairs = stecker.split()
        for p in pairs:
            m, n = ord(p[0]) - ord('A'), ord(p[1]) - ord('A')
            wiring[m] = n
            wiring[n] = m

        p = Plugboard.from_key_sheet(stecker)
        for n in range(26):
            if n in wiring:
                self.assertEqual(p.signal(n), wiring[n])
            else:
                self.assertEqual(p.signal(n), n)
