#include "ephemeris_wrapper.hpp"

JPLEphemeris::JPLEphemeris(const char *path)
{
    this->data = (jpl_eph_data *)jpl_init_ephemeris(path, NULL, NULL);
    // TODO: if data == NULL, that means ephemeris creation failed.
}
JPLEphemeris::~JPLEphemeris()
{
    jpl_close_ephemeris(this->data);
}

std::array<double, 3> JPLEphemeris::compute(const double time_jd, const int id_root, const int id_body)
{
    std::array<double, 3> position;
    jpl_pleph(this->data, time_jd, id_body, id_root, (double *)&position, 0);

    for (int i = 0; i < 3; i++)
    {
        position[i] *= this->data->au; // return result will be in km
    }
    return position;
}

std::array<double, 6> JPLEphemeris::compute_and_differentiate(const double time_jd, const int id_root, const int id_body)
{
    std::array<double, 6> position_velocity;
    jpl_pleph(this->data, time_jd, id_body, id_root, (double *)&position_velocity, 0);

    for (int i = 0; i < 6; i++)
    {
        position_velocity[i] *= this->data->au; // au -> km
    }

    for (int i = 3; i < 6; i++)
    {
        position_velocity[i] *= 86400; // /day -> /sec
    }
    return position_velocity;
}