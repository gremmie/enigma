User's guide
============

This short guide attempts to get you up and running with Py-Enigma quickly. For
more detailed information, please see the :doc:`Reference manual <reference>`.


If you are new to Enigma machines
---------------------------------

This guide assumes you know the basics of Enigma machines. Before proceeding
with Py-Enigma please explore some of the links presented in the
:ref:`references-label`. For the most complete and detailed description of how
an Enigma machine works, please see Dirk Rijmenants' excellent `Technical
Details of the Enigma Machine
<http://users.telenet.be/d.rijmenants/en/enigmatech.htm>`_.

Building your Enigma machine
----------------------------

If you are interested in working with historically accurate Enigma machines, the
easiest way to build your first machine is to use the "key sheet" shortcut
functions. If instead you wish to experiment with custom designed rotors or
configurations, you can build a machine out of separate components by hand.
These two approaches are demonstrated in the following sections.

Using key sheet shortcuts
~~~~~~~~~~~~~~~~~~~~~~~~~

During the war, Enigma machine operators re-configured their machines every day
according to a code book, or key sheet, to help increase security. Each key
sheet contained daily Enigma settings for one month. Before transmitting the
first message of the day, the operator looked up the current day on the key
sheet for the given month and configured the machine accordingly. The key sheet
specified:

* *Walzenlage*: what rotors to use, and what order to put them into the machine
* *Ringstellung*: the ring settings for each rotor
* *Steckerverbindungen*: the plugboard connections
* *Kenngruppen*: special text fragments that should be transmitted to identify
  the transmitter's key settings to any receiver. This is also known as the
  *message indicator*.

The reflector setting was usually fixed and not changed once in the field. The
choice of reflector seems to have been decided at the unit level to establish
different networks. Of course our simulation is not hindered by these logistical
concerns, and our simulated key sheets will also specify reflector type.

When an Enigma machine operator received a message from a radio operator,
probably his first task was to determine what key settings were used to transmit
the message. For example, the message could have been transmitted the day
before, and he was only handed the message just now. This was accomplished by
transitting (in the clear) certain text fragments, the so-called *Kenngruppen*,
at certain points in the message. By examining these text groups, the operator
could scan the key sheet for today and perhaps the past few days and hopefully
identify what day the message was sent. The operator would then reconfigure his
Enigma machine accordingly and decode the message. The *Kenngruppen* was ignored
when decrypting the actual message.

The :class:`EnigmaMachine <enigma.machine.EnigmaMachine>` class has two
class methods for constructing machines from key sheet data. The first class
method is called :meth:`from_key_sheet
<enigma.machine.EnigmaMachine.from_key_sheet>`::

   from enigma.machine import EnigmaMachine

   machine = EnigmaMachine.from_key_sheet(
          rotors='IV V I', 
          reflector='B',
          ring_settings='21 15 16',
          plugboard_settings='AC LS BQ WN MY UV FJ PZ TR OK')

This is all well and good if you wish to simulate an army or air force Enigma
machine. But what about navy (*Kriegsmarine*) models? Navy Enigma machines and
key sheets have slightly different nomenclature. This is also no problem for
Py-Enigma::
   
   machine = EnigmaMachine.from_key_sheet(
          rotors='Beta VII IV V',
          reflector='B-Thin',
          ring_settings='G N O',
          plugboard_settings='18/26 17/4 21/6 3/16 19/14 22/7 8/1 12/25 5/9 10/15')

Some notes on the parameters:

* ``rotors`` can either be a space separated list of rotor names, or a list of
  rotor name strings. For a complete list of supported rotor names, see
  :ref:`rotor-table-label`.
* ``reflector`` is a string that names the reflector to use. For a complete list
  of supported reflector names, see :ref:`reflector-table-label`.
* ``ring_settings`` can be a space separated list of uppercase letters or
  numbers, as would be found on a key sheet. An empty string or ``None`` means
  ring settings of all 'A' or 1.
* ``plugboard_settings`` can either be space separated uppercase letter pairs,
  or slash separated numbers. Note that 'AB' is equivalent to '1/2', etc.

.. warning::

   ``ring_settings`` can also take a list of integers, but these integers are
   **0-based**. Remember that when using a string of numbers they are
   **1-based** to correspond to actual historical key sheet data. In other
   words, these values produce identical ring settings: ``[0, 5, 15]``,
   ``'A F P'``, and ``'1 6 16'``.

The second shortcut function allows you to keep your key settings stored in an
external file::

   from enigma.machine import EnigmaMachine

   with open('my_enigma_keys.txt', 'r') as f:
      machine = EnigmaMachine.from_key_file(f, day=13)

The class method :meth:`from_key_file
<enigma.machine.EnigmaMachine.from_key_file>` builds an :class:`EnigmaMachine
<enigma.machine.EnigmaMachine>` from settings stored in a simulated monthly key
sheet file. The format of this file is explained in :doc:`keyfile`. The ``day``
argument allows you to specify the day of the month (1-31). If this parameter is
omitted or ``None``, the day value is obtained from the current date.


