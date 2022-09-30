from matplotlib import pyplot as plt
import numpy as np

from flyby.orbit_models.ecliptic_frame import ecliptic_from_J2000
import numpy as np
from flyby.solar_system_model.celestial_body import CelestialBody
from flyby.solar_system_model.jpl_ephemeris import de440


def plot_trajectory_about_body(body: CelestialBody, position: np.ndarray, jd: np.ndarray, ax: plt.Axes):
    '''
    Plot a trajectory in the J2000 frame about a body.

    Parameters
    ----------
    body : CelestialBody
        The body to plot the trajectory about.
    position : np.ndarray
        The position of the spacecraft in the ICRS frame, given in units of [m, m, m].
    jd : np.ndarray
        The Julian date at which the spacecraft is in the given position.
    ax : plt.Axes
        The axes to plot the trajectory on.
    '''
    r_body = de440[0, body.ephemeris_id].compute(jd) * 1e3
    r_rel = position - r_body

    ax.plot(r_rel[0], r_rel[1], r_rel[2])


def plot_trajectory(r: np.ndarray, ax: plt.Axes, jd: np.ndarray = None,
                    color: str = "orange",
                    convert_to_ecliptic: bool = True,
                    rel_body: CelestialBody = None) -> None:
    '''
    Plots a trajectory on a matplotlib axes object.

    Parameters
    ----------
    r : np.ndarray
        The trajectory to plot, given in units of [m, m, m].
        Given in ICRS J2000 frame.
    ax : plt.Axes
        The axes to plot the trajectory on.
    jd : np.ndarray
        The Julian date at which the spacecraft is in the given position.
    color : str, optional
        The color to plot the trajectory in, by default "black"   
    convert_to_ecliptic : bool, optional
        Whether to convert the trajectory to the ecliptic frame, by default True
    rel_body : CelestialBody, optional
        The body to plot the trajectory about, by default None
    '''
    if rel_body is not None:
        r_body = de440[0, rel_body.ephemeris_id].compute(jd) * 1e3
        r = r - r_body + (r_body[:, 0])[:, np.newaxis]

    if convert_to_ecliptic and jd is not None:
        C = ecliptic_from_J2000(jd[0])
        r = C @ r
    elif convert_to_ecliptic and jd is None:
        raise ValueError(
            "jd must be specified if convert_to_ecliptic is True.")

    ax.plot(r[0], r[1], color=color)


def plot_point(r: np.ndarray, ax: plt.Axes, jd: np.ndarray = None,
               color: str = "orange",
               convert_to_ecliptic: bool = True) -> None:
    '''
    Puts a marker at position r.
    '''
    if convert_to_ecliptic and jd is not None:
        C = ecliptic_from_J2000(jd[0])
        r = C @ r
    elif convert_to_ecliptic and jd is None:
        raise ValueError(
            "jd must be specified if convert_to_ecliptic is True.")

    ax.plot(r[0], r[1], "o", color=color)
