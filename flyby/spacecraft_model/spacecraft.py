import numpy as np
from flyby.solar_system_model.jpl_ephemeris import de440
from scipy.spatial.transform import Rotation as R
from flyby.solar_system_model.celestial_body import CelestialBody
from flyby.spacecraft_model.gravity import gravity
from flyby.time_model.julian_day import jd_to_datetime64


class Spacecraft:
    def __init__(self, u: np.ndarray, jd_0: float):
        '''
        :param u: The state of the spacecraft in the ICRS frame.
            -> [x, y, z, vx, vy, vz] in [m, m, m, m/s, m/s, m/s]
        :param jd_0: The Julian date at which the spacecraft is at the given state.

        u is a 6x1 vector expressing spacecraft position and velocity relative
        to the solar system barycenter in units of [m, m, m, m/s, m/s, m/s].

        The frame is aligned with J2000.
        '''
        self.initial_state_icrs: np.ndarray = u
        self.jd_0: float = jd_0
        self.mass: float = 1

        self.interacting_bodies: "list[CelestialBody]" = []

    @property
    def interacting_bodies_dict(self):
        return {body.name: body for body in self.interacting_bodies}

    def state_planet(self, body: CelestialBody, jd: float):
        '''
        Returns the state of the spacecraft relative to the planet with the
        given ephemeris ID at the given Julian date.
        '''
        r = body.get_position(jd)
        v = body.get_velocity(jd)

        return self.state_icrs - np.concatenate((r, v))

    def add_interacting_bodies(self, *bodies: "list[CelestialBody]"):
        '''
        Adds the given bodies to the list of bodies that the spacecraft
        interacts with.
        '''
        self.interacting_bodies.extend(bodies)

    def orbital_frame_rel_planet(self, body: CelestialBody, jd: float, u: np.ndarray) -> R:
        '''
        Returns a rotation describing the following directions in the orbital
        frame of the planet with the given ephemeris ID at the given Julian
        date:
        - x: the direction of the velocity vector (prograde)
        - y: the direction of the cross product of the position and velocity (normal up)
        - z: the direction of the cross product of the x and y vectors (radial out)

        This rotation is used to map impulses from the orbital frame to the ICRS frame.

        Parameters
        ----------
        ephemeris_id : int
            The ephemeris ID of the planet.
        jd : float
            The Julian date at which to compute the rotation.
        u : np.ndarray
            The state of the spacecraft in the ICRS frame.
        '''
        r = body.get_position(jd)
        v = body.get_velocity(jd)

        r_rel = u[:3] - r
        v_rel = u[3:] - v

        # Compute the orbital frame
        x = v_rel / np.linalg.norm(v_rel)
        y = np.cross(r_rel, v_rel) / np.linalg.norm(np.cross(r_rel, v_rel))
        z = np.cross(x, y)

        # Convert to a rotation
        return np.array([x, y, z]).T

    @classmethod
    def from_planet(cls, u: np.ndarray, ephemeris_id: int, jd: float):
        '''
        Initialize a spacecraft given a state vector around a planet.

        u is a 6x1 vector expressing spacecraft position and velocity relative
        to the center of the planet in units of [m, m, m, m/s, m/s, m/s].

        The frame is aligned with J2000.
        '''
        r, v = de440[0, ephemeris_id].compute_and_differentiate(jd)
        # note: jplephem gives r in km and v in km/day

        return cls(u + np.concatenate((r*1e3, v*1e3/86400)), jd)

    # dynamics
    def get_rates(self, t: float, u: np.ndarray) -> np.ndarray:
        '''
        Returns the time derivative of the state vector at the given time.

        Used for scipy.solve_ivp.

        Parameters
        ----------
        t: float
            time in seconds
        u: np.ndarray
            state vector in ICRS frame
        '''

        force = np.zeros(3)
        t_jd = self.jd_0 + t/86400

        for body in self.interacting_bodies:
            force += gravity(u, t_jd, body) * self.mass

        return np.concatenate((u[3:], force / self.mass))
