Library Documentation
=====================

The Py-Enigma simulation is made up of several Python classes as described
below.

EnigmaMachine Class Reference
-----------------------------

The top-level ``EnigmaMachine`` class represents an assembled Enigma machine.
The ``EnigmaMachine`` class resides in the ``enigma.machine`` module.

.. class:: enigma.machine.EnigmaMachine(rotors, reflector, plugboard)

   Top-level class that represents Enigma machines.

   :param rotors: A list containing 3 or 4 (for the Kriegsmarine M4 version)
      :class:`Rotor <enigma.rotors.rotor.Rotor>` objects. The order of the
      list is important. The first rotor is the left-most rotor, and the last
      rotor is the right-most (from the operator's perspective sitting at the
      machine).
   :param reflector: A :class:`Rotor <enigma.rotors.rotor.Rotor>` object that
      represents the reflector (*UKW*).
   :param plugboard: A :class:`Plugboard <enigma.plugboard.Plugboard>` object
      that represents the state of the plugboard (*Steckerbrett*).

   .. classmethod:: from_key_sheet([rotors='I II III'[, ring_settings=None[, \
            reflector='B'[, plugboard_settings=None]]]])

      Convenience function to build an EnigmaMachine from the data as you
      might find it on a monthly key sheet (code book).

      :param rotors: Either a list of strings naming the rotors from left to
         right or a single string: e.g. ``["I", "III", "IV"]`` or ``"I III IV"``.
      :param ring_settings: Either a list/tuple of integers, a string, or ``None``
         to represent the ring settings to be applied to the rotors in the
         rotors list (see below).
      :param reflector: A string that names the reflector to use.
      :param plugboard_settings: A string of plugboard settings as you might
         find on a key sheet (see below).
       
      The ``ring_settings`` parameter can accept either:

      * A list/tuple of integers with values between 0-25.
      * A string; either space separated letters or numbers, e.g.
        ``'B U L'`` or ``'1 20 11'``.
      * ``None`` means all ring settings are 0.

      The ``plugboard_settings`` parameter can accept either:

      * A string of space separated letter pairs; e.g. ``'PO ML IU KJ NH YT GB VF RE DC'``.
      * A string of slash separated number pairs; e.g. ``'18/26 17/4 21/6 3/16 19/14 22/7 8/1 12/25 5/9 10/15'``.
      * A value of ``None`` means no plugboard connections are made.

   .. classmethod:: from_key_file(fp[, day=None])

      Convenience function to build an EnigmaMachine by reading key parameters
      from a file.

      :param fp: A file-like object that contains daily key settings, one day's
         settings per line.
      :param day: The line in the file labeled with the day number (1-31) will
         be used for the settings. If day is ``None``, the day number will be
         determined from today's date. 

      For more information on the file format, see :doc:`Key File Format <keyfile>`.

   .. method:: set_display(val)

      Sets the simulated rotor operator windows to *val*. This establishes a new
      starting position for a subsequent encrypt or decrypt operation. See also
      :meth:`get_display`.

      :param val: Must be a string or iterable containing uppercase letter values, one
         for each window from left to right. For example, a valid value for a 3 rotor
         machine would be ``'ABC'``.

   .. method:: get_display(val)

      This method returns the current position of the rotors as a string. See
      also :meth:`set_display`.

      :returns: a string of uppercase letters, one for each rotor
      :rtype: string

.. class:: enigma.rotors.rotor.Rotor(x, y)

   Rotor class
