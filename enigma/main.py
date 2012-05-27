# Copyright (C) 2012 by Brian Neal.
# This file is part of Py-Enigma, the Enigma Machine simulation.
# Py-Enigma is released under the MIT License (see License.txt).

from .machine import EnigmaMachine


def main():

    machine = EnigmaMachine.from_key_sheet(
                        rotors=['I', 'II', 'III'],
                        reflector='B')

    machine.set_display('AAA')
    cipher_text = machine.process_text('AAAAA')

    print(cipher_text)


if __name__ == '__main__':
    main()
