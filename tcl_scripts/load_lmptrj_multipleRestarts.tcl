# a procedure to return a string with n number of zeros depending upon the number of meaningful digits given to it as input
proc GenZerosString {number_digits} {

	# the total number of digits (including zeros and non-zeros)
	set num_total_digits 2 
	set num_zeros [expr $num_total_digits-$number_digits]
	set zeros_string [string repeat "0" $num_zeros]
	
	return "$zeros_string"

}

set dir_ref "/path/to/parent/directory/"
set dir_tmpl "rest"
set num_rest_folder_init 7
set num_rest_folder_final 12

# set the type of data file [lmp_data or gro]
set mol_type "lmp_data"

# read the molecular topology info
if {$mol_type=="lmp_data"} {
	set mol_topology_file [glob -directory $dir_ref *.data]
	topo readlammpsdata $mol_topology_file
} elseif {$mol_type=="gro"} {
	set mol_topology_file [glob -directory $dir_ref *.gro]
	mol new $mol_topology_file
}

set lmp_trjfile_name "trajectory.lammpstrj"

for {set restartNumber $num_rest_folder_init} {$restartNumber <= $num_rest_folder_final} {incr restartNumber} {

	set num_digits [string length $restartNumber]
	
	set zeros_string [GenZerosString $num_digits]
	
	set currentRestDir [join [list $dir_tmpl$zeros_string$restartNumber]]
         
	puts $currentRestDir 
      
	set currentRestDir_path [join [list $dir_ref$currentRestDir]]
	
	cd $currentRestDir_path
	
	# load the lammps trajectory data
	mol addfile $lmp_trjfile_name waitfor all
	

}

cd $dir_ref

# wrap the coordinates of the atoms after loading all the lammps trajectory files
pbc wrap -compound res -all

# delete the 1st frame
animate delete beg 0 end 0 waitfor all molid [molinfo top]