Constructing by hand
~~~~~~~~~~~~~~~~~~~~

It is also possible to "build an Enigma machine by hand" by explicitly providing
the component objects to the :class:`EnigmaMachine
<enigma.machine.EnigmaMachine>` constructor. This makes it possible to invent
different rotor and reflector types::

   from enigma.rotors.rotor import Rotor
   from enigma.plugboard import Plugboard
   from enigma.machine import EnigmaMachine

   r1 = Rotor('my rotor1', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', ring_setting=0, stepping='Q')
   r2 = Rotor('my rotor2', 'AJDKSIRUXBLHWTMCQGZNPYFVOE', ring_setting=5, stepping='E')
   r3 = Rotor('my rotor3', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', ring_setting=15, stepping='V')

   reflector = Rotor('my reflector', 'FVPJIAOYEDRZXWGCTKUQSBNMHL')

   pb = Plugboard.from_key_sheet('PO ML IU KJ NH YT GB VF RE DC')

   machine = EnigmaMachine([r1, r2, r3], reflector, pb)

This example illustrates a few different things:

* When calling the :class:`Rotor <enigma.rotors.rotor.Rotor>` constructor
  directly, the internal wiring is specified as a 26-character long string which
  specifies the cipher substitution. This notation is consistent with several
  online sources of Enigma information.
* :class:`Rotor <enigma.rotors.rotor.Rotor>` ``ring_setting`` arguments are
  0-based integers (0-25).
* :class:`Rotor <enigma.rotors.rotor.Rotor>` ``stepping`` arguments specify 
  when rotors turn their neighbors. For more information see the 
  :class:`Rotor <enigma.rotors.rotor.Rotor>` reference.
* Reflectors are simulated as rotors that have no ring setting or stepping
  capability.
* :class:`Plugboard <enigma.plugboard.Plugboard>` objects have a convenient
  :meth:`from_key_sheet <enigma.plugboard.Plugboard.from_key_sheet>` class method 
  constructor that works in exactly the same way as the previous example.
* When calling the :class:`EnigmaMachine <enigma.machine.EnigmaMachine>`
  constructor directly, the rotor assignment is specified by a list of rotors
  where order specifies the left-to-right order in the machine.

.. note::

   If you decide to create your own reflector, and you desire to maintain
   reciprocal encryption & decryption (a fundamental characteristic of war-time
   Enigma machines), your connections must be made in pairs. Thus if you wire
   'A' to 'G', you must also wire 'G' to 'A', and so on.

For more details on the various constructor arguments, please see the
:doc:`reference`.
   

Encrypting & Decrypting
-----------------------

Now that you have built your Enigma machine, you probably want to start using it
to encrypt and decrypt text! The first step is to set your initial rotor
positions. This is critical if you want someone else to understand your message!

::

   machine.set_display('XYZ')       # set rotor positions

The value given to :meth:`set_display
<enigma.machine.EnigmaMachine.set_display>` is a simple string, which must have
one uppercase letter per rotor in your machine. In this example, we are
setting the leftmost rotor to 'X', the middle rotor to 'Y', and the rightmost
rotor to 'Z'.

If you ever need to obtain the current rotor positions, you can use the
:meth:`get_display <enigma.machine.EnigmaMachine.get_display>` method::

   position = machine.get_display()    # read rotor position

.. note::

   The :meth:`set_display <enigma.machine.EnigmaMachine.set_display>` method
   always takes letters for simulation convenience. If you are simulating an
   Enigma machine with numeric rotors, you'll have to translate the numbers to
   the appropriate letters. On actual Enigma machines, a label on the inside box
   lid had such a table to aid the operator.

Next, you can simulate a single key press::

   c = machine.key_press('A')

The input to :meth:`key_press <enigma.machine.EnigmaMachine.key_press>` is a
string that consists of a single uppercase letter. Invalid input will raise an
``EnigmaError`` exception. The transformed text is returned.

To process a whole string of text::

   c = machine.process_text('This is a test!', replace_char='X')

The :meth:`process_text <enigma.machine.EnigmaMachine.process_text>` method
accepts an arbitrary string and performs some processing on it before internally
calling :meth:`key_press <enigma.machine.EnigmaMachine.key_press>` on each element of
the string. 

First, all input is converted to uppercase. Next, any character not in the
Enigma uppercase character set is either replaced or dropped from the input
according to the ``replace_char`` parameter. If ``replace_char`` is a string of
one character, it is used as the replacement character. If it is ``None``, the
invalid input character is removed from the message. Thus the previous example
is equivalent to::

   c = machine.process_text('THISXISXAXTESTX')

This is all you need to start creating encrypted and decrypted messages.


Example communication procedure
-------------------------------

The Wehrmacht had various elaborate procedures for transmitting and receiving
messages. These procedures varied by service branch and also changed during the
course of the war.  In general, the Kriegsmarine procedures were more elaborate
and involved not only key sheets but other auxiliary documents. On top of this,
each branch of the military had its own conventions for encoding abbreviations,
numbers, space characters, place names, etc. Important words or phrases may need
to be repeated or stressed in some way. 

We will now present a simplified scenario based on a procedure employed by the
army (*Heer*) after 1940. This example is based upon one found in Dirk
Rijmenants' simulator manual, which is based upon a real-life example from Frode
Weierud's `Cryptocellar <http://cryptocellar.org>`_ website.

Suppose a message needs to be transmitted. The operator of the transmitting
machine consults his key sheet and configures his machine according to the daily
settings found inside. Let's suppose the key sheet dictates the following
initial parameters for the current day:

* Rotor usage and order is *II IV V*
* Ring settings for each rotor, in order, are: *B U L*
* Plugboard settings are: *AV BS CG DL FU HZ IN KM OW RX*
* One of the daily Kenngruppen possibilities is *UGZ*

Let us also assume the reflector employed by this army unit is 'B'.

The operator then configures his machine::

   machine = EnigmaMachine.from_key_sheet(
          rotors='II IV V',
          reflector='B',
          ring_settings='B U L',
          plugboard_settings='AV BS CG DL FU HZ IN KM OW RX')

Suppose the Enigma operator was handed a message for transmit by an officer
which reads "The Russians are coming!" The operator would first randomly decide
two things:

* Initial rotor positions, say ``WXC``
* A three letter *message key*, say ``BLA``

The operator would then turn the rotor thumb wheels to set the initial rotor
position and then type the three letter message key to produce an encrypted
message key::

   machine.set_display('WXC')    # set initial rotor positions
   enc_key = machine.process_text('BLA')      # encrypt message key

In this example, the encrypted key turns out to be ``KCH``. This is written down
for later. 

The operator then sets the rotors to the unencrypted message key ``BLA`` and
then types in the officer's message, performing various substitutions and
transformations according to training and current procedures. In our simple
case, he performs the following::

   machine.set_display('BLA')    # use message key BLA
   ciphertext = machine.process_text('THEXRUSSIANSXAREXCOMINGX')
   print(ciphertext)

This produces the ciphertext ``NIBLFMYMLLUFWCASCSSNVHAZ``.

Next, between the Enigma operator and the radio operator, a message is formed
up. This message includes the following components:

* The time of transmission
* The station identification for transmitter and intended recipient(s)
* The message length; in our case this is 24
* The initial rotor positions in unencrypted form (``WXC``)
* The encrypted message key value (``KCH``)
* The unencrypted message indicator (*Kenngruppen*)
* The encrypted message contents

In our example, the message handed over to the radio operator to be transmitted
by either Morse code or perhaps even voice would look something like this::

   U6Z DE C 1500 = 24 = WXC KCH =

   BNUGZ NIBLF MYMLL UFWCA 
   SCSSN VHAZ=

The top line indicates day 31, station C transmits to station U6Z, sent at 1500
hours and contains 24 letters. The starting position is ``WXC`` and the
encrypted message key is ``KCH``.

Next we have the body of the message. The army transmitted messages in 5 letter
groups. The first group contains the Kenngruppen, or indicator. Procedure
required the operator pick one of the Kenngruppen possibilities from the key
sheet, and then pad it out with two random letters. Here the operator chose to
prepend ``BN`` to the Kenngruppen value of ``UGZ``. He could have also appended
the two letters, or perhaps appended one and prepended the other.

After the message indicator group, the encrypted text follows in 5 letter
groups.

Now at receiving station U6Z, the radio operator receives the over-the-air
message and types or writes it up in the form shown and hands it to the Enigma
operator.

The Enigma operator first looks for the message indicator. He uses the group
``BNUGZ`` and scans his key sheet for either ``BNU``, ``NUG``, or ``UGZ``. He
could presumably also use the date information found in the message preamble to
help his search of the key sheet. If everything checks out the operator now
knows which entry in his monthly key sheet to use.  Thus, as was done at the
transmitting station, he configures his Enigma according to the key sheet::

   machine = EnigmaMachine.from_key_sheet(
          rotors='II IV V',
          reflector='B',
          ring_settings='B U L',
          plugboard_settings='AV BS CG DL FU HZ IN KM OW RX')

The receiving operator then must decrypt the message key::

   machine.set_display('WXC')
   msg_key = machine.process_text('KCH')

This should reveal that the message key is the original ``BLA``. The rotors are
then set to this value and the message can be decrypted, taking care to ignore
the Kenngruppen::

   machine.set_display(msg_key)     # original message key is BLA
   plaintext = machine.process_text('NIBLFMYMLLUFWCASCSSNVHAZ')
   print(plaintext)

The Enigma operator then decodes the message "THEXRUSSIANSXAREXCOMINGX". He then
uses his training and procedures to further process the message. Finally, the
somewhat troubling message "The Russians are coming" is handed to his commanding
officer.

