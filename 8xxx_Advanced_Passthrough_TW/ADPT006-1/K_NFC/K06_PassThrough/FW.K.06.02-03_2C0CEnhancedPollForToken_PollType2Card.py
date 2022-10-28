#ID:

# Head #########################################
#LABLE:
#POURPOSE: 2C-0C poll different type of cards
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
C2C01.append(["PassThrough Stop","2C 01 00","2C 00"])
C2C01.append(["PassThrough On","2C 01 01","2C 00"])

C2C0C = []
C2C0C.append(["Tap typeB card after pressing pass","1F 00 00 01 ","56 69 56 4F 74 65 63 68 32 00 2C 00 00 ?? 02 ","ROBOT:CTLSCARD17"])
C2C0C.append(["Tap typeB card after pressing pass","1F 00 00 02 ","56 69 56 4F 74 65 63 68 32 00 2C 00 00 ?? 02 ","ROBOT:CTLSCARD17"])
C2C0C.append(["Tap typeB card after pressing pass","1F 00 00 03 ","56 69 56 4F 74 65 63 68 32 00 2C 00 00 ?? 02 ","ROBOT:CTLSCARD17"])

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

if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[1][0],C2C01[1][1],5000,False,DL),C2C01[1][2],DL)): DL.warnings = DL.warnings +1

for Case in C2C0C:
	if(False ==  Pro_SendCmd().RunCK(P4T_Type_3().Run(Case[0],1,Case[1],Case[3],Robot,30000,200,DL),Case[2],DL)):DL.fails = DL.fails + 1

if(False == Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],5000,False,DL),C2C01[0][2],DL)):DL.warnings = DL.warnings + 1

##################################################

# Result Count ####################################
# Warning Count & Fail Count
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )

##################################################

#! Script END