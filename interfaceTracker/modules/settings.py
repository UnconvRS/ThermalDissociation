"""
a python module for the simulation settings
"""


# a singleton class to hold the specific crystal/image information
class ImageCrystSettings:
    __instance=None

    def __init__(self,numImagesSkipped,NumCrystPerLayer):
        if ImageCrystSettings.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.numImagesSkipped=numImagesSkipped
            self.NumCrystPerLayer=NumCrystPerLayer
            ImageCrystSettings.__instance = self

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = ImageCrystSettings()
        return cls.__instance

