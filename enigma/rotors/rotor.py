# Copyright (C) 2012 by Brian Neal.
# This file is part of Py-Enigma, the Enigma Machine simulation.
# Py-Enigma is released under the MIT License (see License.txt).

"""rotor.py - this module contains the Rotor class for the Enigma simulation."""

import string
import collections

from . import RotorError


ALPHA_LABELS = string.ascii_uppercase

# In specifying a wiring for a rotor, every letter must be included exactly
# once. This variable helps us enforce that:
WIRING_FREQ_SET = set((letter, 1) for letter in ALPHA_LABELS)


class Rotor:
    """The Rotor class represents the Enigma Machine rotors (Walzen).
    
    A rotor has 26 circularly arranged pins on the right (entry) side and 26
    contacts on the left side. Each pin is connected to a single contact by
    internal wiring, thus establishing a substitution cipher. We represent this
    wiring by establishing a mapping from a pin to a contact (and vice versa for
    the return path). Internally we number the pins and contacts from 0-25 in a
    clockwise manner with 0 being the "top".

    An alphabetic or numeric ring is fastened to the rotor by the operator. The
    labels of this ring are displayed to the operator through a small window on
    the top panel. The ring can be fixed to the rotor in one of 26 different
    positions; this is called the ring setting (Ringstellung). We will number
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

    Note that due to the system of ratchets and pawls, the middle rotor (in a 3
    rotor Enigma) can "double-step". The middle rotor will advance on the next
    step of the first rotor a second time in a row, if the middle rotor is in
    its own turnover position.

    Note that we allow the stepping parameter to be None. This indicates the
    rotor does not rotate. This allows us to model the entry wheel and
    reflectors as stationary rotors.
    
    """

    def __init__(self, model_name, wiring, ring_setting=0, stepping=None):
        """Establish rotor characteristics:

        model_name - e.g. "I", "II", "III", "Beta", "Gamma"

        wiring - this should be a string of 26 alphabetic characters that
        represents the internal wiring transformation of the signal as it enters
        from the right side. This is the format used in various online
        resources. For example, for the Wehrmacht Enigma type I rotor the
        mapping is "EKMFLGDQVZNTOWYHXUSPAIBRCJ".

        ring_setting - this should be an integer from 0-25, inclusive, which
        indicates the Ringstellung. A value of 0 means there is no offset; e.g.
        the letter "A" is fixed to pin 0. A value of 1 means "B" is mapped to
        pin 0.

        stepping - this is the stepping or turnover parameter. It should be an
        iterable, for example a string such as "Q". This will indicate that when
        the rotor transitions from "Q" to "R" (by observing the operator
        window), the rotor will "kick" the rotor to its left, causing it to
        rotate. If the rotor has more than one notch, a string of length 2 could
        be used, e.g. "ZM".  Another way to think of this parameter is that when
        a character in the stepping string is visible in the operator window, a
        notch is lined up with the pawl on the left side of the rotor.  This
        will allow the pawl to push up on the rotor *and* the rotor to the left
        when the next key is depressed.

        Note that for purposes of simulation, our rotors will always use
        alphabetic labels A-Z. In reality, the Heer & Luftwaffe devices used
        numbers 01-26, and Kriegsmarine devices used A-Z. Our usage of A-Z is
        simply for simulation convenience. In the future we may allow either
        display.

        """
        self.name = model_name
        self.wiring_str = wiring.upper()
        self.ring_setting = ring_setting
        self.pos = 0
        self.rotations = 0

        # check wiring length
        if len(self.wiring_str) != 26:
            raise RotorError("invalid wiring length")

        # check wiring format; must contain A-Z
        for c in self.wiring_str:
            if c not in ALPHA_LABELS:
                raise RotorError("invalid wiring: %s" % wiring)

        # check wiring format; ensure every letter appears exactly once
        input_set = set(collections.Counter(self.wiring_str).items())
        if input_set != WIRING_FREQ_SET:
            raise RotorError("invalid wiring frequency")

        if not isinstance(ring_setting, int) or not (0 <= ring_setting < 26):
            raise RotorError("invalid ring_setting")

        # Create two lists to describe the internal wiring. Two lists are used
        # to do fast lookup from both entry (from the right) and exit (from the
        # left). 
        self.entry_map = [ord(pin) - ord('A') for pin in self.wiring_str]
        
        self.exit_map = [0] * 26
        for i, v in enumerate(self.entry_map):
            self.exit_map[v] = i

        # build a map of display values to positions
        self.display_map = {}
        for n in range(26):
            self.display_map[chr(ord('A') + n)] = (n - self.ring_setting) % 26

        # build a reverse map of position mapped to display values
        self.pos_map = {v : k for k, v in self.display_map.items()}

        # build step set; this is a set of positions where our notches are in
        # place to allow the pawls to move
        self.step_set = set()
        if stepping is not None:
            for pos in stepping:
                if pos in self.display_map:
                    self.step_set.add(pos)
                else:
                    raise RotorError("stepping: %s" % pos)

        # initialize our position and display value:
        self.set_display('A')

    def set_display(self, val):
        """Spin the rotor such that the string val appears in the operator
        window.

        This sets the internal position of the rotor on the axle and thus
        rotates the pins and contacts accordingly.

        A value of 'A' for example puts the rotor in position 0, assuming an
        internal ring setting of 0.

        The parameter val must be a string in 'A' - 'Z'.

        Setting the display resets the internal rotation counter to 0.

        """
        s = val.upper()
        if s not in self.display_map:
            raise RotorError("bad display value %s" % val)

        self.pos = self.display_map[s]
        self.display_val = s
        self.rotations = 0

    def get_display(self):
        """Returns what is currently being displayed in the operator window."""
        return self.display_val

    def signal_in(self, n):
        """Simulate a signal entering the rotor from the right at a given pin
        position n.

        n must be an integer between 0 and 25.

        Returns the contact number of the output signal (0-25).

        """
        # determine what pin we have at that position due to rotation
        pin = (n + self.pos) % 26

        # run it through the internal wiring
        contact = self.entry_map[pin]

        # turn back into a position due to rotation
        return (contact - self.pos) % 26

    def signal_out(self, n):
        """Simulate a signal entering the rotor from the left at a given
        contact position n.

        n must be an integer between 0 and 25.

        Returns the pin number of the output signal (0-25).

        """
        # determine what contact we have at that position due to rotation
        contact = (n + self.pos) % 26

        # run it through the internal wiring
        pin = self.exit_map[contact]

        # turn back into a position due to rotation
        return (pin - self.pos) % 26

    def notch_over_pawl(self):
        """Return True if this rotor has a notch in the stepping position and
        False otherwise.

        """
        return self.display_val in self.step_set

    def rotate(self):
        """Rotate the rotor forward due to mechanical stepping action."""

        self.pos = (self.pos + 1) % 26
        self.display_val = self.pos_map[self.pos]
        self.rotations += 1
