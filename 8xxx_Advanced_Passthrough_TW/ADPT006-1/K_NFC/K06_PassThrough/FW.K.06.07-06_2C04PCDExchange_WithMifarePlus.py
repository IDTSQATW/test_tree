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
C2C01.append(["PT Stop","2C 01 00","2C ?? 00 00"])

C2C02 = [["Place Mifare PlusX card, not move until the end","1F 00","5669564F7465636832002C0000"]]

C2C04 = []
C2C04.append(["mfpx - pcd loadkey","2C 04 19 00 00 29 86 03 03 0F 0F 0F 0F 0F 0F 0F 0F 0F 0F 0F 0F","56 69 56 4F 74 65 63 68 32 00 2C 00 00 05 00 00 00 00 00 14 F0"])
C2C04.append(["mfpx - pcd authn block 0","2C 04 0C 00 00 29 86 03 07 60 00","56 69 56 4F 74 65 63 68 32 00 2C 00 00 05 00 00 00 00 00 14 F0"])
C2C04.append([ "mfpx - write block 1","2C 04 1E 00 00 29 86 00 07 A0 01 ","56 69 56 4F 74 65 63 68 32 00 2C 00 00 06 00 00 00 00 08 0A 52 D4"])
C2C04.append(["mfpx - write 00-FFh block 1","2C 04 1E 00 00 29 86 00 07 00 11 22 33 44 55 66 77 88 99 AA BB CC DD EE FF","56 69 56 4F 74 65 63 68 32 00 2C 00 00 06 00 00 00 00 08 0A 52 D4"])
C2C04.append(["mfpx - read block 1","2C 04 1E 00 00 29 86 03 0F 30 01 ","56 69 56 4F 74 65 63 68 32 00 2C 00 00 15 00 00 00 00 80 00 11 22 33 44 55 66 77 88 99 AA BB CC DD EE FF 51 5B"])
C2C04.append(["mfpx - set write block 1","2C 04 1E 00 00 29 86 00 07 A0 01","56 69 56 4F 74 65 63 68 32 00 2C 00 00 06 00 00 00 00 08 0A 52 D4 "])
C2C04.append(["mfpx - write 00h block 1","2C 04 1E 00 00 29 86 00 07 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00","56 69 56 4F 74 65 63 68 32 00 2C 00 00 06 00 00 00 00 08 0A 52 D4"])
C2C04.append(["mfpx - read block 1","2C 04 1E 00 00 29 86 03 0F 30 01","56 69 56 4F 74 65 63 68 32 00 2C 00 00 15 00 00 00 00 80 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 43 13 "])

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

RobotAction = "ROBOT:CTLSCARD5"

if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],5000,False,DL),C2C01[0][2],DL)): DL.warnings = DL.warnings +1

strResponse = P4T_Type_1().Run(C2C02[0][0],1,C2C02[0][1],RobotAction,Robot,30000,200,DL)
if(False == Pro_SendCmd().RunCK(strResponse,str(C2C02[0][2]),DL)):DL.fails = DL.fails + 1
strResponse = DL.Get_RXResponse(0)
strResponse = strResponse.replace(" ", "")
strUID = strResponse[len(strResponse)-12:len(strResponse)-4]

Index=0
while (Index < 8):
    if (Index == 1):
        if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run_3(C2C04[Index][0],C2C04[Index][1],strUID,5000,False,DL),C2C04[Index][2],DL)): DL.fails = DL.fails +1
        Index=Index+1
    else:
        if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C04[Index][0],C2C04[Index][1],5000,False,DL),C2C04[Index][2],DL)): DL.fails = DL.fails +1
        Index=Index+1

if(Robot == True):  DL.Robot_RemoveCard()
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