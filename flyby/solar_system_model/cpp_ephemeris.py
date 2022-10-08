

import cppyy
import cppyy.ll
import numpy as np

# wrapper
cppyy.add_include_path(
    "flyby/cpp_models")
cppyy.add_library_path(
    "flyby/cpp_models")
cppyy.include("ephemeris_wrapper.hpp")


cppyy.load_library("jpleph.so")  # needs to be full relative path, not in

de440 = cppyy.gbl.JPLEphemeris("linux_p1550p2650.440")

if __name__ == "__main__":
    time = 2451545.0

    position = de440.compute(time, 12, 3)
    arr = np.array(position)
    print(arr)
