#include <eigen3/Eigen/Dense>
#include <cstdio>
#include <cstdint> // remmeber to include these two headers if you want jpleph to compile
#include "jpl_eph/jpleph.h"
#include "jpl_eph/jpl_int.h"

#include <iostream>

// This is a simple test program to demonstrate the use of the JPL ephemeris library

int main()
{
    jpl_eph_data *ephemeris = (jpl_eph_data *)jpl_init_ephemeris("../../linux_p1550p2650.440", NULL, NULL);

    if (ephemeris == NULL)
    {
        std::cout << "Error: ephemeris is NULL" << std::endl;
        return 1;
    }

    double time = 2451545.0;
    double position_velocity[6];
    jpl_pleph(ephemeris, time, 3, 12, position_velocity, 0);

    Eigen::Vector3d position(position_velocity[0], position_velocity[1], position_velocity[2]);

    Eigen::Vector3d reference(-2.75702837e+07, 1.32358140e+08, 5.74177286e+07);
    position *= ephemeris->au; // convert AU to km

    std::cout << "Position of Earth at J2000: " << position.transpose() << " km" << std::endl;
    std::cout << "Reference position: " << reference.transpose() << " km" << std::endl;

    std::cout << "Difference: " << (position - reference).transpose() << " km" << std::endl;
}