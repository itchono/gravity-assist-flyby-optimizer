#include <string>
#include <eigen3/Eigen/Dense>
#include "ephemeris_wrapper.hpp"

class CelestialBody
{
public:
    std::string name;
    double mass;
    double radius;
    int color; // stored as hex value
    int ephemeris_id;

    JPLEphemeris *ephemeris;

    Eigen::Vector3d get_position(const double time);
    Eigen::Vector3d get_velocity(const double time);
};
