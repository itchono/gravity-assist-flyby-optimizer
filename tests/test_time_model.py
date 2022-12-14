import numpy as np
from flyby.time_model.julian_day import datetime64_to_jd, jd_to_datetime64
from pytest import approx

def test_jd_conversion_1():
    """Test conversion from datetime64 to Julian date."""
    dt64 = np.datetime64('2015-02-08T00:00:00')
    jd = datetime64_to_jd(dt64)
    assert jd == approx(2457061.5)

def test_jd_conversion_2():
    """Test conversion from Julian date to datetime64."""
    jd = 2457061.5
    dt64 = jd_to_datetime64(jd)
    assert dt64 == approx(np.datetime64('2015-02-08T00:00:00'))

def test_jd_conversion_3():
    """Test fractional date conversion."""
    dt64 = np.datetime64('2015-02-08T18:00:00')
    jd = datetime64_to_jd(dt64)
    assert jd == approx(2457061.25)