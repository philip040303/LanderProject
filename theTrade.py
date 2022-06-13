# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 20:28:56 2022

@author: plomb
"""

import numpy as np
import matplotlib.pyplot as plt
import Classes as cf
import ApogeeRaiseFunction as apf

##############################################
# The actual running portion of the code
#
#
##############################################     


# Run through sequence
rocketData  = np.genfromtxt('/Users/plomb/Downloads/RocketData.csv', delimiter=',', dtype='f8')
nDataPointsMass = 100

ispSweep    = [200,250,300,350,400]
mrSweep     = np.array([2.1])
mStart      = np.zeros((nDataPointsMass, np.size(ispSweep)))
mPayload    = np.zeros((nDataPointsMass, np.size(ispSweep)))
mDry        = np.zeros((nDataPointsMass, np.size(ispSweep)))
dv          = np.zeros((nDataPointsMass, np.size(ispSweep)))
twPhase     = np.zeros((nDataPointsMass, np.size(ispSweep)))
cost     = np.zeros((nDataPointsMass, np.size(ispSweep)))


mdotRCS     = 3 / 86400     # divide by seconds per day to get rate per second

config1 = cf.Configuration("rocket", 0, "fuel", "ox", 0, 0, "matTanks", 0, "typeArray", 0) #for top five configurations
config2 = cf.Configuration("rocket", 0, "fuel", "ox", 0, 0, "matTanks", 0, "typeArray", 0)
config3 = cf.Configuration("rocket", 0, "fuel", "ox", 0, 0, "matTanks", 0, "typeArray", 0)
config4 = cf.Configuration("rocket", 0, "fuel", "ox", 0, 0, "matTanks", 0, "typeArray", 0)
config5 = cf.Configuration("rocket", 0, "fuel", "ox", 0, 0, "matTanks", 0, "typeArray", 0)

maxPayload = 0

for jj, ispEngine in enumerate(ispSweep):   
    # The fifth column of rocketData (index 4) contains the rocket of interest
    mSeparated  = np.linspace(rocketData[-1,3], rocketData[0,3], nDataPointsMass)
    for ii, mLaunch in enumerate(mSeparated):
        thrusts = np.linspace(2000, 36000, 20)
        for kk, thrEngine in enumerate(thrusts):
            matTankList = ["Al2219", "Stainless", "Al-Li"]
            for mm, matTank in enumerate(matTankList):
                for nn, numTanks in enumerate([1,2,3]):
                    for tt, typeArray in enumerate(["Body","Deployable"]):
                    
                        # Interpolate the data from the datafile
                        apogeeOrbit = np.interp(mLaunch,rocketData[::-1,3],rocketData[::-1,0]) # the weird -1 reverses the order of the data since interp expects increasing values
                        
                               
                        
                        dvReq   = apf.ApogeeRaise(apogeeOrbit)
                        engMain = cf.Engine(ispEngine, thrEngine, 5.5, 'Biprop', 'Cryo')
                        engRCS  = cf.Engine(220, 448, 1, 'Monoprop', 'NotCryo')
                        
                        
                        if engMain.strCryo == 'Cryo':
                            # Include chill-in and boiloff only for cryogenic sequence
                            mdotOxBoiloff = 5/86400    # divide by seconds per day to get rate per second
                            mdotFuelBoiloff = 10/86400  # divide by seconds per day to get rate per second 
                            
                            PreTLISett  = cf.Phase('Pre-TCM1 Settling',        mLaunch,       0, engMain,'Settling',      0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            PreTLIChill = cf.Phase('Pre-TCM1 Chill',   PreTLISett.mEnd,       0, engMain, 'Chill',        0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            TLI         = cf.Phase('TLI',             PreTLIChill.mEnd,   dvReq, engMain,  'Burn',        0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            CoastToTCM1 = cf.Phase('Coast to TCM1',           TLI.mEnd,       0, engMain, 'Coast', 1*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            PreTCM1Sett = cf.Phase('Pre-TCM1 Settling',CoastToTCM1.mEnd,      0, engMain,'Settling',      0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            PreTCM1Chill= cf.Phase('Pre-TCM1 Chill',  PreTCM1Sett.mEnd,       0, engMain, 'Chill',       0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            TCM1        = cf.Phase('TCM1',           PreTCM1Chill.mEnd,      20, engMain,  'Burn',        0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            CoastToTCM2 = cf.Phase('Coast to TCM2',          TCM1.mEnd,       0, engMain, 'Coast', 2*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            TCM2        = cf.Phase('TCM2',            CoastToTCM2.mEnd,       5,  engRCS,  'Burn',       0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff) 
                            CoastToTCM3 = cf.Phase('Coast to TCM3',          TCM2.mEnd,       0, engMain, 'Coast', 1*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            TCM3        = cf.Phase('TCM3',            CoastToTCM3.mEnd,       5,  engRCS,  'Burn',        0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            CoastToLOI  = cf.Phase('Coast to LOI',           TCM3.mEnd,       0, engMain, 'Coast', 0.5*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            PreLOISett  = cf.Phase('Pre-LOI Settling', CoastToLOI.mEnd,       0, engMain,'Settling',      0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            PreLOIChill = cf.Phase('Pre-LOI Chill',    PreLOISett.mEnd,       0, engMain, 'Chill',       0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff) 
                            LOI         = cf.Phase('LOI',             PreLOIChill.mEnd,     850, engMain,  'Burn',       0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            CoastToTCM4 = cf.Phase('Coast to TCM4',           LOI.mEnd,       0, engMain, 'Coast', 0.5*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            TCM4        = cf.Phase('TCM4',            CoastToTCM4.mEnd,       5, engRCS,  'Burn',        0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            CoastToDOI  = cf.Phase('Coast to DOI',           TCM4.mEnd,       0, engMain, 'Coast', 0.5*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            PreDOISett  = cf.Phase('Pre-DOI Settling', CoastToDOI.mEnd,       0, engMain,'Settling',      0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            PreDOIChill = cf.Phase('Pre-DOI Chill',    PreDOISett.mEnd,       0, engMain, 'Chill',       0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff) 
                            DOI         = cf.Phase('DOI',             PreDOIChill.mEnd,      25, engMain, 'Burn',     0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            CoastToPDI  = cf.Phase('Coast to PDI',            DOI.mEnd,       0, engMain, 'Coast', 0.5*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            PrePDISett  = cf.Phase('Pre-PDI Settling', CoastToPDI.mEnd,       0, engMain,'Settling',      0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            PrePDIChill = cf.Phase('Pre-PDI Chill',    PrePDISett.mEnd,       0, engMain, 'Chill',       0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff) 
                            PDI         = cf.Phase('PDI',             PrePDIChill.mEnd,      -1, engMain,  'Burn',       0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                        
                            Sequence = [PreTLISett, PreTLIChill, TLI, CoastToTCM1, PreTCM1Sett, PreTCM1Chill, TCM1,CoastToTCM2, TCM2, CoastToTCM3, \
                            TCM3,CoastToLOI,PreLOISett, PreLOIChill, LOI, CoastToTCM4, TCM4,CoastToDOI, PreDOISett, PreDOIChill, DOI, CoastToPDI, \
                                PrePDISett, PrePDIChill, PDI]
                        
                        else:
                            # This is not a cryogenic engine, so we don't need chill-in or boiloff
                            mdotOxBoiloff   = 0    # divide by seconds per day to get rate per second
                            mdotFuelBoiloff = 0  # divide by seconds per day to get rate per second 
                            
                            PreTLISett  = cf.Phase('Pre-TCM1 Settling',        mLaunch,       0, engMain,'Settling',      0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            TLI         = cf.Phase('TLI',              PreTLISett.mEnd,   dvReq, engMain,  'Burn',        0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            CoastToTCM1 = cf.Phase('Coast to TCM1',           TLI.mEnd,       0, engMain, 'Coast', 1*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            PreTCM1Sett = cf.Phase('Pre-TCM1 Settling',CoastToTCM1.mEnd,      0, engMain,'Settling',      0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            TCM1        = cf.Phase('TCM1',           PreTCM1Sett.mEnd,      20, engMain,  'Burn',        0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            CoastToTCM2 = cf.Phase('Coast to TCM2',          TCM1.mEnd,       0, engMain, 'Coast', 2*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            TCM2        = cf.Phase('TCM2',            CoastToTCM2.mEnd,       5,  engRCS,  'Burn',       0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff) 
                            CoastToTCM3 = cf.Phase('Coast to TCM3',          TCM2.mEnd,       0, engMain, 'Coast', 1*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            TCM3        = cf.Phase('TCM3',            CoastToTCM3.mEnd,       5,  engRCS,  'Burn',        0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            CoastToLOI  = cf.Phase('Coast to LOI',           TCM3.mEnd,       0, engMain, 'Coast', 0.5*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            PreLOISett  = cf.Phase('Pre-LOI Settling', CoastToLOI.mEnd,       0, engMain,'Settling',      0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            LOI         = cf.Phase('LOI',              PreLOISett.mEnd,     850, engMain,  'Burn',       0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            CoastToTCM4 = cf.Phase('Coast to TCM4',           LOI.mEnd,       0, engMain, 'Coast', 0.5*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            TCM4        = cf.Phase('TCM4',            CoastToTCM4.mEnd,       5, engRCS,  'Burn',        0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            CoastToDOI  = cf.Phase('Coast to DOI',           TCM4.mEnd,       0, engMain, 'Coast', 0.5*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            PreDOISett  = cf.Phase('Pre-DOI Settling', CoastToDOI.mEnd,       0, engMain,'Settling',      0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            DOI         = cf.Phase('DOI',             PreDOISett.mEnd,      25, engMain, 'Burn',     0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            CoastToPDI  = cf.Phase('Coast to PDI',            DOI.mEnd,       0, engMain, 'Coast', 0.5*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            PrePDISett  = cf.Phase('Pre-PDI Settling', CoastToPDI.mEnd,       0, engMain,'Settling',      0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            PDI         = cf.Phase('PDI',              PrePDISett.mEnd,      -1, engMain,  'Burn',       0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
                            
                            Sequence = [PreTLISett, TLI, CoastToTCM1, PreTCM1Sett, TCM1,CoastToTCM2, TCM2, CoastToTCM3, \
                            TCM3,CoastToLOI,PreLOISett,LOI,CoastToTCM4, TCM4,CoastToDOI, PreDOISett, DOI, CoastToPDI, \
                                PrePDISett, PDI]
                        
                        # Create the Misison Summary and calculate subsystem masses with payload 
                        Mission = cf.MissionSummary(Sequence)
                        
                        # Check tanks based on Isp (since each value is a different propellant
                        if ispEngine==340: #storable
                            OxTanks = cf.TankSet("NTO", matTank, numTanks, 1, 300000, Mission.mPropTotalOx)
                            FuelTanks = cf.TankSet("MMH", matTank, numTanks, 2, 300000, Mission.mPropTotalFuel)
                        elif ispEngine==345: # LOX/RP1
                            OxTanks = cf.TankSet("Oxygen", matTank, numTanks, 1, 300000, Mission.mPropTotalOx)
                            FuelTanks = cf.TankSet("RP-1", matTank, numTanks, 2, 300000, Mission.mPropTotalFuel)   
                        elif ispEngine==370: # LOX/Methane
                            OxTanks = cf.TankSet("Oxygen", matTank, numTanks, 1, 300000, Mission.mPropTotalOx)
                            FuelTanks = cf.TankSet("Methane", matTank, numTanks, 2, 300000, Mission.mPropTotalFuel)  
                        else:
                            OxTanks = cf.TankSet("Oxygen", matTank, numTanks, 1, 300000, Mission.mPropTotalOx)
                            FuelTanks = cf.TankSet("Hydrogen", matTank, numTanks, 2, 300000, Mission.mPropTotalFuel)  
                        
                        # Calculate monopropellant tank size
                        MonoTanks = cf.TankSet("MMH", matTank, 1, 2, 300000, Mission.mPropTotalMono)    
                        subs = cf.Subsystems(mLaunch, engMain, OxTanks, FuelTanks, MonoTanks, 100, typeArray, 'Large', 8)
                        
                        # Determine payload
                        payload = mLaunch - Mission.mPropTotalTotal - subs.mTotalAllowable
                        
                        # Determine Cost
                        costObject = cf.Cost(mLaunch-Mission.mPropTotalTotal, engMain.thrust, 60)
                        cost[ii,jj] = costObject.costNRETotal
                        
                        if payload > maxPayload:
                            maxPayload = payload
                            config5 = config4
                            config4 = config3
                            config3 = config2
                            config2 = config1
                            config1 = cf.Configuration("rocket", mLaunch, FuelTanks.strPropType, OxTanks.strPropType, ispEngine, thrEngine, OxTanks.strMatType, numTanks, typeArray, cost)
                        
print(maxPayload)