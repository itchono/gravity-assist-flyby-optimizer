from matplotlib import pyplot as plt
import numpy as np
from flyby.solar_system_model.celestial_body import CelestialBody
from flyby.solar_system_model.jpl_ephemeris import de440
from flyby.orbit_models.keplerian_orbit import KeplerianOrbit
from flyby.orbit_models.ecliptic_frame import ecliptic_from_J2000
from flyby.time_model.julian_day import datetime64_to_jd
from flyby.solar_system_model.relational_tree import RelationalTree


def plot_body(body: CelestialBody, jd: float, ax: plt.Axes, mu: float,
              plot_orbit: bool = True, frame: str = "ecliptic") -> None:
    '''
    Plots a celestial body on a matplotlib axes object.

    Plot is in the barycentric ecliptic frame.

    Parameters
    ----------
    body: CelestialBody
        The body to plot.
    jd: float
        The Julian date at which to plot the body.
    ax: plt.Axes
        The axes on which to plot the body.
    mu: float
        The gravitational parameter of the central body.
    plot_orbit: bool
        Whether to plot the orbit of the body.
    frame: str
        The frame in which to plot the body.
        [ecliptic, J2000]
    '''
    r, v = de440[0, body.ephemeris_id].compute_and_differentiate(jd)

    if frame == "ecliptic":
        C = ecliptic_from_J2000(jd)
    elif frame == "J2000":
        C = np.eye(3)

    r = C @ r * 1e3
    v = C @ v * 1e3

    orbit = KeplerianOrbit.from_state(
        r, v/86400, mu)

    orbit_r = orbit.get_state_space_orbit(1000)

    if plot_orbit:
        ax.plot(orbit_r[0], orbit_r[1], color=f"#{body.color:X}")
    ax.plot(r[0], r[1], 'o', markersize=5,
            color=f"#{body.color:X}", label=body.name)


def full_solar_system_plot(ax: plt.Axes, time: np.datetime64 = np.datetime64("now")):
    '''
    Generates a plot of the solar system at the specified time,
    defaulting to the current time if unspecified.

    Parameters
    ----------
    ax: plt.Axes
        The axes on which to plot the solar system.
    time: np.datetime64
        The time at which to generate the plot.
    '''
    jd = datetime64_to_jd(time)
    solar_system = RelationalTree.solar_system()

    # Plot the Sun
    r_sun = de440[0, 10].compute(jd) * 1e3
    ax.plot(r_sun[0], r_sun[1], 'o', markersize=5,
            color=f"#{solar_system.root.color:X}")

    # Plot the planets
    for i in range(8):
        plot_body(solar_system.root.children[i],
                  jd, ax, solar_system.root.mu)

    ax.set_title(
        f'Solar System at {time}\nBarycentric Ecliptic Frame', wrap=True)
    ax.set_axis_off()
    ax.set_aspect('equal')
    ax.legend()


def inner_solar_system_plot(ax: plt.Axes, time: np.datetime64 = np.datetime64("now")):
    '''
    Generates a plot of the inner (4 planets) solar system at the specified time,
    defaulting to the current time if unspecified.

    Parameters
    ----------
    ax: plt.Axes
        The axes on which to plot the solar system.
    time: np.datetime64
        The time at which to generate the plot.
    '''

    jd = datetime64_to_jd(time)
    solar_system = RelationalTree.solar_system()

    # Plot the Sun
    r_sun = de440[0, 10].compute(jd)
    ax.plot(r_sun[0], r_sun[1], 'o', markersize=5,
            color=f"#{solar_system.root.color:X}")

    # Plot the planets
    for i in range(4):
        plot_body(solar_system.root.children[i],
                  jd, ax, solar_system.root.mu)

    ax.set_title(
        f'Inner Solar System at {time}\nBarycentric Ecliptic Frame', wrap=True)
    ax.set_axis_off()
    ax.set_aspect('equal')
    ax.legend()


def zoom_axes_to_body(ax: plt.Axes, body: CelestialBody, jd: float, zoom: float = 10,
                      ecliptic: bool = True) -> None:
    '''
    Zooms the axes to a body.

    Parameters
    ----------
    ax: plt.Axes
        The axes to zoom.
    body: CelestialBody
        The body to zoom to.
    jd: float
        The Julian date at which to zoom.
    zoom: float
        The zoom factor in terms of body diameters.
    ecliptic: bool
        Whether to plot in the ecliptic frame.
    '''
    r = de440[0, body.ephemeris_id].compute(jd) * 1e3

    r = ecliptic_from_J2000(jd) @ r if ecliptic else r

    diameter = 2 * body.radius

    ax.set_xlim(r[0] - zoom * diameter, r[0] + zoom * diameter)
    ax.set_ylim(r[1] - zoom * diameter, r[1] + zoom * diameter)


if __name__ == "__main__":
    plt.style.use('dark_background')  # dark mode
    plt.figure(figsize=(12, 7))
    plt.subplot(121)
    full_solar_system_plot(plt.gca())
    plt.subplot(122)
    inner_solar_system_plot(plt.gca())

    plt.show()
