from jplephem import Ephemeris

# Load the DE440 ephemeris file.
# This is a binary file that contains the positions of the planets and
# other solar system bodies.

eph = Ephemeris.open("de440.bsp")

