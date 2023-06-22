# Author: Meisam Adibifard
# This code tracks the multi-phase interface using the captured images from MD (Molecular Dynamic) simulations
# This is accomplished via image processing algorithms/techniques

import os
import argparse
import pathlib
from tqdm import tqdm

import ntpath

# import in-house modules
from modules.units import units 
from modules.settings import simSettings
from modules.simulation import  simulation

# Here the code begins
# set type of input
toi=2 # 1:cli, 2: in source code
if toi==1:
    # Get input form cli
    parser=argparse.ArgumentParser();
    # required arguments
    parser.add_argument("--SimDir","-sd",type=str,required=True,help='The path to the simulation directory where all restart folders are located (required)')
    parser.add_argument("--NucellPerTraj","-nupt",type=int,required=True, help="""The depth of each simulation trajectory, which is the number of unit-cells
        by which each simulation trajectory is extended in the direction normal to its plane (required)""")
    parser.add_argument("--Simunits","-su",nargs=2,required=True,help='The units for the simulation data in the following format [time,length]')
    parser.add_argument("--Outunits","-ou",nargs=2,required=True,help='The units for the output data in the following format [time,length]')
    parser.add_argument("--tinfo","-ti",nargs=2,required=True,help='Gets dt (fs), and dump_freq (#time-steps) respectively (required)')

    # optional arguments
    parser.add_argument("--NumImagesSkipped","-si",type=int,required=False,default=1, help='The number of images skipped to speed up the calculations (optional), default=1')
    
    # parse the arguments
    args=parser.parse_args()
    
    simDir=str(pathlib.PurePosixPath(args.SimDir))

    dt=float(args.tinfo[0])
    dump_freq=int(args.tinfo[1])
    
    NumCrystPerLayer=args.NucellPerTraj
    numImagesSkipped=args.NumImagesSkipped

    SimUnits=units(args.Simunits[0],args.Simunits[1])
    OutUnits=units(args.Outunits[0],args.Outunits[1])
else:
    simDir=r'inputs\trajectories'

    dt=10 #fs (simulation time-step)
    dump_freq=20000 # number of time-steps per LAMMPS trajectory dump
    
    NumCrystPerLayer=2
    numImagesSkipped=100

    SimUnits=units('fs','A')
    OutUnits=units('s','A')

    

SimUnits.update_convfactors()  
DynamicData={"dt":dt,"dump_freq":dump_freq}
# set the global settings 
simulation_settings=simSettings(numImagesSkipped,NumCrystPerLayer,DynamicData,SimUnits,OutUnits)
# instantiate a simulation case
SimCase=simulation(simDir)
# process the images and generate mass(hydrate)-time data
SimCase.run()

pass
