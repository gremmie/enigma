Reference manual
================

The Py-Enigma simulation is made up of several Python classes as described
below.

EnigmaMachines
--------------

The ``EnigmaMachine`` class represents an assembled Enigma machine that consists
of rotors, a plugboard, a keyboard, and indicator lamps. The keyboard and lamps
act as input and outputs. The other components are represented by Python
classes.


EnigmaMachine class reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
        ``'B U L'`` or ``'1 20 11'``. Note that if numbers are used, they
        should be between 1-26 to match historical key sheet data.
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

      :returns: a string of uppercase letters, one for each rotor (left to
         right)
      :rtype: string

   .. method:: get_rotor_count()

      Returns a list of integers that represent the rotation counts for each 
      rotor. The rotation counts are reset to 0 every time :meth:`set_display`
      is called.

   .. method:: key_press(key)

      Simulate a front panel key press. First the rotors are stepped by
      simulating the mechanical action of the machine. Next a simulated current
      is run through the machine. The lamp that is lit by this key press is
      returned as a string (a single uppercase letter A-Z).

      :param key: the letter pressed (A-Z)
      :type key: string
      :returns: the lamp that is lit (A-Z)
      :rtype: string

   .. method:: process_text(text[, replace_char='X'])

      This is a convenience function for processing a string of text. For each
      character in the input text, :meth:`key_press` is called. The output text
      is returned as a string.

      This function performs some pre-processing of the input text, unlike
      :meth:`key_press`. First, all input is converted to uppercase. Secondly,
      the parameter ``replace_char`` controls what is done to input characters
      that are not ``A-Z``. If the input text contains a character not on the
      keyboard, it is replaced with ``replace_char``. If ``replace_char`` is
      ``None`` the character is dropped from the input. ``replace_char``
      defaults to ``X``.

      :param string text: the text to process
      :param replace_char: invalid input is replaced with this string or dropped
         if it is ``None``


EnigmaMachine exceptions
~~~~~~~~~~~~~~~~~~~~~~~~

:class:`EnigmaMachine <enigma.machine.EnigmaMachine>` operations may raise
``enigma.machine.EnigmaError`` under error conditions. The two ``classmethod``
constructors, :meth:`from_key_sheet <enigma.machine.EnigmaMachine.from_key_sheet>`
and :meth:`from_key_file <enigma.machine.EnigmaMachine.from_key_file>` assemble
an :class:`EnigmaMachine <enigma.machine.EnigmaMachine>` from parts, and those
parts may raise these exceptions themselves:

* ``rotor.rotors.RotorError``
* ``plugboard.PlugboardError``


Rotors & Reflectors
-------------------

The ``Rotor`` class represents the Enigma rotors, also known as the wheels or
*Walzen* in German. They are the most important parts of the machine.

Rotors have little use on their own. They are placed inside an :class:`EnigmaMachine
<enigma.machine.EnigmaMachine>` object, which then calls the public ``Rotor``
methods.

Rotor class reference
~~~~~~~~~~~~~~~~~~~~~

