from scipy.integrate import solve_ivp
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm

import cProfile

from flyby.orbit_models.keplerian_orbit import KeplerianOrbit
from flyby.solar_system_model.celestial_body import CelestialBody
from flyby.solar_system_model.relational_tree import RelationalTree
from flyby.spacecraft_model.spacecraft import Spacecraft
from flyby.time_model.julian_day import datetime64_to_jd, jd_to_datetime64
from flyby.visualizers.solar_system_plot import zoom_axes_to_body, full_solar_system_plot
from flyby.visualizers.trajectory_plotter import plot_trajectory, plot_trajectory_about_body, plot_point


def generate_initial_conditions_from_keplerian(orbit: KeplerianOrbit, body: CelestialBody,
                                               initial_time: np.datetime64,
                                               initial_true_anomaly: np.ndarray = np.array([0])) -> Spacecraft:

    initial_jd = datetime64_to_jd(initial_time)

    planet_position = orbit.get_state_space_point(initial_true_anomaly)
    planet_velocity = orbit.get_state_space_velocity(
        initial_true_anomaly, body.mu)

    planet_state = np.concatenate(
        (planet_position, planet_velocity)).reshape((6,))

    spacecraft = Spacecraft.from_planet(
        planet_state, body.ephemeris_id, initial_jd)

    spacecraft.add_interacting_bodies(
        *RelationalTree.solar_system().all_bodies)

    return spacecraft


def generate_initial_conditions_from_cartesian(initial_state: np.ndarray,
                                               body: CelestialBody,
                                               initial_time: np.datetime64) -> Spacecraft:
    initial_jd = datetime64_to_jd(initial_time)

    spacecraft = Spacecraft.from_planet(
        initial_state, body.ephemeris_id, initial_jd)

    spacecraft.add_interacting_bodies(
        *RelationalTree.solar_system().all_bodies)

    return spacecraft


def simulate(spacecraft: Spacecraft, end_time: np.datetime64, show_progress=True):
    end_jd = datetime64_to_jd(end_time)

    # Build ephemeris interpolants
    for body in spacecraft.interacting_bodies:
        body.construct_interpolant(spacecraft.jd_0, end_jd)

    prograde_direction = spacecraft.orbital_frame_rel_planet(
        spacecraft.interacting_bodies_dict["Earth"], spacecraft.jd_0,
        spacecraft.initial_state_icrs).T[0]

    print(prograde_direction)

    spacecraft.initial_state_icrs[3:6] += 4000 * prograde_direction

    duration_seconds = (end_jd - spacecraft.jd_0) * 86400

    if show_progress:
        pbar = tqdm(total=int(duration_seconds), unit="sec",
                    desc=f"Propagating from JD {round(spacecraft.jd_0, 2)} to {round(end_jd, 2)}")

    def progress(t, y):
        pbar.update(int(t - pbar.n))
        return 0

    sol = solve_ivp(spacecraft.get_rates, (0, duration_seconds),
                    spacecraft.initial_state_icrs, method='DOP853', rtol=1e-8, atol=1e-8,
                    events=[progress] if show_progress else None)

    if show_progress:
        pbar.close()

    return sol


def earth_orbit_example():
    # Initialize a spacecraft orbiting the Earth

    plt.style.use('dark_background')

    initial_orbit = KeplerianOrbit(7000e3, 0.01, 0.01, 0, 0)
    parent_body = CelestialBody.earth()
    initial_time = np.datetime64('now')

    spacecraft = generate_initial_conditions_from_keplerian(
        initial_orbit, parent_body, initial_time)

    solution = simulate(spacecraft, np.datetime64(
        'now') + np.timedelta64(10, 'D'))

    jd = spacecraft.jd_0 + solution.t / 86400

    fig, ax = plt.subplots()
    full_solar_system_plot(ax, jd_to_datetime64(jd[0]))
    plot_trajectory(solution.y[:3], ax, jd)
    zoom_axes_to_body(ax, parent_body, jd=jd[0])
    plt.show()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    plot_trajectory_about_body(parent_body, solution.y[:3], jd, ax=ax)
    plt.show()


def earth_escape_example(show_progress=True):
    initial_orbit = KeplerianOrbit(7000e3, 0.01, 0, 0, 0)

    parent_body = CelestialBody.earth()
    initial_time = np.datetime64('now')
    initial_ta = np.array([-np.pi/2])

    spacecraft = generate_initial_conditions_from_keplerian(
        initial_orbit, parent_body, initial_time, initial_ta)

    solution = simulate(spacecraft, np.datetime64(
        'now') + np.timedelta64(100, 'D'), show_progress)

    jd = spacecraft.jd_0 + solution.t / 86400

    plt.style.use('dark_background')

    plt.subplot(121)
    # At departure
    full_solar_system_plot(plt.gca(), jd_to_datetime64(jd[0]))
    plot_trajectory(solution.y[:3], plt.gca(), jd, color="white")
    plot_point(solution.y[:3, 0], plt.gca(), jd, color="white")

    plt.subplot(122)
    # At arrival
    full_solar_system_plot(plt.gca(), jd_to_datetime64(jd[-1]))
    plot_trajectory(solution.y[:3], plt.gca(), jd, color="white")
    plot_point(solution.y[:3, -1], plt.gca(), jd, color="white")
    plt.show()


if __name__ == '__main__':
    # earth_orbit_example()

    # cProfile.run('earth_escape_example(False)')
    earth_escape_example()
