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

    machine.set_display('AAA')
    cipher_text = machine.process_text('AAAAA')

    print(cipher_text)


if __name__ == '__main__':
    main()