.. class:: enigma.rotors.rotor.Rotor(model_name, wiring[, ring_setting=0[, stepping=None]])

   A rotor has 26 circularly arranged pins on the right (entry) side and 26
   contacts on the left side. Each pin is connected to a single contact by
   internal wiring, thus establishing a substitution cipher. We represent this
   wiring by establishing a mapping from a pin to a contact (and vice versa for
   the return path). Internally we number the pins and contacts from 0-25 in a
   clockwise manner with 0 being the "top".

   An alphabetic or numeric ring is fastened to the rotor by the operator. The
   labels of this ring are displayed to the operator through a small window on
   the top panel. The ring can be fixed to the rotor in one of 26 different
   positions; this is called the ring setting (*Ringstellung*). We will number
   the ring settings from 0-25 where 0 means no offset (e.g. the letter "A" is
   mapped to pin 0 on an alphabetic ring). A ring setting of 1 means the letter
   "B" is mapped to pin 0.

   Each rotor can be in one of 26 positions on the spindle, with position 0
   where pin/contact 0 is being indicated in the operator window. The rotor
   rotates towards the operator by mechanical means during normal operation as
   keys are being pressed during data entry. Position 1 is thus defined to be
   one step from position 0. Likewise, position 25 is the last position before
   another step returns it to position 0, completing 1 trip around the spindle.

   Finally, a rotor has a "stepping" or "turnover" parameter. Physically this
   is implemented by putting a notch on the alphabet ring and it controls when
   the rotor will "kick" the rotor to its left, causing the neighbor rotor to
   rotate. Most rotors had one notch, but some Kriegsmarine rotors had 2
   notches and thus rotated twice as fast.

   Note that we allow the ``stepping`` parameter to be ``None``. This indicates
   the rotor does not rotate. This allows us to model the entry wheel and
   reflectors as stationary rotors. The fourth rotor on the Kriegsmarine M4
   models (*Beta* or *Gamma*) did not rotate.
   
   The rotor constructor establishes the rotor characteristics.

   :param string model_name: e.g. "I", "II", "III", "Beta", "Gamma"

   :param string wiring: This should be a string of 26 uppercase characters
      A-Z that represent the internal wiring transformation of the signal
      as it enters from the right side. This is the format used in various online
      resources. For example, for the Wehrmacht Enigma type I rotor the
      mapping is ``"EKMFLGDQVZNTOWYHXUSPAIBRCJ"``.

   :param integer ring_setting: This should be an integer from 0-25, inclusive,
      which indicates the *Ringstellung*. A value of 0 means there is no offset; e.g.
      the letter ``A`` is fixed to pin ``0``. A value of 1 means ``B`` is mapped
      to pin ``0``.

   :param stepping: This is the stepping or turnover parameter. When it is an
      iterable, for example a string such as "Q", this indicates that when
      the rotor transitions from "Q" to "R" (by observing the operator
      window), the rotor will "kick" the rotor to its left, causing it to
      rotate. If the rotor has more than one notch, a string of length 2 could
      be used, e.g. "ZM".  Another way to think of this parameter is that when
      a character in the stepping string is visible in the operator window, a
      notch is lined up with the pawl on the left side of the rotor.  This
      will allow the pawl to push up on the rotor *and* the rotor to the left
      when the next key is depressed. A value of ``None`` means this rotor does
      not rotate.

   :raises RotorError: when an invalid parameter is supplied

   Note that for purposes of simulation, our rotors will always use alphabetic
   labels A-Z. In reality, the Heer & Luftwaffe devices used numbers 01-26, and
   Kriegsmarine devices used A-Z. Our usage of A-Z is simply for simulation
   convenience. In the future we may allow either display.

   .. method:: set_display(val)

      Spin the rotor such that the string ``val`` appears in the operator
      window. This sets the internal position of the rotor on the axle and thus
      rotates the pins and contacts accordingly.

      A value of 'A' for example puts the rotor in position 0, assuming an
      internal ring setting of 0.

      :param string val: rotor position which must be in the range ``A-Z``
      :raises RotorError: when an invalid position value is supplied

   .. method:: get_display()

      :returns: current rotor position in the range ``A-Z``
      :rtype: string

   .. method:: signal_in(n)

      Simulate a signal entering the rotor from the right at a given pin
      position n.

      :param integer n: pin number between 0 and 25
      :returns: the contact number of the output signal (0-25)
      :rtype: integer

   .. method:: signal_out(n)

      Simulate a signal entering the rotor from the left at a given contact
      position n.

      :param integer n: contact number between 0 and 25
      :returns: the pin number of the output signal (0-25)
      :rtype: integer

   .. method:: notch_over_pawl()

      Returns ``True`` if this rotor has a notch in the stepping position and
      ``False`` otherwise.

      :rtype: Boolean

   .. method:: rotate()

      Rotates the rotor forward.


A note on the entry wheel and reflectors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The entry wheel (*ETW*) is a special non-movable rotor that sits on the far
right of the rotor array. It connects the rotor array with the plugboard wiring.
On Wehrmacht Enigmas, the entry wheel performs a straight-through mapping. In
other words, the wire from the 'A' key is passed to pin position 0, 'B' to pin
position 1, etc. Thus there is no need to simulate the entry wheel given our
current scope to model only military Enigmas.

The reflector, or *Umkehrwalze* (UKW), sits at the far left of the rotor array.
It simply reflects the incoming signal coming from the right back through the
left side of the rotors. We can thus model the reflector as a special non-movable
rotor.

If you decide to create your own reflector, and you desire to maintain
reciprocal encryption & decryption, your connections must be made in pairs. Thus
if you wire 'A' to 'G', you must also wire 'G' to 'A', and so on.


Rotor & reflector factory functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While it is possible to create your own rotor type, for convenience two factory
functions have been created to return rotors and reflectors used by the
Wehrmacht. These factory functions let you refer to the rotors and reflectors by
name instead of providing their internal wiring every time you need one (which
would be both tedious and error prone).

The following table lists the names of the rotors we currently simulate.

.. _rotor-table-label:

.. table:: Simulated rotor models

   +-------------------+------------------------+
   | Rotor names       | Enigma Models          |
   +===================+========================+
   | I, II, III, IV, V | All Wehrmacht models   |
   +-------------------+------------------------+
   | VI, VII, VIII     | Kriegsmarine M3 & M4   |
   +-------------------+------------------------+
   | Beta, Gamma       | Kriegsmarine M4        |
   |                   | (with thin reflectors) |
   +-------------------+------------------------+

Any of the names in the first column of the above table can be used by the
factory function :func:`enigma.rotors.factory.create_rotor`, described below.

Likewise there exists a factory function to create reflectors by name. The
following table lists the names of the supported reflectors.

