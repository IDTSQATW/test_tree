#ID:

# Head #########################################
#LABLE:
#POURPOSE:
#INPUT: 
#OUTPUT: 
#################################################

#!/usr/bin/env python

# Import #######################################
import Utility_Lib.Pro_PreFile

from  Utility_Lib.Pro_PreFile import *
#################################################

# Variable #####################################
Robot =  DL.isRobot
# true - robot, false - manual
InitPKI = True
# true - MasterReset + Activate + Key Injection, false skip
DeviceType = -1
# 0 - Vivo K3,K4, > 0 - Neoii
DL.warnings = 0 
# Ready for DVT Warning Count
DL.fails = 0
 # Test Part Issue Count
Index = 0
# Child Cases Index

if (DL.isRobot==True):
	DL.setText("RED","Please run manually")
 	DL.pyresult = DL.RUN_AUTO_NOT_SUPPORT
 	sys.exit()
	
C2C01 = [["Passthrough Enable","2C0101","2C00"],["Passthrough Disable","2C0100","2C00"]]

C2C09=[]
C2C09.append(["High Level Halt Command - typeA","2C 09 01","2C 00 00 00"])
C2C09.append(["High Level Halt Command - typeB","2C 09 02","2C 06 00 00"])

C2C02 = []
C2C02.append(["Poll card","2C 02 1E 00","2C 00"])

C0930 = [["Get device memory","09 30"]]

##################################################


# Ready for DVT ##################################
DeviceType = Pro_GetDevice().Run(DL)
if(-1==DeviceType):
	DL.warnings = 1
	DL.setText("RED","Please define device type in Pro_GetDevice")
if(0<DeviceType and 10>=DeviceType):DL.setText("BLACK", "<Kiosk>")
if(10<DeviceType):DL.setText("BLACK", "<NEOII>")
##################################################


# Test Part ######################################

if(10<DeviceType):
	strMemory = Pro_SendCmd().Run(C0930[0][0],C0930[0][1],5000,False,DL)
	strMemory = strMemory.replace(" ","")
	strMemory = strMemory[0:len(strMemory)-12]
    
if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],3000,False,DL),C2C01[0][2],DL)):DL.warnings = DL.warnings +1

DL.ShowMessageBox("Message","Please tap a type A CTLS cardr",0)
if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C02[0][0],C2C02[0][1],30000,False,DL),C2C02[0][2],DL)):DL.fails = DL.fails +1
DL.ShowMessageBox("Message","Please use SmartSpy record acquisition",0)
Ans = False
while (Ans == False):
    if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C09[0][0],C2C09[0][1],3000,False,DL),C2C09[0][2],DL)):DL.fails = DL.fails +1
    Ans = DL.ShowMessageBox("Message","Log recorded successfully? If not, click no and try again",0)
if (False == DL.ShowMessageBox("Message","Spy log contain HLTA? Resatrt recording before clicking",0)):DL.fails = DL.fails +1
if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C09[1][0],C2C09[1][1],3000,False,DL),C2C09[1][2],DL)):DL.fails = DL.fails +1
if (False == DL.ShowMessageBox("Message","Spy log contain nothing?",0)):DL.fails = DL.fails +1

if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[1][0],C2C01[1][1],30000,False,DL),C2C01[1][2],DL)):DL.warnings = DL.warnings +1

#Check device memory not change after script
if(10<DeviceType):
    if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C0930[0][0],C0930[0][1],5000,False,DL),strMemory,DL)): 
        DL.fails = DL.fails +1
        DL.setText("RED","Device memory changed after script")

# Result Count ####################################
# Warning Count & Fail Count
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )

##################################################

#! Script END