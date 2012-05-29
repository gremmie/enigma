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


class ActualDecryptTestCase(unittest.TestCase):
    """This example taken from Dirk Rijmenants' simulator manual.
    
    It is credited to Frode Weierud and Geoff Sullivan.
        http://cryptocellar.com
    
    """
    def setUp(self):

        self.machine = EnigmaMachine.from_key_sheet(
                rotors='II IV V',
                reflector='B',
                ring_settings='B U L',
                plugboard_settings='AV BS CG DL FU HZ IN KM OW RX')

    def decrypt(self, start, enc_key, ciphertext, truth_data):

        # remove spaces & Kenngruppen from the ciphertext
        ciphertext = ciphertext.replace(' ', '')[5:]

        # remove spaces from the truth data
        truth_data = truth_data.replace(' ', '')

        # decrypt the message key
        self.machine.set_display(start)
        msg_key = self.machine.process_text(enc_key)

        # decrypt the cipher text with the unencrypted message key
        self.machine.set_display(msg_key)
        plaintext = self.machine.process_text(ciphertext)

        self.assertEqual(plaintext, truth_data)

    def test_decrypt_part1(self):

        ciphertext = (
            'RFUGZ EDPUD NRGYS ZRCXN'
            'UYTPO MRMBO FKTBZ REZKM'
            'LXLVE FGUEY SIOZV EQMIK'
            'UBPMM YLKLT TDEIS MDICA'
            'GYKUA CTCDO MOHWX MUUIA'
            'UBSTS LRNBZ SZWNR FXWFY'
            'SSXJZ VIJHI DISHP RKLKA'
            'YUPAD TXQSP INQMA TLPIF'
            'SVKDA SCTAC DPBOP VHJK'
        )

        truth_data = (
            'AUFKL XABTE ILUNG XVONX' 
            'KURTI NOWAX KURTI NOWAX'
            'NORDW ESTLX SEBEZ XSEBE'
            'ZXUAF FLIEG ERSTR ASZER'
            'IQTUN GXDUB ROWKI XDUBR'
            'OWKIX OPOTS CHKAX OPOTS'
            'CHKAX UMXEI NSAQT DREIN'
            'ULLXU HRANG ETRET ENXAN'
            'GRIFF XINFX RGTX'
        )

        self.decrypt('WXC', 'KCH', ciphertext, truth_data)

    def test_decrypt_part2(self):

        ciphertext = (
            'FNJAU SFBWD NJUSE GQOBH'
            'KRTAR EEZMW KPPRB XOHDR'
            'OEQGB BGTQV PGVKB VVGBI'
            'MHUSZ YDAJQ IROAX SSSNR'
            'EHYGG RPISE ZBOVM QIEMM'
            'ZCYSG QDGRE RVBIL EKXYQ'
            'IRGIR QNRDN VRXCY YTNJR'
        )

        truth_data = (
            'DREIG EHTLA NGSAM ABERS' 
            'IQERV ORWAE RTSXE INSSI' 
            'EBENN ULLSE QSXUH RXROE' 
            'MXEIN SXINF RGTXD REIXA' 
            'UFFLI EGERS TRASZ EMITA' 
            'NFANG XEINS SEQSX KMXKM' 
            'XOSTW XKAME NECXK'
        )

        self.decrypt('CRS', 'YPJ', ciphertext, truth_data)


class KriegsmarineTestCase(unittest.TestCase):
    """This is the Kriegsmarine example from Dirk Rijmenants' simulator manual.

    It is credited to Stefan Krah and the M4 project:
        http://www.bytereef.org/m4_project.html

    """
    def test_decrypt(self):

        stecker ='1/20 2/12 4/6 7/10 8/13 14/23 15/16 17/25 18/26 22/24'

        machine = EnigmaMachine.from_key_sheet(
                    rotors='Beta II IV I',
                    ring_settings='A A A V',
                    reflector='B-Thin',
                    plugboard_settings=stecker)

        ciphertext = (
        'FCLC QRKN NCZW VUSX PNYM INHZ XMQX SFWX WLKJ AHSH NMCO CCAK UQPM KCSM'
        'HKSE INJU SBLK IOSX CKUB HMLL XCSJ USRR DVKO HULX WCCB GVLI YXEO AHXR'
        'HKKF VDRE WEZL XOBA FGYU JQUK GRTV UKAM EURB VEKS UHHV OYHA BCJW MAKL'
        'FKLM YFVN RIZR VVRT KOFD ANJM OLBG FFLE OPRG TFLV RHOW OPBE KVWM UQFM'
        'PWPA RMFH AGKX IIBG FCLC QRKM VA'
        ).replace(' ', '')

        # remove the message indicators from the message (the first and last 2
        # groups of the message -- it appears the last partial group 'VA' should
        # be removed also)

        ciphertext = ciphertext[8:-10]

        machine.set_display('VJNA')
        plaintext = machine.process_text(ciphertext)

        truth_data = (
            'VONV ONJL OOKS JHFF TTTE'
            'INSE INSD REIZ WOYY QNNS'
            'NEUN INHA LTXX BEIA NGRI'
            'FFUN TERW ASSE RGED RUEC'
            'KTYW ABOS XLET ZTER GEGN'
            'ERST ANDN ULAC HTDR EINU'
            'LUHR MARQ UANT ONJO TANE'
            'UNAC HTSE YHSD REIY ZWOZ'
            'WONU LGRA DYAC HTSM YSTO'
            'SSEN ACHX EKNS VIER MBFA'
            'ELLT YNNN NNNO OOVI ERYS'
            'ICHT EINS NULL'
        ).replace(' ', '')

        self.assertEqual(plaintext, truth_data)
