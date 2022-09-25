import os
from flyby.solar_system_model.jpl_ephemeris import de440
from pytest import approx


def test_ephemeris_download():
    assert os.path.exists("de440.bsp")


def test_earth_ephem():
    position, velocity = de440[0, 4].compute_and_differentiate(2457061.5)
    assert velocity == approx([-363896.059, 2019662.996,  936169.773])
