import os
import urllib.request

DE440_URL = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440.bsp"

def assure_ephemeris():
    """Download the DE440 ephemeris file if it is not already present."""
    filename = "de440.bsp"
    if not os.path.exists(filename):
        print("Downloading DE440 ephemeris file (114 MB)...")
        urllib.request.urlretrieve(DE440_URL, filename)
        print("Done.")