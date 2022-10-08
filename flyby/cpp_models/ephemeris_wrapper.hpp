#include <cstdio>
#include <cstdint> // remmeber to include these two headers if you want jpleph to compile
#include "jpl_eph/jpleph.h"
#include "jpl_eph/jpl_int.h"
#include <string>
#include <array>

class JPLEphemeris
{
private:
    jpl_eph_data *data;

public:
    JPLEphemeris(const char *path);
    ~JPLEphemeris();

    std::array<double, 3> compute(const double time_jd, const int id_root, const int id_body);
    std::array<double, 6> compute_and_differentiate(const double time_jd, const int id_root, const int id_body);
};