=========
Py-Enigma
=========
A historically accurate Enigma Machine library written in Python 3
------------------------------------------------------------------

- **Author:** Brian Neal <bgneal@gmail.com>
- **Version:** 1.0.2
- **Date:** December 30, 2025
- **Home Page:** https://github.com/gremmie/enigma
- **License:** MIT License (see LICENSE.txt)
- **Documentation:** http://py-enigma.readthedocs.org/
- **Support:** https://github.com/gremmie/enigma/issues


Overview
--------

**Py-Enigma** is a Python 3 library for simulating the `Enigma machines`_ used
by the German armed forces (Wehrmacht) during World War 2. Py-Enigma makes it
possible to both encrypt and decrypt messages that can be sent to, or received
from, actual Enigma machines used by the German army (Heer), air force
(Luftwaffe), and navy (Kriegsmarine).

It is my hope that library will be useful to Enigma enthusiasts, historians, and
students interested in cryptography.

Py-Enigma strives to be Pythonic, easy to use, comes with unit tests, and
documentation.


Scope
-----

The current scope of Py-Enigma is to simulate Wehrmacht Enigma machines.
Simulation of other Enigmas, such as the various commercial, railroad, foreign,
and Abwher (Military Intelligence) models may come later if there is enough
interest and data available.

Currently, Py-Enigma can simulate the 3 and 4 rotor Enigma machines used by the
German army, navy, and air force.


Quick Example
-------------

This example shows how the library can be used to decode a message using the
procedure employed by the German army::
   
   from enigma.machine import EnigmaMachine

   # setup machine according to specs from a daily key sheet:

   machine = EnigmaMachine.from_key_sheet(
          rotors='II IV V',
          reflector='B',
          ring_settings=[1, 20, 11],
          plugboard_settings='AV BS CG DL FU HZ IN KM OW RX')

   # set machine initial starting position
   machine.set_display('WXC')

   # decrypt the message key
   msg_key = machine.process_text('KCH')

   # decrypt the cipher text with the unencrypted message key
   machine.set_display(msg_key)

   ciphertext = 'NIBLFMYMLLUFWCASCSSNVHAZ'
   plaintext = machine.process_text(ciphertext)

   print(plaintext)

This program prints::

   THEXRUSSIANSXAREXCOMINGX

Py-Enigma also includes a command-line application for processing messages.
Assuming you have a proper key file that contains the same initial settings as
the code above, the above example can be performed on the command-line::

   $ pyenigma --key-file=keys.txt --start=WXC --text='KCH'
   BLA
   $ pyenigma --key-file=keys.txt --start=BLA --text='NIBLFMYMLLUFWCASCSSNVHAZ'
   THEXRUSSIANSXAREXCOMINGX

The format of the key file can be found in the documentation.


Requirements
------------

Py-Enigma is written in Python_, specifically Python 3.2. It has no other
requirements or dependencies.


Installation
------------

Py-Enigma is available on the `Python Package Index`_ (PyPI). You can install it
using pip_::

   $ python3 -m pip install py-enigma

If you aren't familiar with installing Python packages, please see, for
example, the `Python Packaging Installing Packages tutorial`_.

The latest version of Py-Enigma can always be found at the `Py-Enigma GitHub page`_.


Documentation
-------------

The latest documentation is available at `Read the Docs
<http://readthedocs.org/projects/py-enigma/>`_. There you can `browse the
documentation online <http://readthedocs.org/docs/py-enigma/en/latest/>`_, or
`download it in a variety of formats
<http://readthedocs.org/projects/py-enigma/downloads/>`_.

Sources for the documentation are also included in Sphinx_ format. If you
install Sphinx you can generate the documentation in several output formats.


Support
-------

Support is provided at the `issue tracker`_ at the `Py-Enigma GitHub page`_.
If you have general questions or comments, please feel free to email me (address
at the top of this file). 

And please, if you use Py-Enigma for anything, even if it is just learning,
please let me know!


Acknowledgements & References
-----------------------------

This software would not have been possible without the thorough and detailed
descriptions of the Enigma machine on Dirk Rijmenants' incredible `Cipher
Machines and Cryptology website`_. In particular, his `Technical Details of the
Enigma Machine`_ page was a gold mine of information.

Dirk has also written an `Enigma simulator`_ in Visual Basic. Although I did not
look at his source code, I did use his simulator to check the operation of
Py-Enigma.

I would also like to recommend the photos and video at Dr. Thomas B. Perera's
`Enigma Museum`_.

Another good website is `The Enigma and the Bombe`_ by Graham Ellsbury.

A nice video which shows the basic components and operation of the Enigma
Machine is on YouTube: `Nadia Baker & Enigma demo`_.


.. _Enigma machines: http://en.wikipedia.org/wiki/Enigma_machine
.. _Python: http://www.python.org
.. _Python Package Index: http://pypi.python.org/pypi/py-enigma/
.. _Python Packaging Installing Packages tutorial: https://packaging.python.org/en/latest/tutorials/installing-packages/
.. _pip: http://pip.openplans.org/
.. _Py-Enigma GitHub page: https://github.com/gremmie/enigma
.. _Sphinx: http://sphinx.pocoo.org/
.. _issue tracker: https://github.com/gremmie/enigma/issues
.. _Cipher Machines and Cryptology website: https://www.ciphermachinesandcryptology.com
.. _Technical Details of the Enigma Machine: https://www.ciphermachinesandcryptology.com/en/enigmatech.htm
.. _Enigma simulator: https://www.ciphermachinesandcryptology.com/en/enigmasim.htm
.. _Enigma Museum: http://w1tp.com/enigma/
.. _The Enigma and the Bombe: http://www.ellsbury.com/enigmabombe.htm
.. _Nadia Baker & Enigma demo: http://youtu.be/HBHYAzuVeWc
