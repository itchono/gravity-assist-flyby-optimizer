from scipy.integrate import solve_ivp
import numpy as np

from flyby.orbit_models.keplerian_orbit import KeplerianOrbit
from flyby.solar_system_model.celestial_body import CelestialBody
from flyby.spacecraft_model.spacecraft import Spacecraft
from flyby.time_model.julian_day import datetime64_to_jd


def generate_initial_conditions(orbit: KeplerianOrbit, body: CelestialBody,
                                initial_time: np.datetime64,
                                initial_true_anomaly: np.ndarray = np.array([0])) -> Spacecraft:

    initial_jd = datetime64_to_jd(initial_time)

    planet_position = orbit.get_state_space_point(initial_true_anomaly)
    planet_velocity = orbit.get_state_space_velocity(
        initial_true_anomaly, body.mu)

    planet_state = np.concatenate(
        (planet_position, planet_velocity)).reshape((6,))
    return Spacecraft.from_planet(planet_state, body.ephemeris_id, initial_jd)


def simulate(spacecraft: Spacecraft, end_time: np.datetime64):
    end_jd = datetime64_to_jd(end_time)

    sol = solve_ivp(spacecraft.get_rates, (spacecraft.jd_0, end_jd),
                    spacecraft.initial_state_icrs, method='DOP853', rtol=1e-10, atol=1e-10)

    return sol


if __name__ == "__main__":
    # Initialize a spacecraft orbiting the Earth

    initial_orbit = KeplerianOrbit(7000e3, 0.01, 0, 0, 0)
    parent_body = CelestialBody.earth()

    spacecraft = generate_initial_conditions(
        initial_orbit, parent_body, np.datetime64('now'))

    solution = simulate(spacecraft, np.datetime64(
        'now') + np.timedelta64(1, 'D'))

    print(solution.y)
