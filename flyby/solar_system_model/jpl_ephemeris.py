import os
import urllib.request
from jplephem.spk import SPK

DE440_URL = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440.bsp"

# Download the DE440 ephemeris file if it is not already present
filename = "de440.bsp"
if not os.path.exists(filename):
    print("Downloading DE440 ephemeris file (114 MB)...")
    urllib.request.urlretrieve(DE440_URL, filename)
    print("Done.")

# Load the DE440 ephemeris file.
# This is a binary file that contains the positions of the planets and
# other solar system bodies.

de440 = SPK.open('de440.bsp')
