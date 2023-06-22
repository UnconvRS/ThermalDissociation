"""
a python module for the simulation settings
"""


# a singleton class to hold the specific crystal/image information
class simSettings:
    __instance=None

    def __init__(self,numImagesSkipped,NumCrystPerLayer,DynamicData,SimUnits,OutUnits):
        if simSettings.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.numImagesSkipped=numImagesSkipped
            self.NumCrystPerLayer=NumCrystPerLayer
            self.temporal=DynamicData
            self.SimUnits=SimUnits
            self.OutUnits=OutUnits
            simSettings.__instance = self

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = simSettings()
        return cls.__instance

    # modify the setting parameters after being initialized
    def set_settings(self, numImagesSkipped, NumCrystPerLayer, DynamicData, SimUnits, OutUnits):
        self.numImagesSkipped = numImagesSkipped
        self.NumCrystPerLayer = NumCrystPerLayer
        self.temporal = DynamicData
        self.SimUnits = SimUnits
        self.OutUnits = OutUnits


