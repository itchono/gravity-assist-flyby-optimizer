#include "celestial_body.hpp"

Eigen::Vector3d CelestialBody::get_position(const double time)
{
    std::array<double, 3> position = this->ephemeris->compute(time, 12, this->ephemeris_id);

    return Eigen::Vector3d(position);
}