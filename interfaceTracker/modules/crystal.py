"""
a python module for crystal classes
"""
import matplotlib.pyplot as plt
import numpy as np
from operator import attrgetter

# a class to create a custom crystal object
class crystal:
    def __init__(self,Xcentroid,Ycentroid,NumHost,NumGuest,UnitVol,density):
        self.Xcentroid=Xcentroid 
        self.Ycentroid=Ycentroid
        self.NumHost=NumHost
        self.NumGuest=NumGuest 
        self.UnitVol=UnitVol    #(Angstrom)^3
        self.density=density    # gr/cm3


class sIcrystal(crystal):
    ## class attributes ################################################################
    UnitVol=1728 #(Angstrom)^3
    NumHost=46 # h2o molecules
    NumGuest=8 # ch4 molecules
    density=0.9 # gr/cm3
    si_tmpl_path="C:/Research/Gas Hydrates/Codes/InterfaceTracker/InterfaceTracker/data/template/sI/sI_tmpl.ppm"
    si_tmpl_tophalf_path="C:/Research/Gas Hydrates/Codes/InterfaceTracker/InterfaceTracker/data/template/sI/sI_tmpl_top_half.ppm"
    si_tmpl_bottomhalf_path="C:/Research/Gas Hydrates/Codes/InterfaceTracker/InterfaceTracker/data/template/sI/sI_tmpl_bottom_half.ppm"
    ## class attributes ################################################################

    def __init__(self):
        self.Xcentroid=None 
        self.Ycentroid=None 

class sIIcrystal(crystal):
    ## class attributes ################################################################
    UnitVol=None #(Angstrom)^3
    NumHost=None # h2o molecules
    NumGuest=None # ch4 molecules
    sii_tmpl_path="C:/Research/Gas Hydrates/Codes/InterfaceTracker/InterfaceTracker/data/template/sI/sI_tmpl.ppm"
    ## class attributes ################################################################

    def __init__(self):
        self.Xcentroid=None 
        self.Ycentroid=None       


# a class for a list of crystals
class crystals:
    def __init__(self,listOfCrystals): # listOfCrystals should be a list of crystal objects
        self.crystals=listOfCrystals

    def InterfaceLines(self,Nd):
        # find the lower and upper limits for yCentroid
        YlowerCrystal = min(self.crystals,key=attrgetter('Ycentroid'))
        YupperCrystal=max(self.crystals,key=attrgetter('Ycentroid'))
        
        # set slab thickness prependicular to the y-direction 
        # (Nd is the number of slabs prependicular to the y direction, set by the user)
        dy=(YupperCrystal.Ycentroid-YlowerCrystal.Ycentroid)/Nd 
        slab_y=np.arange(YlowerCrystal.Ycentroid-dy, YupperCrystal.Ycentroid+dy, dy).tolist()

        self.lowerXboundCrystals=[] 
        self.upperXboundCrystals=[] 
        for i in range(0,len(slab_y)-1):
            inSlabCrystals=[] 
            for crystal in self.crystals:
                if crystal.Ycentroid<=slab_y[i+1] and crystal.Ycentroid>=slab_y[i]:
                    inSlabCrystals.append(crystal)

            # find bounding crystals in the x-direction for the slab
            if len(inSlabCrystals)>1:
                self.lowerXboundCrystals.append(min(inSlabCrystals,key=attrgetter('Xcentroid')))
                self.upperXboundCrystals.append(max(inSlabCrystals,key=attrgetter('Xcentroid')))
        
        if len(self.lowerXboundCrystals)>1:
            Interface_lowerCrystal=min(self.lowerXboundCrystals,key=attrgetter('Xcentroid'))
            self.interface_xlower=Interface_lowerCrystal.Xcentroid

        if len(self.upperXboundCrystals)>1:
            Interface_upperCrystal=max(self.upperXboundCrystals,key=attrgetter('Xcentroid'))
            self.interface_xupper=Interface_upperCrystal.Xcentroid
        
        if len(self.crystals)>0:
            Interface_lowerCrystal=min(self.crystals,key=attrgetter('Xcentroid'))
            self.interface_xlower=Interface_lowerCrystal.Xcentroid

        if len(self.crystals)>0:
            Interface_upperCrystal=max(self.crystals,key=attrgetter('Xcentroid'))
            self.interface_xupper=Interface_upperCrystal.Xcentroid
         

    def plot2Dxy(self,crystals_toplot):
        plt.plot([c.Xcentroid for c in crystals_toplot],[c.Ycentroid for c in crystals_toplot],'-o',markersize=1)
        plt.pause(0.000001);
        pass


