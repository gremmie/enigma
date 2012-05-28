# Copyright (C) 2012 by Brian Neal.
# This file is part of Py-Enigma, the Enigma Machine simulation.
# Py-Enigma is released under the MIT License (see License.txt).

"""Tests for the EnigmaMachine class."""

import unittest

from ..machine import EnigmaMachine


class SteppingTestCase(unittest.TestCase):

    def test_double_stepping(self):
        """Ensure the rotors step realistically by testing for a "double-step"
        case.
        
        """
        # This example taken from 
        # http://users.telenet.be/d.rijmenants/en/enigmatech.htm
        # in the section on "The Stepping Mechanism."
        m = EnigmaMachine.from_key_sheet(rotors=['III', 'II', 'I'])

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
        self.machine = EnigmaMachine.from_key_sheet(rotors=['I', 'II', 'III'])
        self.machine.set_display('AAA')

    def test_simple_encrypt(self):

        cipher_text = self.machine.process_text(self.PLAIN_TEXT)
        self.assertEqual(cipher_text, self.CIPHER_TEXT)

    def test_simple_decrypt(self):

        plain_text = self.machine.process_text(self.CIPHER_TEXT)
        self.assertEqual(plain_text, self.PLAIN_TEXT)


class ActualCipherTestCase(unittest.TestCase):
    """This example taken from Dirk Rijmenants' simulator manual."""

    def setUp(self):

        ring_settings = [ord(c) - ord('A') for c in 'BUL']

        self.machine = EnigmaMachine.from_key_sheet(
                rotors='II IV V',
                reflector='B',
                ring_settings=ring_settings,
                plugboard_settings='AV BS CG DL FU HZ IN KM OW RX')

    def test_decrypt(self):

        # retrieve the message key
        self.machine.set_display('WXC')
        msg_key = self.machine.process_text('KCH')

        # set the message key
        self.machine.set_display(msg_key)

        ciphertext = (
            'RFUGZ EDPUD NRGYS ZRCXN'
            'UYTPO MRMBO FKTBZ REZKM'
            'LXLVE FGUEY SIOZV EQMIK'
            'UBPMM YLKLT TDEIS MDICA'
            'GYKUA CTCDO MOHWX MUUIA'
            'UBSTS LRNBZ SZWNR FXWFY'
            'SSXJZ VIJHI DISHP RKLKA'
            'YUPAD TXQSP INQMA TLPIF'
            'SVKDA SCTAC DPBOP VHJK')

        # remove spaces and the Kenngruppen
        ciphertext = ciphertext.replace(' ', '')[5:]
        plaintext = self.machine.process_text(ciphertext)

        print("'{}'\n\n'{}'\n\n'{}'\n\n".format(msg_key, ciphertext[:11],
            plaintext[:11]))
