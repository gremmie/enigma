# Copyright (C) 2012 by Brian Neal.
# This file is part of Py-Enigma, the Enigma Machine simulation.
# Py-Enigma is released under the MIT License (see License.txt).

"""data.py - This file contains rotor & reflector data for all the types
we simulate.

"""

# This data is taken from Dirk Rijmenants very informative and useful Enigma
# website: "Techical Details of the Engigma Machine"
# http://users.telenet.be/d.rijmenants/en/enigmatech.htm
#
# Rotors I-V were used by the Heer, Luftwaffe, and Kriegsmarine. The
# Kriegsmarine added rotors VI-VIII to the M3 model, and added Beta & Gamma to
# the M4 model (used with thin reflectors only). Note that Beta & Gamma rotors
# did not rotate.
#
# The Heer, Luftwaffe, & Kriegsmarine M3 machines used reflectors B & C,
# while the Kriegsmarine M4 used thin reflectors B & C.
#

ROTORS = {
    'I': {
        'wiring': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
        'stepping': 'Q',
    },
    'II': {
        'wiring': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
        'stepping': 'E',
    },
    'III': {
        'wiring': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
        'stepping': 'V',
    },
    'IV': {
        'wiring': 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
        'stepping': 'J',
    },
    'V': {
        'wiring': 'VZBRGITYUPSDNHLXAWMJQOFECK',
        'stepping': 'Z',
    },
    'VI': {
        'wiring': 'JPGVOUMFYQBENHZRDKASXLICTW',
        'stepping': 'ZM',
    },
    'VII': {
        'wiring': 'NZJHGRCXMYSWBOUFAIVLPEKQDT',
        'stepping': 'ZM',
    },
    'VIII': {
        'wiring': 'FKQHTLXOCBJSPDZRAMEWNIUYGV',
        'stepping': 'ZM',
    },
    'Beta': {
        'wiring': 'LEYJVCNIXWPBQMDRTAKZGFUHOS',
        'stepping': None,
    },
    'Gamma': {
        'wiring': 'FSOKANUERHMBTIYCWLQPZXVGJD',
        'stepping': None,
    },
}

REFLECTORS = {
    'B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
    'C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL',
    'B-Thin': 'ENKQAUYWJICOPBLMDXZVFTHRGS',
    'C-Thin': 'RDOBJNTKVEHMLFCWZAXGYIPSUQ',
}