.. _reflector-table-label:

.. table:: Simulated reflector types

   +-------------------+------------------------+
   | Reflector names   | Enigma Models          |
   +===================+========================+
   | B, C              | All Wehrmacht models   |
   +-------------------+------------------------+
   | B-Thin, C-Thin    | Kriegsmarine M4        |
   |                   | (with Beta & Gamma     |
   |                   | rotors)                |
   +-------------------+------------------------+

The two factory functions are described next:

.. function:: enigma.rotors.factory.create_rotor(model[, ring_setting=0])

   Create and return a :class:`Rotor <enigma.rotors.rotor.Rotor>` object with
   the given ring setting.

   :param string model: the model name to create; see the :ref:`rotor-table-label` table
   :param integer ring_setting: the ring setting (0-25) to use
   :returns: the newly created :class:`Rotor <enigma.rotors.rotor.Rotor>`
   :raises RotorError: when an unknown model name is provided


.. function:: enigma.rotors.factory.create_reflector(model)

   Create and return a :class:`Rotor <enigma.rotors.rotor.Rotor>` object that
   is meant to be used in the reflector role.

   :param string model: the model name to create; see the :ref:`reflector-table-label` table
   :returns: the newly created reflector, which is actually of type
      :class:`Rotor <enigma.rotors.rotor.Rotor>`
   :raises RotorError: when an unknown model name is provided


Rotor exceptions
~~~~~~~~~~~~~~~~

:class:`Rotor <enigma.rotors.rotor.Rotor>` objects may raise
``enigma.rotors.RotorError`` when an invalid constructor argument is given, or
if the rotor object is given an invalid parameter during a :meth:`set_display
<enigma.rotors.rotor.Rotor.set_display>` operation.


Plugboards
----------

The plugboard, or *Steckerbrett* in German, allows the operator to swap up to 10
keys and indicator lamps for increased key strength.

Plugboards have little use on their own. They are placed inside an :class:`EnigmaMachine
<enigma.machine.EnigmaMachine>` object, which then calls the public ``Plugboard``
methods.

Plugboard class reference
~~~~~~~~~~~~~~~~~~~~~~~~~

.. class:: enigma.plugboard.Plugboard([wiring_pairs=None])

   The plugboard allows the operator to swap letters before and after the entry
   wheel. This is accomplished by connecting cables between pairs of plugs that
   are marked with letters (Heer & Luftwaffe models) or numbers (Kriegsmarine).
   Ten cables were issued with each machine; thus up to 10 of these swappings
   could be used as part of a machine setup.

   Each cable swaps both the input and output signals. Thus if A is connected
   to B, A crosses to B in the keyboard to entry wheel direction and also in
   the reverse entry wheel to lamp direction.

   The constructor configures the plugboard according to a list or tuple of
   integer pairs, or None.

   :param wiring_pairs: A value of ``None`` or an empty list/tuple indicates no
      plugboard connections are to be used (i.e. a straight mapping).  Otherwise
      ``wiring_pairs`` must be an iterable of integer pairs, where each integer
      is between 0-25, inclusive. At most 10 such pairs can be specified. Each
      value represents an input/output path through the plugboard. It is invalid
      to specify the same path more than once in the list.

   :raises PlugboardError: If an invalid ``wiring_pairs`` parameter is given.

   .. classmethod:: from_key_sheet([settings=None])

      This is a convenience function to build a plugboard according to a 
      settings string as you may find on a key sheet.

      Two syntaxes are supported, the Heer/Luftwaffe and Kriegsmarine styles:

      In the Heer syntax, the settings are given as a string of
      alphabetic pairs. For example: ``'PO ML IU KJ NH YT GB VF RE DC'``.

      In the Kriegsmarine syntax, the settings are given as a string of number
      pairs, separated by a '/'. Note that the numbering uses 1-26, inclusive.
      For example: ``'18/26 17/4 21/6 3/16 19/14 22/7 8/1 12/25 5/9 10/15'``.

      To specify no plugboard connections, settings can be ``None`` or an empty
      string.

      :param settings: A settings string as described above, or ``None``.
      :raises PlugboardError: If the settings string is invalid, or if
         it contains more than 10 pairs. Each plug should be present at
         most once in the settings string.

   .. method:: signal(n)

      Simulate a signal entering the plugboard on wire n, where n must be
      an integer between 0 and 25.

      :param integer n: The wire number the input signal is on (0-25).
      :returns: The wire number of the output signal (0-25).
      :rtype: integer

      Note that since the plugboard always crosses pairs of wires, it doesn't
      matter what direction (keyboard -> entry wheel or vice versa) the signal
      is coming from.


Plugboard exceptions
~~~~~~~~~~~~~~~~~~~~

:class:`Plugboard <enigma.plugboard.Plugboard>` objects may raise
``enigma.plugboard.PlugboardError`` when an invalid constructor argument is given.
