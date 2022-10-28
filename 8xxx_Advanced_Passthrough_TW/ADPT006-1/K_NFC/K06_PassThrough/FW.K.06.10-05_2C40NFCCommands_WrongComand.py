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

C2C40Wrong = []
C2C40Wrong.append(["2C-40 Wrong command","2C 40 00","2C 05 00 00"])
C2C40Wrong.append(["2C-40 FF length","2C 40 FF","2C 05 00 00"])
C2C40Wrong.append(["2C-40 11 wrong length","2C 40 11 00","2C 05 00 00"])
C2C40Wrong.append(["2C-40 12 wrong length","2C 40 12","2C 05 00 00"])
C2C40Wrong.append(["2C-40 13 wrong length","2C 40 13","2C 05 00 00"])
C2C40Wrong.append(["2C-40 14 wrong length","2C 40 14 ","2C 05 00 00"])
C2C40Wrong.append(["2C-40 15 wrong length","2C 40 15","2C 05 00 00"])
C2C40Wrong.append(["2C-40 16 wrong length","2C 40 16","2C 05 00 00"])
C2C40Wrong.append(["2C-40 17 wrong length","2C 40 17","2C 05 00 00"])
C2C40Wrong.append(["2C-40 18 wrong length","2C 40 18","2C 05 00 00"])
C2C40Wrong.append(["2C-40 21 wrong length","2C 40 21","2C 05 00 00"])
C2C40Wrong.append(["2C-40 22 wrong length","2C 40 22","2C 05 00 00"])
C2C40Wrong.append(["2C-40 23 wrong length","2C 40 23","2C 05 00 00"])
C2C40Wrong.append(["2C-40 41 wrong length","2C 40 41","2C 05 00 00"])
C2C40Wrong.append(["2C-40 42 wrong length","2C 40 42","2C 05 00 00"])

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

#Operate tag4
for Case in C2C40Wrong:
	if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(Case[0],Case[1],5000,False,DL),Case[2],DL)): DL.fails = DL.fails +1

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