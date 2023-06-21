# Author: Meisam Adibifard
# This code tracks the multi-phase interface using the captured images from MD (Molecular Dynamic) simulations
# This is accomplished via image processing algorithms/techniques

from pickle import NONE
from tabnanny import NannyNag
from skimage import data
from skimage import filters
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from operator import attrgetter # to find a specific attribute of a class

from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
import cv2
#from google.colab.patches import cv2_imshow
import pixellib
#from pixellib.semantic import semantic_segmentation
import imutils
import copy
import os
import argparse
import pathlib
import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom
import pandas as pd
from tqdm import tqdm

import ntpath

# import in-house modules
from modules.units import units 
from modules.settings import ImageCrystSettings
from modules.simulation import DynamicData, SimBox, simulation

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
    parser.add_argument("--units","-u",type=int,required=True,help='The units for the output data')
    parser.add_argument("--tinfo","-ti",nargs=2,required=True,help='Gets dt (fs), and dump_freq (#time-steps) respectively (required)')

    # optional arguments
    parser.add_argument("--NumImagesSkipped","-sf",type=int,required=False,default=1, help='The number of images skipped to speed up the calculations (optional), default=1')
    
    # parse the arguments
    args=parser.parse_args()
    
    simDir=str(pathlib.PurePosixPath(args.SimDir))
    dt=float(args.tinfo[0])
    dump_freq=int(args.tinfo[1])
    NumCrystPerLayer=args.NucellPerTraj

    numImagesSkipped=args.NumImagesSkipped
    
    
SimUnits=units('fs','','A')
OutUnits=units('ns','gr','A')

dump_freq=20000 # number of time-steps per LAMMPS trajectory dump
dt=10 #fs (simulation time-step)
simDir=r'D:\renders_tmp\p75atm_Teq281K_Tb291K'
SimDynamics=DynamicData(dt,dump_freq)
MySimBox=SimBox(80,10,10,SimDynamics,SimUnits,OutUnits)

numImagesSkipped=100
NumCrystPerLayer=2
imageCrystalSetting=ImageCrystSettings(numImagesSkipped,NumCrystPerLayer)

MySimCase=simulation(simDir,MySimBox)
MySimCase.process_restarts()
MySimCase.collectWriteOutputData()

pass
