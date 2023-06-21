# Written by: Meisam Adibifard (PhD Student in Engineering Science, Louisiana State University)
# This script load a molecule, import the lammps trajectory, and renders the time tailored images at different clipping planes

# a procedure to set the display settings
proc SetDisplaySettings {} {
    #display resize 4000 3000 
    color Display Background white
    color Axes Labels black
    #pbc box -color black
    display projection orthographic
}

# a procedure to modify the molecule's representation settings
proc ModifyMolRepr {molID bwc} {
	# create new representations until the number of representations==2
	set numRep [molinfo $molID  get numreps]
	while {$numRep<2} {
		mol addrep $molID
		set numRep [molinfo $molID get numreps]
	}
	# set rep styles
	mol modstyle  0 $molID  "lines"
	mol modstyle  1 $molID  "lines"
	# set atom type for each rep
	mol modselect 0 $molID  "type 1"
	mol modselect 1 $molID  "type 2"
	
	# set the color of the reps based on the value of $bwc parameter
	if {$bwc=="color"} {
		# set color of each atom
		mol modcolor  0 $molID  ColorID 21
		mol modcolor  1 $molID  ColorID 1
		# make sure all representations are shown
		mol showrep $molID 0 on 
		mol showrep $molID 1 on 
	} else {
		display ambientocclusion off 
		# alter the color id for the water molecules (black)
		mol showrep $molID 0 on 
		mol modcolor  0  $molID  ColorID 16
		# hide the other reps
		mol showrep $molID 1 off 
	}
}

# a procedure to get the coordinates of the simulation box
proc GetBoxCoord {atoms} {
	set tmp [measure minmax $atoms]
	set min [lindex $tmp 0]
	set max [lindex $tmp 1]
	set zmin [lindex $min 2]
	set zmax [lindex $max 2]
	return "$zmin $zmax"
}

# a procedure to update the location of the moving slides within the box
proc CalcSlicesLoc {Ns atoms} {
	# get box boundaries
	set Zminmax [GetBoxCoord $atoms]
	set zmin [lindex $Zminmax 0]
	set zmax [lindex $Zminmax 1]
	
	set Dslice [expr ($zmax-$zmin)/$Ns]
	
	# set the upper coordinates of the slices
	# z values for clipplane with id=0
	set zi $zmin;set zf $zmax
	set z_clipPlanes0 []
	set ztmp $zf
	for {set index 0} {$index<$Ns} {incr index} {lappend z_clipPlanes0 $ztmp;set ztmp [expr $ztmp-$Dslice]}
	
	# set the lower coordinates of the slices
	# z values for clipplane with id=1
	set zi [expr [lindex $z_clipPlanes0 end]-$Dslice]
	set zf [expr [lindex $z_clipPlanes0 0]-$Dslice]
	set z_clipPlanes1 []
	set ztmp $zf
	for {set index 0} {$index<$Ns} {incr index} {lappend z_clipPlanes1 $ztmp;set ztmp [expr $ztmp-$Dslice] }
	
	return "{$z_clipPlanes0}  {$z_clipPlanes1}"
}

# a procedure to return a string with n number of zeros depending upon the number of meaningful digits given to it as input
proc GenZerosString {number_digits} {

	# the total number of digits (including zeros and non-zeros)
	set num_total_digits 4 
	set num_zeros [expr $num_total_digits-$number_digits]
	set zeros_string [string repeat "0" $num_zeros]
	
	return "$zeros_string"

}

############ load the LAMMPS data file and load the trajectory file into the loaded molecule ############
#set lmp_datatrj_dir ""


#set lmp_datafile_name ""
#set lmp_datafile_path [join [list $lmp_datatrj_dir$lmp_datafile_name]]

#set lmp_trjfile_name ""
#set lmp_trjfile_path [join [list $lmp_datatrj_dir$lmp_trjfile_name]]

# load the LAMMPS .data file
#topo readlammpsdata lmp_datafile_path

# load the LAMMPS .trj file into the loaded molecule
#mol addfile $lmp_trjfile_path time 1

############ the TCL script to render the slices of lammps trajectories ############
# set the specifications of the hydrate slides in the z-direction (all spatial values in Angstrom)
# number of slices
set Ns 5 
set all [atomselect top all] 


# Define the list of subdirectories
set clipPlane_subdirs []
set foldMain "cp"
for {set index 0} {$index<$Ns} {incr index} {set subdir_name $foldMain$index;lappend clipPlane_subdirs $subdir_name}

# Get the path to the current directory
set currentDir [pwd]

# get molid, numframes, and last frame
set MolID [molinfo top get id]
set Numframes [molinfo top get numframes]
set fr_init 1
set fr_final [expr $Numframes-1]
set imgext ".ppm"
set sep "-"


# set rendering directory
set render_dir "/Users/unconvrs/Gas Hydrate/MDsim_hpc/renders_tmp/Tb_288K/rest10/sliced_images/output_blacknwhite"
cd  $render_dir
foreach {subdir} $clipPlane_subdirs {file mkdir $subdir}

# initiate the display settings
SetDisplaySettings
ModifyMolRepr $MolID "bw"

# activate the clipplanes
mol clipplane status 0 0 $MolID 1
mol clipplane status 1 0 $MolID 1

# set normal vector for the clipping plane (we will have two clipping planes acting in reverse directions)
mol clipplane normal 0 0 $MolID "0 0 -1"
mol clipplane normal 1 0 $MolID "0 0 +1"

# Iterate over the position of the interface 
for {set frame 0} {$frame < $Numframes} {incr frame} {
    # Go to the next frame
    animate goto $frame
    sleep 1
    # determine the min-max of the slices based on the updated box coordinates
    set Sloc [CalcSlicesLoc $Ns $all]
    set z_clipPlanes0 [lindex $Sloc 0]
    set z_clipPlanes1 [lindex $Sloc 1]

    # iterate over the location of the clipping planes
    for {set index 0} {$index<$Ns} {incr index} {
    	set current_cplane_dir [lindex $clipPlane_subdirs $index]
    	cd  $current_cplane_dir
    	
    	set z_current_cPlane0 [lindex $z_clipPlanes0  $index]
    	set z_current_cPlane1 [lindex $z_clipPlanes1  $index]
    	# update the position of the clipping planes
    	mol clipplane center 0 0 $MolID "0 0 $z_current_cPlane0"
    	mol clipplane center 1 0 $MolID "0 0 $z_current_cPlane1"
    	display update
    	sleep 1
    	
    	# get the current frame number (this will be the filename for the rendered image)
    	set frameCurrent [molinfo top get frame]
    	
    	# get the number of digits in the fram number
    	set num_digits [string length $frameCurrent]
		set zeros_string [GenZerosString $num_digits]
    	set rendering_filename [join [list $current_cplane_dir$sep$zeros_string$frameCurrent$imgext]]
    	
    	# render the current VMD scene to an image
    	render TachyonInternal $rendering_filename
    	sleep 1
    	# resort to the rendering directory
    	cd $render_dir	
    }  
}

cd $currentDir

