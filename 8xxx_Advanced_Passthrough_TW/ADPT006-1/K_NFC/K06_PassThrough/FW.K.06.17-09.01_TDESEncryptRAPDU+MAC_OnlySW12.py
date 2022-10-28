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

C2CX3 = []
C2CX3.append(["PSE ","2C 03 00 A4 04 00 0E 31 50 41 59 2E 53 59 53 2E 44 44 46 30 31 00  ","56 69 56 4F 74 65 63 68 32 00 2C00 0002 6A82"])
C2CX3.append(["PSE ","2C 13 00 00 A4 04 00 0E 31 50 41 59 2E 53 59 53 2E 44 44 46 30 31 00  ","56 69 56 4F 74 65 63 68 32 00 2C00 0002 6A82"])

CC733=[["Get Dukpt Encryption","C7 33","C7 00 00 01 00"]]
CC7A3 = [["Get DataKey Encrp Type","C7 a3 01 00"," C7 00 00 06 00 00"]]
C8140 = [["Get MAC Verification output","81 40 00","81 00 00 01 01"]]
C81401 = [["Set MAC Verification output on","81 40 01","81 00 00 00"]]
strKey = "0123456789ABCDEFFEDCBA9876543210"
CC78X = []
CC78X.append(["Get customer config","C7 83","C7 00 00 05 00 01 02 00 00"])
CC78X.append(["Set customer config-2","C7 82 0001 02 0000","C7 00 00 00"])

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

#TDES + MAC on + CustomerID2
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(CC7A3[0][0],CC7A3[0][1],30000,False,DL),CC7A3[0][2],DL) and False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(CC733[0][0],CC733[0][1],30000,False,DL),CC733[0][2],DL)): 
	Pro_PKI().MasterReset(DL)
	Pro_PKI().Activate(DL)
	if(False == Pro_PKI().EnsureActive(DL)):DL.warnings=DL.warnings+1
	else:
		Pro_KeyInjection().Run(5,DL)
if(False == Pro_SendCmd().RunCK(Pro_SendCmd().Run(C8140[0][0],C8140[0][1],30000,False,DL),C8140[0][2],DL)):
	if(False == Pro_SendCmd().RunCK(Pro_SendCmd().Run(C81401[0][0],C81401[0][1],30000,False,DL),C81401[0][2],DL)):DL.warnings=DL.warnings+1
if(False == Pro_SendCmd().RunCK(Pro_SendCmd().Run(CC78X[0][0],CC78X[0][1],30000,False,DL),CC78X[0][2],DL)):
	if(False == Pro_SendCmd().RunCK(Pro_SendCmd().Run(CC78X[1][0],CC78X[1][1],30000,False,DL),CC78X[1][2],DL)):DL.fails = DL.fails +1

if(Robot):
	DL.Robot_CTLSCard(2)
	DL.Robot_RemoveCard()

if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],5000,False,DL),C2C01[0][2],DL)):DL.fails = DL.fails + 1

if(Robot):DL.Robot_CTLSCard(2)
else:DL.ShowMessageBox("Poll Card", "Present MC21 card and ot move until the end",0)
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C02[0][0],C2C02[0][1],30000,False,DL),C2C02[0][2],DL)):DL.fails = DL.fails + 1
for case in C2CX3:
    strRes = Pro_SendCmd().Run(case[0],case[1],5000,False,DL)
    if(False ==  Pro_SendCmd().RunCK_C(strRes,case[2],DL)):DL.fails = DL.fails + 1
    #Pro_Encryption().DecRAPDU(strRes,strKey,0,1,True,True,case_2C03[3],DL)

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