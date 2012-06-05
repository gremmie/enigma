pyenigma command-line application
=================================

Py-Enigma includes a simple application, *pyenigma.py*, to let you perform
Enigma text transformations on the command-line. This allows for quick
experimentation and scripting of operations.

Getting help
------------

To get help and see all the available options, invoke pyenigma.py with the
``--help`` option::

   $ python pyenigma.py --help

   usage: pyenigma.py [-h] [-k KEY_FILE] [-d DAY] [-r ROTOR [ROTOR ...]]
                      [-i RING_SETTING [RING_SETTING ...]]
                      [-p PLUGBOARD [PLUGBOARD ...]] [-u REFLECTOR] [-s START]
                      [-t TEXT] [-f FILE] [-x REPLACE_CHAR] [-z] [-v]

   Encrypt/decrypt text according to Enigma machine key settings

   optional arguments:
     -h, --help            show this help message and exit
     -k KEY_FILE, --key-file KEY_FILE
                           path to key file for daily settings
     -d DAY, --day DAY     use the settings for day DAY when reading key file
     -r ROTOR [ROTOR ...], --rotors ROTOR [ROTOR ...]
                           rotor list ordered from left to right; e.g III IV I
     -i RING_SETTING [RING_SETTING ...], --ring-settings RING_SETTING [RING_SETTING ...]
                           ring setting list from left to right; e.g. A A J
     -p PLUGBOARD [PLUGBOARD ...], --plugboard PLUGBOARD [PLUGBOARD ...]
                           plugboard settings
     -u REFLECTOR, --reflector REFLECTOR
                           reflector name
     -s START, --start START
                           starting position
     -t TEXT, --text TEXT  text to process
     -f FILE, --file FILE  input file to process
     -x REPLACE_CHAR, --replace-char REPLACE_CHAR
                           if the input text contains chars not found on the
                           enigma keyboard, replace with this char [default: X]
     -z, --delete-chars    if the input text contains chars not found on the
                           enigma keyboard, delete them from the input
     -v, --verbose         provide verbose output; include final rotor positions

   Key settings can either be specified by command-line arguments, or read
   from a key file. If reading from a key file, the line labeled with the
   current day number is used unless the --day argument is provided.

   Text to process can be supplied 3 ways:

      if --text=TEXT is present TEXT is processed
      if --file=FILE is present the contents of FILE are processed
      otherwise the text is read from standard input

   Examples:

       $ pyenigma.py --key-file=enigma.keys -s XYZ -t HELLOXWORLDX
       $ pyenigma.py -r III IV V -i 1 2 3 -p AB CD EF GH IJ KL MN -u B -s XYZ
       $ pyenigma.py -r Beta III IV V -i A B C D -p 1/2 3/4 5/6 -u B-Thin -s WXYZ
     
There are numerous options, but most are hopefully self-explanatory. There are
two ways to invoke *pyenigma.py*:

#. Explicitly specifying all initial key settings
#. Using a key file to initialize the Enigma machine


Specifying all key settings
---------------------------

Here are some examples of specifying all the key settings on the command-line::

   $ python pyenigma.py --rotors I IV V --ring-settings 5 17 8 \
     --plugboard AV BS CG DL FU HZ IN KM OW RX --reflector C \
     --start=DRX

   $ python pyenigma.py -r I IV V -i 5 17 8 \
     -p AV BS CG DL FU HZ IN KM OW RX -u C -s DRX

These two invocations create the same settings, the first uses long form
option names, while the second uses short form.

If no ``--text`` or ``--file`` options are provided, *pyenigma.py* will prompt
for input::

   $ python pyenigma.py -r I IV V -i 5 17 8 -p AV BS CG DL FU HZ IN KM OW RX -u C -s DRX
   --> THIS IS MY SECRET MESSAGE
   QAWYWZBVCDEZWOHPVCKFMMFLY


Using a key file for settings
-----------------------------

It is often unwieldy to type so many options on the command-line, so
*pyenigma.py* provides a way to store key settings in a simulated key sheet
file::

   $ python pyenigma.py --key-file keyfile --start='AAB' --day=29 --text='HERE IS MY MESSAGE'
   OCJNFADTCMQIBJLYWW


If the ``--day`` option is omitted, the day is determined from the current date.

The format of the key sheet file is described in :doc:`keyfile`.


Verbose output
--------------

The ``--verbose`` or ``-v`` option is useful if you wish to view the final rotor
positions and view how many times the rotors stepped while processing your
text::

   $ python pyenigma.py --key-file keyfile --start='XHC' --day=29 --file msg.txt --verbose
   Final rotor positions: YXY
   Rotor rotation counts: [1, 16, 412]
   Output:
   TOSCKAVFTVPONPBJZQPZFBFJXNMCLCZEVDHNEGNPGBWTYTRXJUVOKWBCBFVXIMURRDWNQTHEWTBHMPLKLPLVSJLNLNUOZDCSWAOYQTVFCNLERRWGJPOZMCIMVNVZBYQCVOQEXXFBJKFEEVKTLYNUMRBNHEQMIZXESQBFFSTNXWGMGIHDCAWFDBQRQRJCMOVDVQEEZGIFNPMGAGDVBIIYMZJYDVPIUOFHXSHTZBKCEOZABDPBOMXDZJUNIIMBCLTGZLQCTHAGUNBWMQUNYRJVEIOIHIQWCVJWPXBMVWHMSALPBPTENSLASKQUTJTCDYSCVJSXFANCCRGWAZVKJJOXXJOESZLRQKUEKZNYJNZMYQSAZVNPFRWFFZIWXSNZGNMWMACVOFSAGRJZCLDZEFATXNLVBBUA

