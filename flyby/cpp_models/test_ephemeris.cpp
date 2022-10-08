#include <eigen3/Eigen/Dense>
#include "ephemeris_wrapper.hpp"
#include <iostream>

// This is a simple test program to demonstrate the use of the JPL ephemeris library

int main()
{
    JPLEphemeris ephemeris = JPLEphemeris("../../linux_p1550p2650.440");

    double time = 2451545.0;

    std::array<double, 3> eph_position = ephemeris.compute(time, 12, 3);

    Eigen::Vector3d position(eph_position[0], eph_position[1], eph_position[2]);

    Eigen::Vector3d reference(-2.75702837e+07, 1.32358140e+08, 5.74177286e+07);

    std::cout << "Position of Earth at J2000: " << position.transpose() << " km" << std::endl;
    std::cout << "Reference position: " << reference.transpose() << " km" << std::endl;

    std::cout << "Difference: " << (position - reference).transpose() << " km" << std::endl;
}