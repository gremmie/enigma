Key file format
===============

Specifying key settings can become tedious and error-prone, so Py-Enigma allows
you to store key settings in a simulated monthly key sheet file. This is a
simple text file that you can create with your favorite text editor. Each line
of this file represents one days settings. Within the line, whitespace separates
each item. The columns for each line are as follows:

#. The first column is the day number for the setting, similar to a real key
   sheet. The day should be an integer in the range 1-31.
#. The next 3 or 4 columns are rotor names. See :ref:`rotor-table-label` for a
   list of valid rotor names.
#. The next 3 or 4 columns are the ring settings for each rotor. These can be a
   list of numbers (1-26) or letters (A-Z).
#. The next 10 columns are the plugboard settings. These can be a list of
   2-letter pairs (e.g. AB CD, etc.) or slash separated number pairs (e.g. 1/20
   3/22).
#. The last column is the reflector name. See :ref:`reflector-table-label` for a
   list of the valid reflector names.

Please note the following about the file format:

* Each line must have either 18 or 20 columns, depending on if you are
  simulating a 3 or 4 rotor Enigma.
* It is possible to mix 3 and 4 rotor settings in the same file.
* You do not have to supply settings for every day in the month.
* Py-Enigma will simply scan the file from top to bottom until it finds the line
  that corresponds to the day number it is looking for. Thus duplicate day
  settings are allowed, but keep in mind the first line will be used.
* The file can contain blank lines.
* The file can contain comment lines. Comment lines begin with a ``#`` character
  in the first column and extend to the end of the line.

Example file::

   # My sample settings file
   29 II IV V 1 16 10 AV BS CG DL FU HZ IN KM OW RX B
   30 Beta II IV I A A A V 1/20 2/12 4/6 7/10 8/13 14/23 15/16 17/25 18/26 22/24 B-Thin
