# Hydrate Dissociation Mass Estimation Tool

This python script, `hyd_diss_mass.py`, processes images of molecular trajectories and outputs the mass of the remaining hydrate versus simulation time. The code utilizes a template-matching algorithm to count the number of hydrate unit-cells in the simulation box, then converts the unit-cell count to hydrate mass using the mass density of the hydrate at given pressure and temperature conditions. The size of the simulation box is automatically taken into account when matching hydrate unit-cells.

## Basic Usage

```bash
python hyd_diss_mass.py -sd <path_to_simulation_directory> -nupt <number_of_perpendicular_unit_cells> -su <simulation_unit_time> <simulation_unit_length> -ou <output_unit_time> <output_unit_length> -ti <time_step> <dump_freq> 
```

## Inputs
`-sd <path_to_simulation_directory>`: Specifies the path to the directory containing the simulation results. Each restart run should have its own subdirectory within this directory. Each restart case should have multiple subdirectories, with each subdirectory containing rendered molecular images from a box slice.

`-nupt <number_of_perpendicular_unit_cells>`: Specifies the depth of each slice in terms of the number of unit-cells in the direction parallel to the slice's normal vector.

`-su <simulation_unit_time> <simulation_unit_length>`: Sets the simulation units for time and length dimensions.

`-ou <output_unit_time> <output_unit_length>`: Sets the desired output units for time and length dimensions.

`-ti <time_step> <dump_freq>`: Specifies the simulation time-step (in femtoseconds) and the dumping frequency used in the LAMMPS simulations.

Optional Arguments
`-si <number_of_skipped_images>`: To speed up processing, users can set this argument to skip a certain number of images.

## Sample Data
Sample data is located in the data folder. Users can run the script using this data to test the functionality of the code. For Windows users, the `run_example_win.bat` script is provided to run the code on the sample data, while Linux users can use the provided `run_example_linux.sh` script.



## Author:
### Meisam Adibifard, madibi1@lsu.edu, me.adibifard@gmail.com

## PI:
### Dr. Olufemi Olorode, folorode@lsu.edu
