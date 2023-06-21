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
from image import image
from crystal import sIcrystal
from settings import ImageCrystSettings

# a class for the simulation box
class SimBox:
    def __init__(self,NumCryst_xinit,NumCryst_yinit,NumCryst_zinit,DynamicData,SimUnits,OutUnits):
        self.NumCryst_xinit=NumCryst_xinit
        self.NumCryst_yinit=NumCryst_yinit
        self.NumCryst_zinit=NumCryst_zinit
        self.NumCryst_init=NumCryst_xinit*NumCryst_yinit*NumCryst_zinit
        self.DynamicData=DynamicData
        self.SimUnits=SimUnits
        self.OutUnits=OutUnits


class DynamicData:
    def __init__(self,dt,dumpfreq):
        self.dt=dt
        self.dumpfreq=dumpfreq


# a class for a trajectory layer
class layer:
    def __init__(self,LayerPath,numCrystPrepPerLayer):
        self.path=LayerPath 
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
    ## class attributes ##################################################################
    output_dir="C:/Research/Gas Hydrates/Codes/InterfaceTracker/InterfaceTracker/output/"

    si_tophalf_xmldir=r'C:\Research\Gas Hydrates\Codes\InterfaceTracker\InterfaceTracker\data\annot\si_tophalf'
    si_bothalf_xmldir=r'C:\Research\Gas Hydrates\Codes\InterfaceTracker\InterfaceTracker\data\annot\si_bothalf'

    
    si_image=image(sIcrystal.si_tmpl_path)
    si_top_half_image=image(sIcrystal.si_tmpl_tophalf_path)
    si_bottom_half_image=image(sIcrystal.si_tmpl_bottomhalf_path)

    ## class attributes ###################################################################

    # class constructor
    def __init__(self,SimBox,t0,layers):
        self.SimBox=SimBox
        self.layers=layers
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


    # a static method to scaling the pixel data to simulation-unit data 
    @staticmethod
    def PixelsToSimUnits(x_pixels,ppa,xref_pixel,xref_sim): # ppa: pixels per angstrom
        dx_pixels=x_pixels-xref_pixel # in pixels
        dx_sim=dx_pixels/ppa
        x_sim=dx_sim+xref_sim
        return x_sim


    # a private method to determine the convesion factor that should be used within the processing 
    def __DetermineConversionFactors(self):
        timeConvString=self.SimBox.SimUnits.time+'2'+self.SimBox.OutUnits.time
        lengthConvString=self.SimBox.SimUnits.length+'2'+self.SimBox.OutUnits.length
        self.timeConvertor=1.0 if self.SimBox.SimUnits.time==self.SimBox.OutUnits.time else attrgetter(timeConvString)(self.SimBox.SimUnits)  
        self.LengthConvertor=1.0 if self.SimBox.SimUnits.length==self.SimBox.OutUnits.length else attrgetter(lengthConvString)(self.SimBox.SimUnits)  


    def detect_crystalls(self,numImagesSkipped):
        # update the timer
        self.timer=self.t0
        num_images=len(self.layers[0].md_image_files)
        dataIndex=0
        # iterate over the rendered MD images
        for i in tqdm(range(0,num_images,numImagesSkipped)):
            for layer in self.layers:
                imgfile=layer.md_image_files[i]
                img_full_path=os.path.join(layer.path,imgfile)
            
                currentImage=image(img_full_path)
                currentImage.TemplateMatching(self.si_top_half_image)
                #currentImage.WriteXMLfile(self.si_tophalf_xmldir)
                numTopHalf=currentImage.numSiCrystals

                currentImage2=image(img_full_path)
                currentImage2.TemplateMatching(self.si_bottom_half_image)
                #currentImage2.WriteXMLfile(self.si_bothalf_xmldir)
                numBotHalf=currentImage2.numSiCrystals

                #self.crystals=crystals(currentImage.sICrystals+currentImage2.sICrystals)

                numTotalSi_xy=0.5*(numTopHalf+numBotHalf)
                numTotalSi_xyz=numTotalSi_xy*layer.numCrystPrepPerLayer
                # mass of remaining hydrate
                massSi_xyz=numTotalSi_xyz*(self.Si_unit.UnitVol*pow(self.SimBox.SimUnits.A2cm,3))*self.Si_unit.density
                
                layer.numCrystals.append(numTotalSi_xyz)
                layer.massCrystals.append(massSi_xyz)
                
            
            # update crystal data
            self.numSiCrystals.append(sum(layer.numCrystals[dataIndex] for layer in self.layers))
            self.massSi.append(sum(layer.massCrystals[dataIndex] for layer in self.layers))

            # update simulation time vector
            self.simTime_SimUnits.append(self.timer*self.SimBox.DynamicData.dt*self.SimBox.DynamicData.dumpfreq)            # time in fs or whatever the simulation units is
            self.simTime_OutUnits.append(self.simTime_SimUnits[-1]*self.timeConvertor)                                      # time in requested output unit
                
            # update the timer and the data index
            self.timer+=numImagesSkipped
            dataIndex+=1
            

        # rescale the xlo-xhi of the moving interface
        ppa=1745/961
        xref_pixel=375
        xref_sim=0
        self.xlo_interface[:]=[self.__PixelsToSimUnits(dataPixel,ppa,xref_pixel,xref_sim) for dataPixel in self.xlo_interface]
        self.xhi_interface[:]=[self.__PixelsToSimUnits(dataPixel,ppa,xref_pixel,xref_sim) for dataPixel in self.xhi_interface]


    def crystalls_time_plot(self,y):
        figureDPI=300
        fileDPI=300
        fig = plt.figure(figsize=(30,15),dpi=30)
        axes = fig.add_axes([0, 0,1.0,1.0])
        # Set font sizes for different elements of the figure
        Inset_labelsize=55;
        XY_labelSize=60
        xyticksize=60;
        titlesize=30;
        lineWidthSize=5
        MarkrSize=20
        LegendSize=60
        AxisTickWidth=3
        AxisTickLength=10
        
        plt.xticks(fontsize=xyticksize)
        plt.yticks(fontsize=xyticksize)
        axes.xaxis.set_tick_params(width=AxisTickWidth,length=AxisTickLength,color='black')
        axes.yaxis.set_tick_params(width=AxisTickWidth,length=AxisTickLength,color='black')
        axes.set_xlabel("time, [ns]",fontsize=XY_labelSize);
        axes.set_ylabel("Si patterns, []",fontsize=XY_labelSize);
        axes.xaxis.grid(True, which='minor')

        #title_temporal=title+"�$t_{sim}$="+str(time)
        #axes.set_title(title_temporal,fontsize=titlesize)
        #axes.set_ylim([yminmax[0],yminmax[1]]);
        # Adjust the legend properties
