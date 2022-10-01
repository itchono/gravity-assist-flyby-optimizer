#include <string>
#include <eigen3/Eigen/Dense>
#include "interpolator.h"
#include "../../jpl_eph/jpleph.h"
#include "../../jpl_eph/jpl_int.h"

class CelestialBody
{
public:
    std::string name;
    double mass;
    double radius;
    int color; // stored as hex value
    int ephemeris_id;

    jpl_eph_data *ephemeris;

    Eigen::Vector3d get_position(double time);
    Eigen::Vector3d get_velocity(double time);
};
