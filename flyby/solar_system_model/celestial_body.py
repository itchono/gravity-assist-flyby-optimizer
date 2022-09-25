from scipy.constants import G


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

    def __str__(self):
        return self.name

    @property
    def mu(self) -> float:
        return self.mass * G

    # Real-World Presets
    @classmethod
    def sun(cls):
        return cls("Sun", 695700000, 1.989e30, 0xffff66, 10)

    @classmethod
    def earth(cls):
        return cls("Earth", 6371000, 5.972e24, 0x0099ff, 3)

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
        return cls("Mars", 3389500, 6.39e23, 0xff6600, 4)

    @classmethod
    def jupiter(cls):
        return cls("Jupiter", 69911000, 1.898e27, 0xffcc66, 5)

    @classmethod
    def saturn(cls):
        return cls("Saturn", 58232000, 5.683e26, 0xfff7e6, 6)

    @classmethod
    def uranus(cls):
        return cls("Uranus", 25362000, 8.681e25, 0xcceeff, 7)

    @classmethod
    def neptune(cls):
        return cls("Neptune", 24622000, 1.024e26, 0x0066ff, 8)

    # KSP Presets
    @classmethod
    def kerbin(cls):
        return cls("Kerbin", 600000, 5.2915793e22, 0xCCCCCC)
