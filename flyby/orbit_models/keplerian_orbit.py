import numpy as np
import matplotlib.pyplot as plt


class KeplerianOrbit:
    def __init__(self, a, e, i, raan, arg_perigee) -> None:
        self.a = a
        self.e = e
        self.i = i
        self.raan = raan
        self.arg_perigee = arg_perigee

    def __str__(self) -> str:
        return f'KeplerianOrbit(a={self.a}, e={self.e}, i={self.i}, raan={self.raan}, arg_perigee={self.arg_perigee})'

    def get_state_space_point(self, nu: float) -> np.ndarray:
        '''
        Return a point in state space corresponding to a certain true anomaly.

        Parameters
        ----------
        nu: float
            True anomaly in radians

        Returns
        -------
        np.ndarray
            A 3x1 array of the position in state space.
        '''
        e = self.e
        a = self.a
        i = self.i
        raan = self.raan
        arg_perigee = self.arg_perigee

        # Calculate the radius
        r = a*(1-e**2)/(1+e*np.cos(nu))

        # Calculate the position in the perifocal frame
        rp = r*np.vstack((np.cos(nu), np.sin(nu), np.zeros(len(nu))))

        # Transform to inertial frame
        C = np.array([
            [np.cos(raan)*np.cos(arg_perigee)-np.sin(raan)*np.sin(arg_perigee)*np.cos(i), -np.cos(raan)
             * np.sin(arg_perigee)-np.sin(raan)*np.cos(arg_perigee)*np.cos(i), np.sin(raan)*np.sin(i)],
            [np.sin(raan)*np.cos(arg_perigee)+np.cos(raan)*np.sin(arg_perigee)*np.cos(i), -np.sin(raan)
             * np.sin(arg_perigee)+np.cos(raan)*np.cos(arg_perigee)*np.cos(i), -np.cos(raan)*np.sin(i)],
            [np.sin(arg_perigee)*np.sin(i),
             np.cos(arg_perigee)*np.sin(i), np.cos(i)]
        ])

        return C @ rp

    def get_state_space_velocity(self, nu: float, mu: float) -> np.ndarray:
        '''
        Return a velocity in state space corresponding to a certain true anomaly.

        Parameters
        ----------
        nu: float
            True anomaly in radians
        mu: float
            Gravitational parameter of the central body in m^3/s^2

        Returns
        -------
        np.ndarray
            A 3x1 array of the velocity in state space.
        '''
        e = self.e
        a = self.a
        i = self.i
        raan = self.raan
        arg_perigee = self.arg_perigee

        # Calculate the magnitude of the velocity
        v_partial = np.sqrt(mu/(a*(1 - e**2)))

        # Calculate the velocity in the perifocal frame
        vp = v_partial * \
            np.vstack((-np.sin(nu), e+np.cos(nu), np.zeros(len(nu))))

        # Transform to inertial frame
        C = np.array([
            [np.cos(raan)*np.cos(arg_perigee)-np.sin(raan)*np.sin(arg_perigee)*np.cos(i), -np.cos(raan)
             * np.sin(arg_perigee)-np.sin(raan)*np.cos(arg_perigee)*np.cos(i), np.sin(raan)*np.sin(i)],
            [np.sin(raan)*np.cos(arg_perigee)+np.cos(raan)*np.sin(arg_perigee)*np.cos(i), -np.sin(raan)
             * np.sin(arg_perigee)+np.cos(raan)*np.cos(arg_perigee)*np.cos(i), -np.cos(raan)*np.sin(i)],
            [np.sin(arg_perigee)*np.sin(i),
             np.cos(arg_perigee)*np.sin(i), np.cos(i)]
        ])

        return C @ vp

    def get_state_space_orbit(self, n: float) -> np.ndarray:
        """
        Returns a set of positions in state space for the orbit.

        Parameters
        ----------
        n : int
            The number of points to return.

        Returns
        -------
        np.ndarray
            A 3xN array of positions in state space.

        """
        return self.get_state_space_point(np.linspace(0, 2*np.pi, n))

    def plot(self):
        state_space_orbit = self.get_state_space_orbit(1000)

        fig = plt.figure(figsize=(10, 4))
        # 3 views from xy, xz, and yz planes

        ax_xy = fig.add_subplot(131)
        ax_xz = fig.add_subplot(132)
        ax_yz = fig.add_subplot(133)

        print(state_space_orbit.shape)

        ax_xy.plot(
            state_space_orbit[0, :], state_space_orbit[1, :])
        ax_xz.plot(
            state_space_orbit[0, :], state_space_orbit[2, :])
        ax_yz.plot(state_space_orbit[1, :], state_space_orbit[2, :])

        ax_xy.set_xlabel('x')
        ax_xy.set_ylabel('y')
        ax_xy.set_title('xy plane')
        ax_xy.set_aspect('equal')

        ax_xz.set_xlabel('x')
        ax_xz.set_ylabel('z')
        ax_xz.set_title('xz plane')
        ax_xz.set_aspect('equal')

        ax_yz.set_xlabel('y')
        ax_yz.set_ylabel('z')
        ax_yz.set_title('yz plane')
        ax_yz.set_aspect('equal')

        plt.tight_layout()
        plt.show()

    @classmethod
    def from_state(cls, r: np.ndarray, v: np.ndarray, mu: float):
        '''
        Fits the osculating Keplerian orbit to the given state.

        Parameters
        ----------
        r: np.ndarray
            Position vector in meters expressed in J2000 about the central body.
        v: np.ndarray
            Velocity vector in meters per second expressed in J2000 about the central body.
        mu: float
            gravitational parameter of the central body in meters cubed per second squared.
        '''
        h = np.cross(r, v)  # angular momentum vector
        n = np.cross(np.array([0, 0, 1]), h)  # node vector

        e_vec = (1/mu)*((np.linalg.norm(v)**2 - mu/np.linalg.norm(r))
                        * r - (r @ v)*v)  # eccentricity vector

        e = np.linalg.norm(e_vec)  # eccentricity
        # energy (specific mechanical energy)
        energy = (np.linalg.norm(v)**2)/2 - mu/np.linalg.norm(r)

        a = -mu/(2*energy)  # semi-major axis

        i = np.arccos(h[2]/np.linalg.norm(h))  # inclination
        # right ascension of the ascending node
        raan = np.arccos(n[0]/np.linalg.norm(n))
        # argument of perigee
        arg_perigee = np.arccos(
            (n @ e_vec)/(np.linalg.norm(n)*np.linalg.norm(e_vec)))

        return cls(a, np.linalg.norm(e), i, raan, arg_perigee)
