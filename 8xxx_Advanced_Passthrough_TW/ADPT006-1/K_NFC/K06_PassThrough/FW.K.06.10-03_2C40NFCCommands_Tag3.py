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
Robot = DL.isRobot
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

C2C01 = []
C2C01.append(["PT Stop","2C 01 00","5669564F7465636832002C000000"])
C2C01.append(["PT Start","2C 01 01","5669564F7465636832002C0000001C9B"])

C2C40Tag3 = []
C2C40Tag3.append(["Poll tag 3","2C 40 FF 22","2C 00 00 09 0C"])
C2C40Tag3.append(["Tag3 Write Data","2C 40 42 01 09 00 01 80 08 31 32 33 34 35 36 37 38 31 32 33 34 35 36 37 38 ","2C 00 00 00 1C 9B"])
C2C40Tag3.append(["Tag3 Read Data","2C 40 41 01 09 00 01 80 08","2C 00 00 13 00 00 01 31 32 33 34 35 36 37 38 31 32 33 34 35 36 37 38 37 19"])
C2C40Tag3.append(["Tag3 Write NDEF - block0","2C 40 42 01 09 00 01 80 00 10 04 01 00 0D 00 00 00 00 00 01 00 00 11 00 34","2C 00 00 00 1C 9B"])
C2C40Tag3.append(["Tag3 Write NDEF - block1","2C 40 42 01 09 00 01 80 01 D1 01 0D 54 02 65 6E 68 65 6C 6C 6F 57 6F 72 6C ","2C 00 00 00 1C 9B"])
C2C40Tag3.append(["Tag3 Write NDEF - block2","2C 40 42 01 09 00 01 80 02 64 00 00 00 00 00 00 00 00 00 00 00 00 00 DA B2","2C 00 00 00 1C 9B"])
C2C40Tag3.append(["Tag3 Read NDEF - block0-2","2C 40 41 01 0B 00 03 80 00 80 01 80 02","2C 00 00 33 00 00 03 10 04 01 00 0D 00 00 00 00 00 01 00 00 11 00 34 D1 01 0D 54 02 65 6E 68 65 6C 6C 6F 57 6F 72 6C 64 00 00 00 00 00 00 00 00 00 00 00 00 00 DA B2 71 61"])

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

#Start Pass through
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[1][0],C2C01[1][1],50000,False,DL),C2C01[1][2],DL)): DL.warnings = DL.warnings +1

#Operate tag3
if(Robot == False):DL.ShowMessageBox("card","Please Tap tag3 card after clicking",0)
else: DL.Robot_SwipeorTapCard(24,0)
for Case in C2C40Tag3:
	if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(Case[0],Case[1],5000,False,DL),Case[2],DL)): DL.fails = DL.fails +1
if(Robot == True): DL.Robot_RemoveCard()

#Stop Pass through
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],50000,False,DL),C2C01[0][2],DL)): DL.warnings = DL.warnings +1

#Check device memory not change after script
if(10<DeviceType):
    if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C0930[0][0],C0930[0][1],5000,False,DL),strMemory,DL)): 
        DL.fails = DL.fails +1
        DL.setText("RED","Device memory changed after script")

##################################################

# Result Count ####################################
# Warning Count & Fail Count
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )

##################################################

#! Script END