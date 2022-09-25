from matplotlib import pyplot as plt
import numpy as np
from flyby.solar_system_model.celestial_body import CelestialBody
from flyby.solar_system_model.jpl_ephemeris import de440
from flyby.orbit_models.keplerian_orbit import KeplerianOrbit
from flyby.time_model.julian_day import datetime64_to_jd
from flyby.solar_system_model.relational_tree import RelationalTree

# Get current system time as datetime64
current_time = np.datetime64('now')

jd = datetime64_to_jd(current_time)

solar_system = RelationalTree.solar_system()

plt.style.use('dark_background')

# Plot the Sun
plt.plot(0, 0, 'yo', markersize=5)

# Plot the planets
for i in range(8):
    planet: CelestialBody = solar_system.root.children[i]
    r, v = de440[0, planet.ephemeris_id].compute_and_differentiate(jd)

    orbit = KeplerianOrbit.from_state(
        r*1e3, v*1e3/86400, solar_system.root.mu)

    orbit_r = orbit.get_state_space_orbit(200) / 1e3

    plt.plot(orbit_r[0], orbit_r[1], color=f"#{planet.color:X}")
    plt.plot(r[0], r[1], 'o', markersize=5,
             color=f"#{planet.color:X}", label=planet.name)

plt.title(f'The Solar System at {current_time}')
plt.axis("equal")
plt.axis("off")
plt.legend()
plt.show()