#        plt.legend(loc='upper right', prop={'size': LegendSize},labelspacing=0.1,handleheight=0.3,borderaxespad=0.1,borderpad=0.2)

        plt.setp([axes.get_xticklines(), axes.get_yticklines()], color='black')
        plt.setp(axes.spines.values(),color='black')
        axes.spines["top"].set_color("black");axes.spines["bottom"].set_color("black")
        axes.spines["left"].set_color("black");axes.spines["right"].set_color("black")
        
        # resize time data if y and time are not the same size
        self.sim_time_ns=self.sim_time_ns[:len(y)-len(self.sim_time_ns)] if len(y)!=len(self.sim_time_ns) else self.sim_time_ns

        axes.plot(self.sim_time_ns,y,linestyle='', marker='o',markersize=MarkrSize, color='r',linewidth=lineWidthSize,label='MD Simulations');
        
#        self.axes.legend()
        plt.pause(0.000001);
        pass

    def WriteTemporalData(self,data,flag,fileName):
        # data should be of the same size as the time vector
        fullfilepath=self.output_dir+fileName+".csv"

        with open(fullfilepath,'w',newline='') as csv_file:
            fieldnames = ['time(ns)', flag]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(len(self.sim_time_ns)):
                writer.writerow({'time(ns)':self.sim_time_ns[i],flag:data[i]})


# a class for the restart case
class restart():

    def __init__(self,dir,simBox,layers):
        self.dir=dir
        self.simBox=simBox
        self.layers=layers

    def __str__(self):
        return f'this is a restart case located at {self.dir}'

    # a method to instantiate a simulation trajectory
    def init_trajectory(self,t0):
        self.t0=t0
        self.traj=trajectory(self.simBox,self.t0,self.layers)


# a class for the simulation instance
class simulation():
    # class attributes
    SimOutputData=pd.DataFrame()

    SimOutputData['time']=[] 
    SimOutputData['num_unit_cells']=[] 
    SimOutputData['mass_hydrate']=[] 

    localPath=r'sliced_images\output_blacknwhite'

    # a private method to get the list of the restart cases
    def __GetRestartFoldersSorted(self):
        self.restarts=[]
        for item in os.scandir(self.workingDir):
            if item.is_dir():
                # find subdirectories
                path2slicesDir=os.path.join(item,self.localPath)
                subdirs=self.GetSubfolders(path2slicesDir)
                layers=[]
                for folder in subdirs:
                    layers.append(layer(os.path.join(path2slicesDir,folder),ImageCrystSettings.NumCrystPerLayer))
                
                self.restarts.append(restart(item,self.SimBox,layers)) # input the arbitrary t0=0 for t0
        
        # sort the restart cases based on the restart directory name
        self.restarts.sort(key=lambda x:x.dir.name, reverse=False)


    def __init__(self,workingDir,SimBox):
        self.workingDir=workingDir
        self.SimBox=SimBox


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
            restart.traj.detect_crystalls(ImageCrystSettings.numImagesSkipped)
            
            # set t0 for the next restart case
            t0=restart.traj.timer
            count+=1
    
    # an auxiliary method to return the directories living within a directory
    @staticmethod 
    def GetSubfolders(parentPath):
        try:
            return next(os.walk(parentPath))[1]
        except StopIteration:
            return []


    # collect and dump the output data
    def collectWriteOutputData(self):
        for restart in self.restarts:
            dictn = {'time':restart.traj.simTime_OutUnits,'num_unit_cells':restart.traj.numSiCrystals,'mass_hydrate':restart.traj.massSi}
            self.SimOutputData=self.SimOutputData.append(pd.DataFrame(dictn),ignore_index=True)

        self.SimOutputData.to_csv(os.path.join(self.workingDir,f'outputData_TstepsSkipped{ImageCrystSettings.numImagesSkipped}.csv'))
