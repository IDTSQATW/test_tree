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

C2C02 = [["Place UltraLight card, not move until the end","1F 00","56 69 56 4F 74 65 63 68 32 00 2C 00 00 08 04"]]

C2C07 = []
C2C07.append(["ReadBlockO","2C 07 41 00","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock1","2C 07 41 01","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock2","2C 07 41 02","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock3","2C 07 41 03","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock4","2C 07 41 04","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock5","2C 07 41 05","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock6","2C 07 41 06","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock7","2C 07 41 07","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock8","2C 07 41 08","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock9","2C 07 41 09","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock10","2C 07 41 0A","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock11","2C 07 41 0B","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock12","2C 07 41 0C","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock13","2C 07 41 0D","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock14","2C 07 41 0E","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock15","2C 07 41 0F","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock16","2C 07 41 10","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock17","2C 07 41 11","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock18","2C 07 41 12","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock19","2C 07 41 13","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock20","2C 07 41 14","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock21","2C 07 41 15","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock22","2C 07 41 16","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock23","2C 07 41 17","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock24","2C 07 41 18","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock25","2C 07 41 19","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock26","2C 07 41 1A","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock27","2C 07 41 1B","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock28","2C 07 41 1C","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock29","2C 07 41 1D","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock30","2C 07 41 1E","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock31","2C 07 41 1F","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock32","2C 07 41 20","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock33","2C 07 41 21","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock34","2C 07 41 22","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock35","2C 07 41 23","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock36","2C 07 41 24","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock37","2C 07 41 25","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock38","2C 07 41 26","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])
C2C07.append(["ReadBlock39","2C 07 41 27","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10"])

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
RobotAction = "ROBOT:CTLSCARD14"

#Start PT
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],5000,False,DL),C2C01[0][2],DL)): DL.warnings = DL.warnings +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[1][0],C2C01[1][1],5000,False,DL),C2C01[1][2],DL)): DL.warnings = DL.warnings +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2801[1][0],C2801[1][1],5000,False,DL),C2801[1][3],DL)): DL.fails = DL.fails +1
if(10<DeviceType):
	strMemory = Pro_SendCmd().Run(C0930[0][0],C0930[0][1],5000,False,DL)
	strMemory = strMemory.replace(" ","")
	strMemory = strMemory[0:len(strMemory)-12]
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],5000,False,DL),C2C01[0][2],DL)): DL.warnings = DL.warnings +1

#Poll Ultra card + read all
strResponse = P4T_Type_1().Run(C2C02[0][0],1,C2C02[0][1],RobotAction,Robot,30000,200,DL)
if(False==DL.Check_RXResponse(0,str(C2C02[0][2]))):DL.fails = DL.fails + 1

for Case in C2C07:
	if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(Case[0],Case[1],5000,False,DL),Case[2],DL)): DL.fails = DL.fails +1

#Remove card + Stop PT
if(Robot == True):  DL.Robot_RemoveCard()
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[1][0],C2C01[1][1],5000,False,DL),C2C01[1][2],DL)): DL.warnings = DL.warnings +1

#Check device memory not change after script
if(10<DeviceType):
	time.sleep(2)
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