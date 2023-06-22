## TCL scripts to run in VMD (Visual Molecular Dynamics)

There are two TCL scripts in this directory. The goal of each script is explained below:

### 1. RenderWithClippingPlanes.tcl
This script is designed to work with VMD (Visual Molecular Dynamics) software. It takes the currently loaded molecule in VMD, creates slices for each simulation frame using two clipping planes with opposite normal vectors, and renders the resulting slice into an image.

### Usage:
### Input parameters:
#### 1. The number of Slices: 

The user can specify the number of trajectory slices. This can be set in the script on the line with set Ns 5. Replace 5 with the desired number of slices.

 #### 2. Render Directory: 
 
 The directory where the rendered images will be saved. This can be set in the script on the line with `set render_dir "/path/to/save/the/rendered/images"`. Replace `/path/to/save/the/rendered/images` with your preferred directory path.

For example, if you want to create 10 slices and save the images to a directory at `/home/user/rendered_images`, you would modify the lines as follows:

`set Ns 10`
`set render_dir "/home/user/rendered_images"`



### 2. load_lmptrj_multipleRestarts.tcl


### Prerequisites:

### Basic Usage:

#### Author:
### Meisam Adibifard, madibi1@lsu.edu, me.adibifard@gmail.com

#### PI:
### Dr. Olufemi Olorode
