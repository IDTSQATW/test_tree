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
C2801 = []
C2801.append(["AntennaEnable","28 01 01","28 00 00 00"])
C2801.append(["AntennaDisable","28 01 00","28 00 00 00","28 0C 00 00"])
C2C02 = [["Place Mifare PlusX card, not move until the end","1F 00","5669564F7465636832002C00"]]


C2C06 = []
C2C06.append([" mfpx - authen block 1 w/ 2c-06","2C 06 01 01 FF FF FF FF FF FF","5669564F7465636832002C0000001C9B"])

C2C08 = []
C2C08.append(["mfpx - write 00-FFh","2C 08 C1 01 00 11 22 33 44 55 66 77 88 99 AA BB CC DD EE FF","5669564F7465636832002C0000001C9B"])
C2C08.append(["mfpx - write 00h","2C 08 C1 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00","5669564F7465636832002C0000001C9B"])

C2C07 = []
C2C07.append(["mfpx - read block 00-FF","2C 07 C1 01","5669564F7465636832002C00001000112233445566778899AABBCCDDEEFF60EC"])
C2C07.append(["mfpx - read block 00","2C 07 C1 01","5669564F7465636832002C0000100000000000000000000000000000000072A4"])

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

RobotAction = "ROBOT:CTLSCARD5"

if(10<DeviceType):
	strMemory = Pro_SendCmd().Run(C0930[0][0],C0930[0][1],5000,False,DL)
	strMemory = strMemory.replace(" ","")
	strMemory = strMemory[0:len(strMemory)-12]

    
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],5000,False,DL),C2C01[0][2],DL)): DL.warnings = DL.warnings +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2801[0][0],C2801[0][1],5000,False,DL),C2801[0][2],DL)): DL.warnings = DL.warnings +1


strResponse = P4T_Type_1().Run(C2C02[0][0],1,C2C02[0][1],RobotAction,Robot,30000,200,DL)
if(False==DL.Check_RXResponse(0,str(C2C02[0][2]))):DL.fails = DL.fails + 1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C06[0][0],C2C06[0][1],5000,False,DL),C2C06[0][2],DL)): DL.fails = DL.fails +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C08[0][0],C2C08[0][1],5000,False,DL),C2C08[0][2],DL)): DL.fails = DL.fails +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C07[0][0],C2C07[0][1],5000,False,DL),C2C07[0][2],DL)): DL.fails = DL.fails +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C08[1][0],C2C08[1][1],5000,False,DL),C2C08[1][2],DL)): DL.fails = DL.fails +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C07[1][0],C2C07[1][1],5000,False,DL),C2C07[1][2],DL)): DL.fails = DL.fails +1

#Remove card + stop PT
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