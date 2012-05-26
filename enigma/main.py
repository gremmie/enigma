# Copyright (C) 2012 by Brian Neal.
# This file is part of Py-Enigma, the Enigma Machine simulation.
# Py-Enigma is released under the MIT License (see License.txt).


from rotors.factory import create_rotor
from rotors.factory import create_reflector
from machine import EnigmaMachine

def main():

    rotors = []
    rotors.append(create_rotor('I'))
    rotors.append(create_rotor('II'))
    rotors.append(create_rotor('III'))

    reflector = create_reflector('B')

    machine = EnigmaMachine(rotors=rotors, reflector=reflector)

    machine.set_display('AAB')
    machine.cipher('A')
    machine.set_display('AAC')
    machine.cipher('A')
    machine.set_display('AAD')
    machine.cipher('A')
    machine.set_display('AAE')
    machine.cipher('A')
    machine.set_display('AAF')
    machine.cipher('A')


if __name__ == '__main__':
    main()
