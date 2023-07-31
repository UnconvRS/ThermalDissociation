# TCL scripts to run in VMD (Visual Molecular Dynamics)

There are two TCL scripts in this directory. The goal of each script is explained below:

## 1. RenderWithClippingPlanes.tcl
This script is designed to work with VMD (Visual Molecular Dynamics) software. It takes the currently loaded molecule in VMD, creates slices for each simulation frame using two clipping planes with opposite normal vectors, and renders the resulting slice into an image.

### Usage:
#### Input parameters:
#### 1. The number of Slices: 

The user can specify the number of trajectory slices. This can be set in the script on the line with set Ns 5. Replace 5 with the desired number of slices.

 #### 2. Rendering Directory: 
 
 The directory where the rendered images will be saved. This can be set in the script on the line with `set render_dir "/path/to/save/the/rendered/images"`. Replace `/path/to/save/the/rendered/images` with your preferred directory path.

For example, if you want to create 10 slices and save the images to a directory at `/home/user/rendered_images`, you would modify the lines as follows:

`set Ns 10`

`set render_dir "/home/user/rendered_images"`

## 2. load_lmptrj_multipleRestarts.tcl

This script is designed to work with VMD (Visual Molecular Dynamics) software. It is used to import and process multiple LAMMPS restart files. The script reads the path to a parent directory that contains all the restart folders (each containing individual simulation results). It then loads the topological data of the molecules into VMD. The script iterates through the restart folders, importing the trajectory of each restart case into the loaded molecules. Finally, it wraps the coordinates of the molecules inside the simulation box.

### Usage:
#### Input parameters:

#### 1. Parent Directory Path: 

This is the path to the parent directory that contains the restart cases. Upon running the script user will be asked to input the parent directory.

#### 2. Restart Folder String Pattern: 

This is the common string pattern in the restart folders' names. This can be modified on the line with `set dir_tmpl "rest"`. Note that the name of each restart folder must contain a two-digit number. If the restart case falls below 10, then it must be left-padded with a leading zero.

#### 3. First and Last Restart Cases: 

The script will read results starting from the first restart case and up to the last restart case. These can be set on the lines with `set num_rest_folder_init 7` and `set num_rest_folder_final 12`. Replace 7 and 12 with your preferred start and end cases.

#### 4. Molecular Topology File: 

The name of the file from which to read the topological data. This can be a LAMMPS `.data` or a GROMACS `.gro` file. The type of the topology file is specified in the line `set mol_type "lmp_data"`. The topology file should be located in the parent directory. 

#### 5. LAMMPS Trajectory File Name: 

The name of the LAMMPS trajectory file. This can be modified on the line with `set lmp_trjfile_name "trajectory.lammpstrj"`.

For example, if your parent directory is at `/home/user/restarts`, the string pattern in the restart folders is `rest`, you want to read results from restart cases `5` to `10`, your topology file is a LAMMPS data file, and your LAMMPS trajectory file is named `myTrajectory.lammpstrj`, you would modify the lines as follows:

`set dir_ref "/home/user/restarts"`

`set dir_tmpl "rest"`

`set num_rest_folder_init 5`

`set num_rest_folder_final 10`

`set mol_type "lmp_data"`

`set lmp_trjfile_name "myTrajectory.lammpstrj"`


## Author:
### Meisam Adibifard, madibi1@lsu.edu, me.adibifard@gmail.com

## PI:
### Dr. Olufemi Olorode
