import os
from flyby.solar_system_model.assure_ephermeris import assure_ephemeris

def test_ephemeris_download():
    assure_ephemeris()
    assert os.path.exists("de440.bsp")