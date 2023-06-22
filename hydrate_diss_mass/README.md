# Hydrate Dissociation Mass Estimation Tool

This python script, `hyd_diss_mass.py`, processes images of molecular trajectories and outputs the mass of the remaining hydrate versus simulation time. The code utilizes a template-matching algorithm to count the number of hydrate unit-cells in the simulation box, then converts the unit-cell count to hydrate mass using the mass density of the hydrate at given pressure and temperature conditions. The size of the simulation box is automatically taken into account when matching hydrate unit-cells.

## Basic Usage

```bash
python hyd_diss_mass.py -sd <path_to_simulation_directory> -nupt <number_of_perpendicular_unit_cells> -su <simulation_unit_time> <simulation_unit_length> -ou <output_unit_time> <output_unit_length> -ti <time_step> <dump_freq> bash```


### Author:
#### Meisam Adibifard, madibi1@lsu.edu, me.adibifard@gmail.com

### PI:
#### Dr. Olufemi Olorode, folorode@lsu.edu
