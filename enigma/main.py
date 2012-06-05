# Copyright (C) 2012 by Brian Neal.
# This file is part of Py-Enigma, the Enigma Machine simulation.
# Py-Enigma is released under the MIT License (see License.txt).

"""Provide an example command-line app that can setup an EnigmaMachine and
process text.

"""

import argparse
import sys

from .machine import EnigmaMachine, EnigmaError
from .rotors import RotorError
from .keyfile import KeyFileError


PROG_DESC = 'Encrypt/decrypt text according to Enigma machine key settings'

HELP_EPILOG = """\
Key settings can either be specified by command-line arguments, or read
from a key file. If reading from a key file, the line labeled with the
current day number is used unless the --day argument is provided.

Text to process can be supplied 3 ways:

   if --text=TEXT is present TEXT is processed
   if --file=FILE is present the contents of FILE are processed
   otherwise the text is read from standard input

Examples:

    $ %(prog)s --key-file=enigma.keys -s XYZ -t HELLOXWORLDX
    $ %(prog)s -r III IV V -i 1 2 3 -p AB CD EF GH IJ KL MN -u B -s XYZ
    $ %(prog)s -r Beta III IV V -i A B C D -p 1/2 3/4 5/6 -u B-Thin -s WXYZ
  
"""

def create_from_key_file(filename, day=None):
    """Create an EnigmaMachine from a daily key sheet."""

    with open(filename, 'r') as f:
        return EnigmaMachine.from_key_file(f, day)


def create_from_args(parser, args):
    """Create an EnigmaMachine from command-line specs."""

    if args.rotors is None:
        parser.error("Please specify 3 or 4 rotors; e.g. II IV V")
    elif len(args.rotors) not in [3, 4]:
        parser.error("Expecting 3 or 4 rotors; %d supplied" % len(args.rotors))

    if args.text and args.file:
        parser.error("Please specify --text or --file, but not both")

    ring_settings = ' '.join(args.ring_settings) if args.ring_settings else None
    plugboard = ' '.join(args.plugboard) if args.plugboard else None

    return EnigmaMachine.from_key_sheet(rotors=args.rotors,
                                        ring_settings=ring_settings,
                                        plugboard_settings=plugboard,
                                        reflector=args.reflector)


def main():

    parser = argparse.ArgumentParser(description=PROG_DESC, epilog=HELP_EPILOG,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('-k', '--key-file',
            help='path to key file for daily settings')
    parser.add_argument('-d', '--day', type=int, default=None,
            help='use the settings for day DAY when reading key file')
    parser.add_argument('-r', '--rotors', nargs='+', metavar='ROTOR',
            help='rotor list ordered from left to right; e.g III IV I')
    parser.add_argument('-i', '--ring-settings', nargs='+',
            metavar='RING_SETTING',
            help='ring setting list from left to right; e.g. A A J')
    parser.add_argument('-p', '--plugboard', nargs='+', metavar='PLUGBOARD',
            help='plugboard settings')
    parser.add_argument('-u', '--reflector', help='reflector name')
    parser.add_argument('-s', '--start', help='starting position')
    parser.add_argument('-t', '--text', help='text to process')
    parser.add_argument('-f', '--file', help='input file to process')
    parser.add_argument('-x', '--replace-char', default='X',
            help=('if the input text contains chars not found on the enigma'
                  ' keyboard, replace with this char [default: %(default)s]'))
    parser.add_argument('-z', '--delete-chars', default=False,
            action='store_true',
            help=('if the input text contains chars not found on the enigma'
                  ' keyboard, delete them from the input'))
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
            help='provide verbose output; include final rotor positions')

    args = parser.parse_args()

    if args.key_file and (args.rotors or args.ring_settings or args.plugboard
            or args.reflector):
        parser.error("Please specify either a key file or command-line key "
                     "settings, but not both")

    if args.start is None:
        parser.error("Please specify a start position")

    if args.key_file:
        machine = create_from_key_file(args.key_file, args.day)
    else:
        machine = create_from_args(parser, args)

    if args.text:
        text = args.text
    elif args.file:
        with open(args.file, 'r') as f:
            text = f.read()
    else:
        text = input('--> ')

    replace_char = args.replace_char if not args.delete_chars else None

    machine.set_display(args.start)

    s = machine.process_text(text, replace_char=replace_char)

    if args.verbose:
        print('Final rotor positions:', machine.get_display())
        print('Rotor rotation counts:', machine.get_rotor_counts())
        print('Output:')

    print(s)


def console_main():
    try:
        main()
    except (IOError, EnigmaError, RotorError, KeyFileError) as ex:
        sys.stderr.write("%s\n" % ex)


if __name__ == '__main__':
    console_main()
