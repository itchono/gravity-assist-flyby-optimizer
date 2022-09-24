# Coordinate Systems

Several different coordinate systems are used in the project. This document describes them.

# Planetary

## PCI - Planet Centered Inertial
* Centered at the center of mass of the Planet
* Inertial - no acceleration from rotation

## PCC - Planet Centered Co-rotating
* Centered at the center of mass of the Planet
* Rotates with the planet

# Solar System

## ICRS - International Celestial Reference System
* Centered at the center of mass of the solar system
* Inertial - no acceleration from rotation

All physics calculations are done in the ICRS. The ICRS is the standard coordinate system for the solar system. It is centered at the center of mass of the solar system and is inertial. This means that it does not rotate with the solar system. This is the coordinate system that the physics engine uses.

# Conversions

## PCI to PCC
* Rotate about the z-axis by the planet's rotation rate

## PCI to ICRS
* Translate by the planet's position in the solar system


