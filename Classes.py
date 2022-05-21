
import numpy as np



def PrintData(phaseList):
    print('{0:25s}'.format("-----------------------------------------------------------------------------------------" ))
    print('{0:20s}{1:>11s}{2:>11s}{3:>11s}{4:>13s}{5:>13s}{6:>14s}'.format("Phase Name", "DV (m/s)", "Mass0 (kg)", "MassF (kg)", "TotProp (kg)", "OxProp (kg)", "FuelProp (kg)"  ))
    print('{0:25s}'.format("-----------------------------------------------------------------------------------------" ))
    for curPhase in phaseList:
        print('{0:20s}{1:11.1f}{2:11.1f}{3:11.1f}{4:13.1f}{5:13.1f}{6:14.1f}'.format(curPhase.strName, curPhase.dvPhase, curPhase.mStart, curPhase.mEnd, curPhase.mPropImpulse, curPhase.mPropImpulseOx, curPhase.mPropImpulseFuel ))

class Phase:

    def __init__(self,strName, mStart, dvPhase, clsEng):

        # Check if this is a T/W phase. If so, 
        # update the dV calculate the thrust-to-weight
        twPhase = clsEng.thrust/(mStart*9.81)
        if dvPhase<0:
            dvPhase = 4335*np.exp(-(twPhase)*20.25)+1880


        # Calculate Impulse Propellant Using Rocket Equation   
        mPropImpulse = 

   
        # Determine Oxidizer and Fuel
        mPropImpulseOx = 
        mPropImpulseFuel = mPropImpulse/(1+clsEng.mr)
        
          
        mEnd = 
        
        
        # Move data to class structure to save information
        self.mStart         = mStart
        self.mEnd           = mEnd
        self.dvPhase        = 
        self.clsEng         = 
        self.mPropImpulse   = 
        self.strName        = 
        self.twPhase        = 

        self.mPropImpulse   = 
        self.mPropImpulseOx = 
        self.mPropImpulseFuel = 
          
class MissionSummary:
    def __init__(self, tupPhases):
        """
        Inputs:
            tupPhases: list of phase classes
        
        """

   
        
        mPropImpulse     = 0
        mPropImpulseOx   = 
        mPropImpulseFuel = 

        # sum up the usages by phase
        for curPhase in tupPhases:
            mPropImpulse     += curPhase.mPropImpulse 
            mPropImpulseOx   += 
            mPropImpulseFuel += 

        # Stuff everything into self    
        self.mPropImpulse      = 
        self.mPropImpulseOx    = 
        self.mPropImpulseFuel  = mPropImpulseFuel



class Engine:
    def __init__(self,isp, thrust, mr):
        self.isp = 
        self.thrust = 
        self.mr =