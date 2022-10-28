#ID:MifareUltra-WrongPara

# Head #########################################
#LABLE:
#POURPOSE:Ensure wrong length data can't be writen
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

C2C08 = []
C2C08.append(["2.WriteBlock#10","2C 08 41 0A 00 00 00 00","2C 00 00 00"])

C2C07 = []
C2C07.append(["ReadBlock10","2C 07 41 0A","56 69 56 4F 74 65 63 68 32 00 2C 00 00 10 00 00 00 00"])

C2C08Wrong = []
C2C08Wrong.append(["WriteBlock#10-3BYTE","2C 08 41 0A 11 11 11","2C 05 00 00"])
C2C08Wrong.append(["WriteBlock#10-5BTTE","2C 08 41 0A 11 11 11 11 11","2C 05 00 00"])
C2C08Wrong.append(["Write2Blocks-7BTTE","2C 08 41 0A 11 11 11 11 00 00 00","2C 05 00 00"])
C2C08Wrong.append(["Write2Blocks-9BTTE","2C 08 41 0A 11 11 11 11 00 00 00 00 00","2C 05 00 00"])

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

if(10<DeviceType):
	strMemory = Pro_SendCmd().Run(C0930[0][0],C0930[0][1],5000,False,DL)
	strMemory = strMemory.replace(" ","")
	strMemory = strMemory[0:len(strMemory)-12]

#Start PT
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],5000,False,DL),C2C01[0][2],DL)): DL.warnings = DL.warnings +1

#Poll for Ultra card + write with wrong para
strResponse = P4T_Type_1().Run(C2C02[0][0],1,C2C02[0][1],RobotAction,Robot,30000,200,DL)
if(False==DL.Check_RXResponse(0,str(C2C02[0][2]))):DL.DL.warnings = DL.warnings +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C08[0][0],C2C08[0][1],5000,False,DL),C2C08[0][2],DL)): DL.warnings = DL.warnings +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C07[0][0],C2C07[0][1],5000,False,DL),C2C07[0][2],DL)): DL.warnings = DL.warnings +1

for Case in C2C08Wrong:
	if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(Case[0],Case[1],5000,False,DL),Case[2],DL)): DL.fails = DL.fails +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C07[0][0],C2C07[0][1],5000,False,DL),C2C07[0][2],DL)): DL.fails = DL.fails +1

#Remove card + Stop PT
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