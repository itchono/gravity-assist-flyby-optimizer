from scipy.constants import G
from flyby.math_utilities.fast_linear_interpolator import FastLerp
from flyby.solar_system_model.jpl_ephemeris import de440
import numpy as np


class CelestialBody:
    def __init__(self, name: str, radius: float,
                 mass: float, color: int, ephemeris_id: int = None) -> None:
        '''
        :param name: Name of the celestial body
        :param radius: Radius of the celestial body in meters
        :param mass: Mass of the celestial body in kilograms
        :param color: Color of the celestial body as a hex value
        :param ephemeris_id: ID of the celestial body in the JPL ephemeris file, if applicable
        '''
        self.name: str = name
        self.radius: float = radius
        self.mass: float = mass
        self.color: int = color

        self.ephemeris_id: int = ephemeris_id
        self.position_interpolant: FastLerp = None
        self.velocity_interpolant: FastLerp = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"CelestialBody({self.name}, {self.radius}, {self.mass}, {self.color}, {self.ephemeris_id})"

    def construct_interpolant(self, start_time: float, end_time: float):
        '''
        Constructs a scipy.interpolate.interp1d object that interpolates the position and velocity of
        the body at any time between start_time and end_time

        Parameters
        ----------
        start_time : float
            The start time of the interpolation in Julian days
        end_time : float
            The end time of the interpolation in Julian days
        n : int, optional
            The number of points to use in the interpolation, by default 1000
        '''
        n = int(end_time - start_time) * 10  # 10 steps per day

        t_jd = np.linspace(start_time, end_time, n)

        position_arr, velocity_arr = de440[0, self.ephemeris_id].compute_and_differentiate(
            t_jd)

        self.position_interpolant = FastLerp(
            t_jd, position_arr * 1e3)
        self.velocity_interpolant = FastLerp(
            t_jd, velocity_arr * 1e3 / 86400)

    def get_position(self, time: float) -> np.ndarray:
        '''
        Returns the position of the body at the specified time in m [ICRS]

        Parameters
        ----------
        time : float
            The time at which to get the position of the body in Julian days

        Returns
        -------
        np.ndarray
            The position of the body at the specified time in the ICRS frame
        '''
        if self.position_interpolant is None:
            raise Exception(
                "Interpolant has not been constructed for this body")
        return self.position_interpolant(time)

    def get_velocity(self, time: float) -> np.ndarray:
        '''
        Returns the velocity of the body at the specified time in m/s [ICRS]

        Parameters
        ----------
        time : float
            The time at which to get the velocity of the body in Julian days

        Returns
        -------
        np.ndarray
            The velocity of the body at the specified time in the ICRS frame
        '''
        if self.velocity_interpolant is None:
            raise Exception(
                "Interpolant has not been constructed for this body")
        return self.velocity_interpolant(time)

    @property
    def mu(self) -> float:
        return self.mass * G

    # Real-World Presets
    @classmethod
    def sun(cls):
        return cls("Sun", 695700000, 1.989e30, 0xffff22, 10)

    @classmethod
    def earth(cls):
        return cls("Earth", 6371000, 5.972e24, 0x3E93C3, 3)

    @classmethod
    def moon(cls):
        return cls("Moon", 1737000, 7.34767309e22, 0xCCCCCC)

    @classmethod
    def mercury(cls):
        return cls("Mercury", 2439700, 3.285e23, 0x999999, 1)

    @classmethod
    def venus(cls):
        return cls("Venus", 6051800, 4.867e24, 0xffe6b3, 2)

    @classmethod
    def mars(cls):
        return cls("Mars", 3389500, 6.39e23, 0x993d00, 4)

    @classmethod
    def jupiter(cls):
        return cls("Jupiter", 69911000, 1.898e27, 0xF5A52E, 5)

    @classmethod
    def saturn(cls):
        return cls("Saturn", 58232000, 5.683e26, 0xEEC554, 6)

    @classmethod
    def uranus(cls):
        return cls("Uranus", 25362000, 8.681e25, 0xcceeff, 7)

    @classmethod
    def neptune(cls):
        return cls("Neptune", 24622000, 1.024e26, 0x0066ff, 8)

    # KSP Presets
    @classmethod
    def kerbin(cls):
        return cls("Kerbin", 600000, 5.2915793e22, 0x3E93C3)
