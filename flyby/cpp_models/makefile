# Compile the JPL ephemeris library first
# Then compile the C++ models

main: jpleph.o test_ephemeris.o
	g++ -o test_ephemeris test_ephemeris.o jpleph.o

jpleph.o: jpl_eph/jpleph.cpp
	gcc -c jpl_eph/jpleph.cpp -I lunar

test_ephemeris.o: test_ephemeris.cpp
	g++ -c test_ephemeris.cpp