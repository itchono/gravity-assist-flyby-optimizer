from jplephem.spk import SPK

# Load the DE440 ephemeris file.
# This is a binary file that contains the positions of the planets and
# other solar system bodies.

de440 = SPK.open('de440.bsp')
