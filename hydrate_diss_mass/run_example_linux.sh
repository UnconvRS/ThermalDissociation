#!/bin/bash

python3 hyd_diss_mass.py -sd inputs/trajectories -nupt 2 -su fs A -ou s cm -ti 10 20000 -si 100

read -p "Press any key to continue . . . " -n1 -s