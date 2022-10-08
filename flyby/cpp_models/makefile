# Compile the JPL ephemeris library first
# Then compile the C++ models

main: jpleph.o test_ephemeris.o ephemeris_wrapper.o
	g++ -o test_ephemeris test_ephemeris.o jpleph.o ephemeris_wrapper.o

shared: jpleph.o ephemeris_wrapper.o
	g++ -shared -o jpleph.so jpleph.o ephemeris_wrapper.o 

jpleph.o: jpl_eph/jpleph.cpp
	gcc -c jpl_eph/jpleph.cpp -I lunar

test_ephemeris.o: test_ephemeris.cpp
	g++ -c test_ephemeris.cpp

ephemeris_wrapper.o: ephemeris_wrapper.cpp
	g++ -c ephemeris_wrapper.cpp