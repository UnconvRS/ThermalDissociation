"""
a python module that holds the unit class
"""

class units:
    # get all conversion factors
    @staticmethod 
    def get_all_conversion_factors(conv_factors):
        # derive all other conversion factors
        new_conversions={}
        for key1,value1 in conv_factors.items():
            unit_parts1 = key1.split('2')
            reversed_key = '2'.join(reversed(unit_parts1))
            revresed_value=1/value1
            new_conversions[reversed_key]=revresed_value
            # find the other conversion factors
            for key2,value2 in conv_factors.items():
                if key2!=key1:
                    unit_parts2 = key2.split('2')
                    newKey = '2'.join([unit_parts1[1],unit_parts2[1]])
                    # calcluate the conversion factor
                    matchedKey=None 
                    conversion_factor=revresed_value
                    for key3,value3 in conv_factors.items():
                        if key3!=key1:
                            unit_parts3 = key3.split('2')
                            matchedKey='2'.join([unit_parts1[1],unit_parts3[1]])

                        if matchedKey == newKey:
                            conversion_factor*=value3
                            new_conversions[newKey]=conversion_factor
                            break

        conv_factors.update(new_conversions)

    # ... (rest of your class definition)
    _updatedConvFactors = False
    def update_convfactors(cls):
        if cls._updatedConvFactors:
            return
        cls.get_all_conversion_factors(cls.time_conversions)
        cls.get_all_conversion_factors(cls.length_conversions)

    #### preliminary conversion factors ####

    # preliminary time conversions
    time_conversions={
        "fs2ps":1e-3,       # femtosecond to picosecond
        "fs2ns":1e-6,       # femtosecond to nanosecond
        "fs2mics":1e-9,     # femtosecond to microsecond
        "fs2ms":1e-12,
        "fs2cs":1e-13,
        "fs2ds":1e-14,
        "fs2s":1e-15
        }

    # preliminary length conversions
    length_conversions={
        "A2nm":1e-1,     # Angstrom to nanometer
        "A2micron":1e-4, # Angstrom to micrometer (micron)
        "A2mm":1e-7,     # Angstrom to milimeter
        "A2cm":1e-8,     # Angstrom to centimeter
        "A2m":1e-10      # Angstrom to meter
        }

    def __init__(self,time,length):
        self.time=time
        self.length=length


if __name__=='main':
    myUnits=units('fs','A')
    pass
