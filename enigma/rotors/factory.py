# Copyright (C) 2012 by Brian Neal.
# This file is part of Py-Enigma, the Enigma Machine simulation.
# Py-Enigma is released under the MIT License (see License.txt).

"""Contains factory functions for creating rotors and reflectors."""

from enigma.rotors import RotorError
from enigma.rotors.rotor import Rotor
from enigma.rotors.data import ROTORS, REFLECTORS


def create_rotor(model, ring_setting, alpha_labels=True):
    """Factory function to create and return a rotor of the given model name."""

    if model in ROTORS:
        data = ROTORS[model]
        return Rotor(model, data['wiring'], ring_setting, data['stepping'],
                alpha_labels)

    raise RotorError("Unknown rotor type: %s" % model)


def create_reflector(model):
    """Factory function to create and return a reflector of the given model
    name.
    
    """
    if model in REFLECTORS:
        return Rotor(model, wiring=REFLECTORS[model])

    raise RotorError("Unknown reflector type: %s" % model)
