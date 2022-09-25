# Gravity Assist Flyby Optimizer
This is a personal project about determining optimal gravity-assist based flyby trajectories for interplanetary missions. The goal is to determine the optimal trajectory for a spacecraft to fly from one planet to another using the least amount of fuel. The project is written in Python and is accelerated using C extensions. The project is currently in the early stages of development.

# Components
## Solar System Model
I built my own solar system model using planetary data from JPL Development Ephemerides (DE440). Below is a plot of the solar system model with the planets and their orbits.
![Solar System Plot Demo](https://raw.githubusercontent.com/itchono/gravity-assist-flyby-optimizer/assets/solar_system_plot_demo.png)