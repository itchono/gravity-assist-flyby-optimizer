import numpy as np

from flyby.solar_system_model.celestial_body import CelestialBody
from flyby.solar_system_model.jpl_ephemeris import de440


def gravity(icrs_state: np.ndarray, t_jd: float, body: CelestialBody):
    '''
    Get acceleration on spacecraft due to gravity from all bodies in the solar system.

    Parameters
    ----------
    icrs_state : np.ndarray
        The state of the spacecraft [x y z vx vy vx] in the ICRS frame,
        given in units of [m, m, m, m/s, m/s, m/s].
    t_jd : float
        The Julian date at which to compute the acceleration.
    body : CelestialBody
        The body to compute the acceleration from.
    '''
    r_body = body.get_position(t_jd)

    r_rel = icrs_state[:3] - r_body

    return -body.mu * r_rel / np.linalg.norm(r_rel)**3
