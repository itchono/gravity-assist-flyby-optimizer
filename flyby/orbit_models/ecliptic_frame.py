import numpy as np
from scipy.spatial.transform import Rotation as R


def obliquity_of_ecliptic(jd: np.ndarray) -> np.ndarray:
    '''
    Returns the obliquity of the ecliptic at the given Julian date.
    '''
    # See https://en.wikipedia.org/wiki/Obliquity_of_the_ecliptic
    T = (jd - 2451545) / 36525

    e = 23.43929111 - 46.8150*T/3600 - 0.00059*T**2/3600 + 0.001813*T**3/3600

    return np.radians(e)


def ecliptic_from_J2000(jd: np.ndarray) -> np.ndarray:
    '''
    Returns a rotation describing the following directions in the ecliptic
    frame at the given Julian date:
    - x: the direction of the vernal equinox (prograde)
    - y: the direction of the cross product of the x and z vectors (normal up)
    - z: the direction of the cross product of the y and x vectors (radial out)

    This rotation is used to map impulses from the ICRS frame to the ecliptic frame.

    Parameters
    ----------
    jd : float
        The Julian date at which to compute the rotation.
    '''
    e = obliquity_of_ecliptic(jd)

    return R.from_euler('x', -e, degrees=False).as_matrix()
