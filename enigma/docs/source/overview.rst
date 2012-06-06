Overview
========

Introduction
------------

**Py-Enigma** is a Python 3 library for simulating the `Enigma machines`_ used
by the German armed forces (*Wehrmacht*) during World War II. Py-Enigma is
historically accurate, meaning it can interoperate with actual Wehrmacht Enigma
machines. In other words, Py-Enigma can decrypt coded messages created with an
actual Enigma, and it can encrypt messages that an actual Enigma can decode.

It is hoped that this library will be useful to Enigma enthusiasts, historians,
and students interested in cryptography.

Py-Enigma strives to be Pythonic, easy to use, and comes with both unit tests
and documentation. Py-Enigma is a library for building applications for
encrypting and decrypting Enigma messages. However, it also ships with a simple
command-line application that can encrypt & decrypt messages for scripting and
experimentation.

Scope
-----

Currently, Py-Enigma simulates the Wehrmacht Enigma machines. This includes the
3 and 4 rotor machines used by the German Army (*Heer*), Air Force
(*Luftwaffe*), and Navy (*Kriegsmarine*). Simulation of other Enigma models,
including the various commercial, railroad, foreign market, and Abhwer (Military
Intelligence) models may come later if there is enough interest and data
available.

Quick Example
-------------

This example shows how the library can be used to decode a message using the
procedure employed by the German army

.. literalinclude:: ../../examples/example1.py
   
This program prints::

   THEXRUSSIANSXAREXCOMINGX

Py-Enigma also includes a command-line application for processing messages.
Assuming you have a proper key file that contains the same initial settings as
the code above, the above example can be performed on the command-line::

   $ pyenigma.py --key-file=keys.txt --start=WXC --text='KCH'
   BLA
   $ pyenigma.py --key-file=keys.txt --start=BLA --text='NIBLFMYMLLUFWCASCSSNVHAZ'
   THEXRUSSIANSXAREXCOMINGX

The format of the key file can be found in :doc:`keyfile`.

Requirements
------------

Py-Enigma is written in Python_, specifically Python 3.2. It has no other
requirements or dependencies.

Installation
------------

Py-Enigma is available on the `Python Package Index`_ (PyPI). You can install it
using pip_::

   $ pip install py-enigma             # install
   $ pip install --upgrade py-enigma   # upgrade

You may also download a tarball or .zip file of the latest code using the "get
source" link on the `Py-Enigma Bitbucket page`_. Alternatively if you use
Mercurial_, you can clone the repository with the following command::

   $ hg clone https://bitbucket.org/bgneal/enigma

If you did not use pip, you can install with this command::

   $ python setup.py install


Support & Source
----------------

All support takes place at the `Py-Enigma Bitbucket page`_. Please enter any
feature requests or bugs into the `issue tracker`_.

You may also clone the Mercurial_ source code repository::

   $ hg clone https://bitbucket.org/bgneal/enigma


.. _references-label:

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
.. _Py-Enigma Bitbucket page: https://bitbucket.org/bgneal/enigma
.. _pip: http://www.pip-installer.org
.. _Mercurial: http://mercurial.selenic.com/
.. _issue tracker: https://bitbucket.org/bgneal/enigma/issues
.. _Cipher Machines and Cryptology website: http://users.telenet.be/d.rijmenants/index.htm
.. _Technical Details of the Enigma Machine: http://users.telenet.be/d.rijmenants/en/enigmatech.htm
.. _Enigma simulator: http://users.telenet.be/d.rijmenants/en/enigmasim.htm
.. _Enigma Museum: http://w1tp.com/enigma/
.. _The Enigma and the Bombe: http://www.ellsbury.com/enigmabombe.htm
.. _Nadia Baker & Enigma demo: http://youtu.be/HBHYAzuVeWc
