from flyby.orbit_models.keplerian_orbit import KeplerianOrbit
from flyby.solar_system_model.celestial_body import CelestialBody
from flyby.solar_system_model.read_jpl_ephemeris import de440


def test_earth_orbit():
    earth = CelestialBody.earth()
    sun = CelestialBody.sun()
    r, v = de440[0, earth.ephemeris_id].compute_and_differentiate(2451545.0)
    # IMPORTANT: velocity is given in km/d, so convert to m/s
    orbit = KeplerianOrbit.from_state(r*1e3, v*1e3/86400, sun.mu)
    print(v*1e3/86400)
    print(orbit)

    orbit.plot()
