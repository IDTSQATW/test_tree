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
C2C01.append(["PT Start","2C 01 01","2C 00 00 00"])
C2C01.append(["PT Stop","2C 01 00","2C 00 00 00"])

C2C02 = []
C2C02.append(["P4T","2C 02 1F 00","56 69 56 4F 74 65 63 68 32 00 2C 00 00 05 03"])

C2C04 = []
C2C04.append(["PCDLoadKey","2C 04 19 00 00 29 68 01 0F 0F 0F 0F 0F 0F 0F 0F 0F 0F 0F 0F 0F","56 69 56 4F 74 65 63 68 32 00 2C 00 00 05 00 00 00 00 00 14 F0"])
C2C04.append(["PCD Auth Sector 1","2C 04 0C 00 00 29 68 01 0F 60 07","56 69 56 4F 74 65 63 68 32 00 2C 00 00 05 00 00 00 00 00 14 F0"])

CN2C04 = []
CN2C04.append(["PCDReadBlock0","2C 04 1E 00 00 29 68 01 0F 30 00 ","56 69 56 4F 74 65 63 68 32 00 2C 0A 00 06 EA 00 00 00 08 04"])
CN2C04.append(["PCDReadBlock1","2C 04 1E 00 00 29 68 01 0F 30 01 ","56 69 56 4F 74 65 63 68 32 00 2C 08 00 05 E5 00 00 00 00 12 71"])
CN2C04.append(["PCDReadBlock2","2C 04 1E 00 00 29 68 01 0F 30 02 ","56 69 56 4F 74 65 63 68 32 00 2C 08 00 05 E5 00 00 00 00 12 71"])
CN2C04.append(["PCDReadBlock3","2C 04 1E 00 00 29 68 01 0F 30 03 ","56 69 56 4F 74 65 63 68 32 00 2C 08 00 05 E5 00 00 00 00 12 71"])

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

if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],5000,False,DL),C2C01[0][2],DL)): DL.warnings = DL.warnings +1

if(Robot == False):DL.ShowMessageBox("card","Please Tap S50/S70 card after clicking",0)
else: DL.Robot_CTLSCard(20)
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C02[0][0],C2C02[0][1],35000,False,DL),C2C02[0][2][0],DL)): DL.fails = DL.fails +1
strResponse = DL.Get_RXResponse(0)
strResponse = strResponse.replace(" ", "")
strUID = strResponse[30:len(strResponse) - 4]
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C04[0][0],C2C04[0][1],5000,False,DL),C2C04[0][2],DL)): DL.fails = DL.fails +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run_3(C2C04[1][0],C2C04[1][1],strUID,5000,False,DL),C2C04[1][2],DL)): DL.fails = DL.fails +1
for case in CN2C04:
    if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(case[0],case[1],5000,False,DL),case[2],DL)): DL.fails = DL.fails +1
if(Robot == True): DL.Robot_RemoveCard()

if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[1][0],C2C01[1][1],5000,False,DL),C2C01[1][2],DL)): DL.warnings = DL.warnings +1

##################################################

# Result Count ####################################
# Warning Count & Fail Count
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )

##################################################

#! Script END