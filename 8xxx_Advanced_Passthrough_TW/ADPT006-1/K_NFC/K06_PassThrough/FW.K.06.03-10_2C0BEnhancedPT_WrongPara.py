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
C2C01.append(["PassThrough Stop","2C 01 00","2C 00"])
C2C01.append(["PassThrough On","2C 01 01","2C 00"])

C2C0B = []
C2C0B.append(["Activate Interface + Deactivate Interface","2C 0B 03 00 00 00 00 00 00","56 69 56 4F 74 65 63 68 32 00 2C 05"])
C2C0B.append(["Deactivate Interface + Poll For Token","2C 0B 06 00 00 00 00 00 00","56 69 56 4F 74 65 63 68 32 00 2C 05"])
C2C0B.append(["Poll For Token + invalid interface","2C 0B 25 00 00 00 00 0A 00 01","56 69 56 4F 74 65 63 68 32 00 2C 05"])

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

for Case in C2C0B:
    if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(Case[0],Case[1],5000,False,DL),Case[2],DL)):DL.fails = DL.fails + 1

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