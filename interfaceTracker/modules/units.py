"""
a python module that holds the unit class
"""



class units:
    #### conversion factors ####

    # temporal units
    fs2ps=1e-3 # femtosecond to picosecond
    fs2ns=1e-6 # femtosecond to nanosecond
    fs2ms=1e-9 # femtosecond to microsecond

    # Spatial units
    A2nm=1e-1         # Angstrom to nanometer
    A2micron=1e-4     # Angstrom to micrometer (micron)
    A2mm=1e-7         # Angstrom to milimeter
    A2cm=1e-8         # Angstrom to centimeter
    A2m=1e-10         # Angstrom to meter

    def __init__(self,time,length):
        self.time=time
        self.length=length

