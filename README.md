# Gravity Assist Flyby Optimizer
This is a personal project about determining optimal gravity-assist based flyby trajectories for interplanetary missions. The goal is to determine the optimal trajectory for a spacecraft to fly from one planet to another using the least amount of fuel. The project is written in Python and is accelerated using C extensions. The project is currently in the early stages of development.

# Components
## Solar System Model
I built my own solar system model using planetary data from JPL Development Ephemerides (DE440). Below is a plot of the solar system model with the planets and their orbits.
![Solar System Plot Demo](https://raw.githubusercontent.com/itchono/gravity-assist-flyby-optimizer/assets/solar_system_plot_demo_2.png)

You can run this example by running the following command:
`
python -m flyby.visualizers.solar_system_plot`

## Time Integration of Spacecraft Dynamics
I modelled gravity from all major solar system bodies (8 planets + the Sun) acting on a spacecraft. The dynamic simulation is integrated using `scipy.integrate.solve_ivp`.

# Dependencies
## C++
### [Eigen](http://eigen.tuxfamily.org/index.php?title=Main_Page)
Install on debian-based systems:
`sudo apt-get install libeigen3-dev`

## General
### DE440 Ephemerides
Download from [JPL SSD](https://ssd.jpl.nasa.gov/ftp/eph/planets/Linux/de440/). Place the file into the root directory of the project.

e.g. `wget https://ssd.jpl.nasa.gov/ftp/eph/planets/Linux/de440/linux_p1550p2650.440`

# Installation
Once you have the dependencies installed, you can install the project by running the following command:

`pip install git+https://github.com/itchono/gravity-assist-flyby-optimizer.git`