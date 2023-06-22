"""
a python module that holds the classes attributed to the simulation box
"""
import os
import csv
import pandas as pd
from operator import attrgetter
from tqdm import tqdm
import matplotlib.pyplot as plt

# import in-house modules
from modules.image import image
from modules.crystal import sIcrystal
from modules.settings import simSettings

# a class for a trajectory slice
class slice:
    def __init__(self,slicePath,numCrystPrepPerLayer):
        self.path=slicePath 
        self.numCrystPrepPerLayer=numCrystPrepPerLayer # number of crystal units in the direction prependicular to the layer
        self.md_image_files=os.listdir(self.path)
        self.md_image_files=sorted([x for x in self.md_image_files if x.endswith(".ppm")]) # this command only reads images with ".ppm" extension
        self.numCrystals=[] 
        self.massCrystals=[] 
        
    @staticmethod
    def SortRenamefiles(dirpath):        
        files=os.listdir(dirpath)
        sorted_files=sorted([x for x in files if x.endswith(".ppm")])
        for i, filename in enumerate(sorted_files):
            old_path = os.path.join(dirpath, filename)
            filename_wo_ext=os.path.splitext(filename)[0]
            filename_prefix=filename_wo_ext.split("-")[0]
            try:
                #filename_suffix=int(filename_wo_ext[-5:].replace(" ",""))
                filename_suffix=int(filename_wo_ext.split("-")[1].replace(" ",""))
                new_filename = f"{filename_prefix}-{filename_suffix:04}.ppm" # Pad with four zeros
                new_path = os.path.join(dirpath, new_filename)
                os.rename(old_path, new_path)
            except:
                pass



# a class to take the trajectory data    
class trajectory:
    # the path to the output data
    output_dir="output/"
    
    # get the template images
    si_image=image(sIcrystal.si_tmpl_path)
    si_top_half_image=image(sIcrystal.si_tmpl_tophalf_path)
    si_bottom_half_image=image(sIcrystal.si_tmpl_bottomhalf_path)

    # constructor
    def __init__(self,t0,slices):
        # retrieve the global simulation settings
        self.simSettings=simSettings.get_instance()

        self.slices=slices
        self.t0=t0
        self.numSiCrystals=[] 
        self.massSi=[]
        self.numSiiCrystals=[] 
        self.Si_unit=sIcrystal()
        self.xlo_interface=[] 
        self.xhi_interface=[] 
        self.simTime_SimUnits=[]
        self.simTime_OutUnits=[] 
        self.__DetermineConversionFactors()

        

    # a static method to scale the pixel data to simulation-unit data 
    @staticmethod
    def PixelsToSimUnits(x_pixels,ppa,xref_pixel,xref_sim): # ppa: pixels per angstrom
        dx_pixels=x_pixels-xref_pixel # in pixels
        dx_sim=dx_pixels/ppa
        x_sim=dx_sim+xref_sim
        return x_sim


    # a private method to get the convesion factor that is used to write the outputs in the user-specified units
    def __DetermineConversionFactors(self):
        
        timeConvString=f"{self.simSettings.SimUnits.time}2{self.simSettings.OutUnits.time}"
        lengthConvString=f"{self.simSettings.SimUnits.length}2{self.simSettings.OutUnits.length}"
        self.timeConvertor=1.0 if self.simSettings.SimUnits.time==self.simSettings.OutUnits.time else attrgetter(timeConvString)(self.simSettings.SimUnits)  
        self.LengthConvertor=1.0 if self.simSettings.SimUnits.length==self.simSettings.OutUnits.length else attrgetter(lengthConvString)(self.simSettings.SimUnits)  

    def detect_crystalls(self,numImagesSkipped):
        # update the timer
        self.timer=self.t0
        num_images=len(self.slices[0].md_image_files)
        dataIndex=0
        # iterate over the rendered MD images
        for i in tqdm(range(0,num_images,numImagesSkipped)):
            for slice in self.slices:
                imgfile=slice.md_image_files[i]
                img_full_path=os.path.join(slice.path,imgfile)
            
                currentImage=image(img_full_path)
                currentImage.TemplateMatching(self.si_top_half_image)
                numTopHalf=currentImage.numSiCrystals

                currentImage2=image(img_full_path)
                currentImage2.TemplateMatching(self.si_bottom_half_image)
                numBotHalf=currentImage2.numSiCrystals

                numTotalSi_xy=0.5*(numTopHalf+numBotHalf)
                numTotalSi_xyz=numTotalSi_xy*slice.numCrystPrepPerLayer
                # mass of the remaining hydrate
                massSi_xyz=numTotalSi_xyz*(self.Si_unit.UnitVol*pow(self.simSettings.SimUnits.A2cm,3))*self.Si_unit.density
                
                slice.numCrystals.append(numTotalSi_xyz)
                slice.massCrystals.append(massSi_xyz)
                
            
            # update crystal data
            self.numSiCrystals.append(sum(slice.numCrystals[dataIndex] for slice in self.slices))
            self.massSi.append(sum(slice.massCrystals[dataIndex] for slice in self.slices))

            # update the simulation time vector
            self.simTime_SimUnits.append(self.timer*self.simSettings.temporal["dt"]*self.simSettings.temporal["dump_freq"])            # time in fs or whatever the simulation units is
            self.simTime_OutUnits.append(self.simTime_SimUnits[-1]*self.timeConvertor)                                           # time in requested output unit
                
            # update the timer and the data index
            self.timer+=numImagesSkipped
            dataIndex+=1
            

    def WriteTemporalData(self,data,flag,fileName):
        # data should be of the same size as the time vector
        fullfilepath=os.path.join(self.output_dir,fileName,".csv")

        with open(fullfilepath,'w',newline='') as csv_file:
            fieldnames = ['time(ns)', flag]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(len(self.sim_time_ns)):
                writer.writerow({'time(ns)':self.sim_time_ns[i],flag:data[i]})


