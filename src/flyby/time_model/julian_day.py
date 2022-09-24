import numpy as np

def datetime64_to_jd(dt64: np.datetime64) -> float:
    """Convert a numpy.datetime64 to a Julian date."""
    # 1970-01-01T00:00:00Z is jd 2440587.5
    return dt64.astype("datetime64[D]").astype(float) + 2440587.5

def jd_to_datetime64(jd: float) -> np.datetime64:
    """Convert a Julian date to a numpy.datetime64."""
    epoch = np.datetime64("1970-01-01T00:00:00Z")
    return epoch + np.timedelta64((jd - 2440587.5), "D")