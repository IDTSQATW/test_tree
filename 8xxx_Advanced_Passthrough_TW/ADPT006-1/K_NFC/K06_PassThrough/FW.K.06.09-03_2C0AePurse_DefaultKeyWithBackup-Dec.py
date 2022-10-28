#ID:

# Head #########################################
#LABLE:
#POURPOSE:
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
C2C01.append(["PT Start","2C 01 01","2C 00 00 00"])
C2C01.append(["PT Stop","2C 01 00","2C ?? 00 00"])

CInit = []
CInit.append(["poll for token","2C 02 1F 00","56 69 56 4F 74 65 63 68 32 00 2C 00 00 05 03"])
CInit.append(["Auth with default key","2C 06 01 01 FF FF FF FF FF FF","2C000000"])
CInit.append(["Initialize Blocks","2C 08 33 10 87 19 00 00 78 E6 FF FF 87 19 00 00 00 FF 00 FF B7 1A 00 00 48 E5 FF FF B7 1A 00 00 00 FF 00 FF 88 19 00 00 77 E6 FF FF 88 19 00 00 00 FF 00 FF","5669564F7465636832002C0000001C9B"])
CInit.append(["Read 3 Initialized Blocks","2C 07 33 10","5669564F7465636832002C0000308719000078E6FFFF8719000000FF00FFB71A000048E5FFFFB71A000000FF00FF8819000077E6FFFF8819000000FF00FF4CD2"])

CePurse = []
CePurse.append(["poll for token","2C 02 1F 00","56 69 56 4F 74 65 63 68 32 00 2C 00 00 05 03"])
CePurse.append(["Decrement Block *Original - minus 1 @ block 16 with BACKUP","2C 0A 32 10 04 01 00 00 00 12 01 10","5669564F7465636832002C0000001C9B"])
CePurse.append(["Read 3 Blocks - DECed","2C 07 33 10","5669564F7465636832002C0000308619000079E6FFFF8619000000FF00FFB71A000048E5FFFFB71A000000FF00FF8619000079E6FFFF8619000000FF00FF50C2"])

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

if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],5000,False,DL),C2C01[0][2],DL)): DL.warnings = DL.warnings +1
if(Robot == False):	DL.ShowMessageBox("card","Please Tap S70 card after clicking",0)
else:DL.Robot_CTLSCard(20,1)
for Case in CInit:
	if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(Case[0],Case[1],5000,False,DL),Case[2],DL)): DL.warnings = DL.warnings +1

if(Robot == False):	DL.ShowMessageBox("card","Please Remove then ReTap S70 card",0)
else: 
	DL.Robot_RemoveCard()
	DL.Robot_CTLSCard(20,1)
for Case in CePurse:
	if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(Case[0],Case[1],5000,False,DL),Case[2],DL)): DL.fails = DL.fails +1

if(Robot == True):  DL.Robot_RemoveCard()
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[1][0],C2C01[1][1],5000,False,DL),C2C01[1][2],DL)): DL.warnings = DL.warnings +1

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