# a class for the restart case
class restart():

    def __init__(self,dir,slices):
        self.dir=dir
        self.slices=slices

    def __str__(self):
        return f'this is a restart case located at {self.dir}'

    # a method to instantiate a simulation trajectory
    def init_trajectory(self,t0):
        self.t0=t0
        self.traj=trajectory(self.t0,self.slices)


# a class for the simulation instance
class simulation():
    OutputData=pd.DataFrame()
    OutputData['time']=[] 
    OutputData['num_unit_cells']=[] 
    OutputData['mass_hydrate']=[] 

    # you may need to provide local path to the images if the images are not stored directly under the restart folder 
    localPath=r''

    # constructor
    def __init__(self,workingDir):
        self.simDir=workingDir
        self.restarts=[]

    # a private method to get the list of the restart cases
    def __GetRestartFoldersSorted(self):
        numSubdirs=0
        for item in os.scandir(self.simDir):
            if item.is_dir():
                numSubdirs+=1
                # locate the subdirectories
                subdirs=os.scandir(item.path)
                #self.GetSubfolders(os.path.join(item,self.localPath))
                slices=[]
                for folder in subdirs:
                    slices.append(slice(folder.path,simSettings.get_instance().NumCrystPerLayer))
                self.restarts.append(restart(item,slices)) # input the arbitrary t0=0 for t0

        if numSubdirs!=0:
            # sort the restart cases based on the restart directory name
            self.restarts.sort(key=lambda x:x.dir.name, reverse=False)
        else:
            raise Exception("no subdirectories found! make sure there is at least a restart subdirectory...")


    def process_restarts(self):
        # find and sort the restart folders within the working directory
        self.__GetRestartFoldersSorted()

        # iterate over the folders in the working directory 
        t0=0
        count=0
        for restart in self.restarts:
            # process the image files for each restart case
            print("images from restart-{} are being processed".format(count))
            # initialize the trajectory class within the restart class            
            restart.init_trajectory(t0)
            restart.traj.detect_crystalls(simSettings.get_instance().numImagesSkipped)
            
            # set the t0 for the next restart 
            t0=restart.traj.timer
            count+=1
    

    # an auxiliary method to return the subdirectories of a directory
    @staticmethod 
    def GetSubfolders(parentPath):
        try:
            return next(os.walk(parentPath))[1]
        except StopIteration:
            return []


    # collect and dump the output data into a csv file
    def collectWriteOutputData(self):
        for restart in self.restarts:
            dictn = {'time':restart.traj.simTime_OutUnits,'num_unit_cells':restart.traj.numSiCrystals,'mass_hydrate':restart.traj.massSi}
            self.OutputData=self.OutputData.append(pd.DataFrame(dictn),ignore_index=True)

        self.OutputData.to_csv(os.path.join(self.workingDir,f'outputData_TstepsSkipped{simSettings.get_instance().numImagesSkipped}.csv'))


    def run(self):
        self.process_restarts()
        self.collectWriteOutputData()