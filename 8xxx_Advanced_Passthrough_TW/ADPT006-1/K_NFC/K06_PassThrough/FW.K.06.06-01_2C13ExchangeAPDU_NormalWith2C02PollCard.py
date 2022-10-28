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
InitPKI = False
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
C2C01.append(["PassThrough Start","2C 01 01","2C 00 00 00"])
C2C01.append(["PassThrough Stop","2C 01 00","2C 00 00 00"])

C2C02 = []
C2C02.append(["Poll for token","2C 02 1E 00 ","56 69 56 4F 74 65 63 68 32 00 2C 00 00 05 07"])

C2C13 = []
C2C13.append(["PPSE ","2C 13 00 00 A4 04 00 0E 32 50 41 59 2E 53 59 53 2E 44 44 46 30 31 00  ","56 69 56 4F 74 65 63 68 32 00 2C 00","56 69 56 4F 74 65 63 68 32 00 2C 00 00 27 6F 23 84 0E 32 50 41 59 2E 53 59 53 2E 44 44 46 30 31 A5 11 BF 0C 0E 61 0C 4F 07 A0 00 00 00 04 10 10 87 01 01 90 00 8E B6"])
C2C13.append(["Select ","2C 13 00 00 A4 04 00 07 A0 00 00 00 04 10 10 00 ","56 69 56 4F 74 65 63 68 32 00 2C 00 ","56 69 56 4F 74 65 63 68 32 00 2C 00 00 20 6F 1C 84 07 A0 00 00 00 04 10 10 A5 11 50 0F 50 50 43 20 4D 43 44 20 30 31 20 20 76 32 30 90 00 45 09"])
C2C13.append(["GPO ","2C 13 00 80 A8 00 00 02 83 00 00 ","56 69 56 4F 74 65 63 68 32 00 2C 00","56 69 56 4F 74 65 63 68 32 00 2C 00 00 1A 77 16 82 02 59 80 94 10 08 01 01 00 10 01 01 01 18 01 02 00 20 01 02 00 90 00 0E 13"])
C2C13.append(["Read Record ","2C 13 00 00 B2 01 0C 00 ","56 69 56 4F 74 65 63 68 32 00 2C 00 ","56 69 56 4F 74 65 63 68 32 00 2C 06 00 00"])
C2C13.append(["CCC","2C 13 00 80 2A 8E 80 04 00 00 00 00 00","56 69 56 4F 74 65 63 68 32 00 2C 00 ","56 69 56 4F 74 65 63 68 32 00 2C 06 00 00"])

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

if(Robot):
	DL.Robot_CTLSCard(2)
	DL.Robot_RemoveCard()

if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],5000,False,DL),C2C01[0][2],DL)):DL.fails = DL.fails + 1

if(Robot):DL.Robot_CTLSCard(2)
else:DL.ShowMessageBox("Poll Card", "Present MC21 card and ot move until the end",0)
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C02[0][0],C2C02[0][1],30000,False,DL),C2C02[0][2],DL)):DL.fails = DL.fails + 1
for case in C2C13:
    if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(case[0],case[1],5000,False,DL),case[3],DL)):DL.fails = DL.fails + 1
if(Robot):DL.Robot_RemoveCard()

if(False == Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[1][0],C2C01[1][1],30000,False,DL),C2C01[1][2],DL)):DL.fails = DL.fails + 1

##################################################


# Result Count ####################################
# Warning Count & Fail Count
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )

##################################################

#! Script END