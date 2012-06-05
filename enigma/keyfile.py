# Copyright (C) 2012 by Brian Neal.
# This file is part of Py-Enigma, the Enigma Machine simulation.
# Py-Enigma is released under the MIT License (see License.txt).

"""Contains a function to read key settings from a file.

A key file is expected to be formatted as one line per day of the month. Each
line consists of a sequence of space separated columns as follows:

day number - the first column is the day number (1-31). The lines can be in
any order.

rotor list - the next 3 or 4 columns should be rotor names. 

ring settings - the next 3 or 4 columns should be ring settings. They can be
in either alphabetic (A-Z) or numeric (0-25) formats.

plugboard settings - the next 10 columns should be plugboard settings. They
can be in either alphabetic (AB CD EF ...) or numeric (1/2 3/4 ...) formats.

reflector - the last column must be the reflector name.

Comment lines have a # character in the first column. Blank lines are ignored.

Each line must either have exactly 18 or 20 columns to be valid.

"""
import datetime


class KeyFileError(Exception):
    pass


def get_daily_settings(fp, day=None):
    """Read and parse a key file for daily key settings. 

    fp - a file-like object 

    day - specifies the day number to look for in the file (1-31). If day is
    None, the day number from today is used.
    
    Returns a dictionary of keyword arguments for EnigmaMachine.from_key_sheet.

    """
    if day is None:
        day = datetime.date.today().day

    for n, line in enumerate(fp):
        line = line.strip()
        if line == '' or line[0] == '#':
            continue

        cols = line.split()
        if len(cols) not in [18, 20]:
            raise KeyFileError("invalid column count on line %d" % n)
        
        rotor_count = 3 if len(cols) == 18 else 4

        try:
            day_num = int(cols[0])
        except ValueError:
            raise KeyFileError("invalid day on line %d" % n)

        if day_num != day:
            continue

        settings = {}
        if rotor_count == 3:
            settings['rotors'] = cols[1:4]
            settings['ring_settings'] = ' '.join(cols[4:7])
        else:
            settings['rotors'] = cols[1:5]
            settings['ring_settings'] = ' '.join(cols[5:9])

        settings['plugboard_settings'] = ' '.join(cols[-11:-1])
        settings['reflector'] = cols[-1]
        return settings

    else:
        raise KeyFileError('no entry for day %d found' % day)

        return settings
