# a procedure to return a string with n number of zeros depending upon the number of meaningful digits given to it as input
proc GenZerosString {number_digits} {

	# the total number of digits (including zeros and non-zeros)
	set num_total_digits 2 
	set num_zeros [expr $num_total_digits-$number_digits]
	set zeros_string [string repeat "0" $num_zeros]
	
	return "$zeros_string"

}

set dir_ref "/scratch/madibi/MDSim/ch4_hydrate/Mw_Model/CalcTdiss/Interface_method/NPT/Box_80_10_10/p_100atm_new/NPHSimulations/Teq_283K/Tb_288K/"
set dir_tmpl "rest"
set num_rest_folder_init 7
set num_rest_folder_final 12

set datafile_name "MwHydarteTime0.data"
set lmp_trjfile_name "NPH_Trajectory.lammpstrj"

for {set restartNumber $num_rest_folder_init} {$restartNumber <= $num_rest_folder_final} {incr restartNumber} {

	set num_digits [string length $restartNumber]
	
	set zeros_string [GenZerosString $num_digits]
	
	set currentRestDir [join [list $dir_tmpl$zeros_string$restartNumber]]
         
	puts $currentRestDir 
      
        set currentRestDir_path [join [list $dir_ref$currentRestDir]]
        cd $currentRestDir_path

	# read the lammps data file if we are in restart0
	if {$restartNumber==$num_rest_folder_init} {
		topo readlammpsdata $datafile_name
	}
        	
	# load the lammps trajectory file
	mol addfile $lmp_trjfile_name waitfor all
	

}

# wrap the coordinates of the atoms after loading all the lammps trajectory files
pbc wrap -all




