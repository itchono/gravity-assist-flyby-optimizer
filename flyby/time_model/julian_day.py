import numpy as np


def datetime64_to_jd(dt64: np.datetime64) -> float:
    """Convert a numpy.datetime64 to a Julian date."""
    # 1970-01-01T00:00:00Z is jd 2440587.5
    return dt64.astype("datetime64[us]").astype(float)/(1e6 * 86400) + 2440587.5


def jd_to_datetime64(jd: float) -> np.datetime64:
    """Convert a Julian date to a numpy.datetime64."""
    # Expand jd value to microseconds for a 64 bit time range of 584.5 million years
    return np.timedelta64(round((jd - 2440587.5) * 86400 * 1e6), "us").astype("datetime64[us]")
