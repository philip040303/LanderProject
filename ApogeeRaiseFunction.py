import numpy as np

def ApogeeRaise(apogeeStart):
    # this function takes in an apogee and calculates the dV 
    # necessary to raise the orbit to 410,000 km 
    
    # the input value is assumed to be an altitude, so this function
    # adjusts it by the radius of the earth when doing calculations
    mu = 398600
    apogeeEnd = 410000
    rEarth = 6378
    rStart = rEarth+185
    aStart = (185+rEarth + apogeeStart+rEarth)/2
    aEnd   = (185+rEarth + apogeeEnd+rEarth)/2
        
    vStart = np.sqrt(mu*((2/rStart) - (1/aStart)))
    vEnd   = np.sqrt(mu*((2/rStart) - (1/aEnd)))
    dv     = vEnd-vStart
       
    return dv*1000 # multiply by 1000 to put in m/s
