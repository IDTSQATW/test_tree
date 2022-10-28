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
Robot =  DL.isRobot
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

C0101 = [["Poll on demand","01 01 01","01 00"],["Auto Poll","01 01 00","01 00"]]
C2C01 = [["Passthrough Enable","2C0101","2C00"],["Passthrough Disable","2C0100","2C00"]]

C2C42=[]
C2C42.append(["Authen Key","2C 42 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00","2C 00"])

C2C41=[]
C2C41.append(["Normal Read ID","2C 41 06 01 0B 00 01 80 82","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13"])
C2C41.append(["Normal Read S_PAD0","2C 41 06 01 0B 00 01 80 00","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13 00 00 01"])
C2C41.append(["Normal Read S_PAD1","2C 41 06 01 0B 00 01 80 01","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13 00 00 01"])
C2C41.append(["Normal Read S_PAD2","2C 41 06 01 0B 00 01 80 02","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13"])
C2C41.append(["Normal Read S_PAD3","2C 41 06 01 0B 00 01 80 03","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13"])
C2C41.append(["Normal Read S_PAD4","2C 41 06 01 0B 00 01 80 04","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13"])
C2C41.append(["Normal Read S_PAD5","2C 41 06 01 0B 00 01 80 05","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13"])
C2C41.append(["Normal Read S_PAD6","2C 41 06 01 0B 00 01 80 06","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13"])
C2C41.append(["Normal Read S_PAD7","2C 41 06 01 0B 00 01 80 07","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13 00 00 01"])
C2C41.append(["Normal Read S_PAD8","2C 41 06 01 0B 00 01 80 08","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13"])
C2C41.append(["Normal Read S_PAD9","2C 41 06 01 0B 00 01 80 09","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13"])
C2C41.append(["Normal Read S_PAD10","2C 41 06 01 0B 00 01 80 0A","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13"])
C2C41.append(["Normal Read S_PAD11","2C 41 06 01 0B 00 01 80 0B","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13"])
C2C41.append(["Normal Read S_PAD12","2C 41 06 01 0B 00 01 80 0C","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13"])
C2C41.append(["Normal Read S_PAD13","2C 41 06 01 0B 00 01 80 0D","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13"])
C2C41.append(["Normal Read Reg","2C 41 06 01 0B 00 01 80 0E","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13 00 00 01 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF"])
C2C41.append(["Normal Read RC","2C 41 06 01 0B 00 01 80 80","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13"])
C2C41.append(["Normal Read MAC","2C 41 06 01 0B 00 01 80 81","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13"])
C2C41.append(["Normal Read ID","2C 41 06 01 0B 00 01 80 82","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13"])
C2C41.append(["Normal Read D_ID","2C 41 06 01 0B 00 01 80 83","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13"])
C2C41.append(["Normal Read SER_C","2C 41 06 01 0B 00 01 80 84","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13"])
C2C41.append(["Normal Read SYS_C","2C 41 06 01 0B 00 01 80 85","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13"])
C2C41.append(["Normal Read CKV","2C 41 06 01 0B 00 01 80 86","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13"])
C2C41.append(["Normal Read CK","2C 41 06 01 0B 00 01 80 87","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13"])
C2C41.append(["Normal Read MC","2C 41 06 01 0B 00 01 80 88","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13"])
C2C41.append(["Normal Read WCNT","2C 41 06 01 0B 00 01 80 90","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13"])
C2C41.append(["Normal Read STATE","2C 41 06 01 0B 00 01 80 92","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13"])
C2C41.append(["Normal Read CRC_CHECK","2C 41 06 01 0B 00 01 80 A0","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13"])

T2C40=[]
T2C40.append(["Please Tap Felica Lite Card","FF 0A","2C 00 00 09 0C "])

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
RobotAction = "ROBOT:CTLSCARD12"

if(10<DeviceType):
	strMemory = Pro_SendCmd().Run(C0930[0][0],C0930[0][1],5000,False,DL)
	strMemory = strMemory.replace(" ","")
	strMemory = strMemory[0:len(strMemory)-12]
    
if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],3000,False,DL),C2C01[0][2],DL)):DL.warnings = DL.warnings +1

if(False==Pro_SendCmd().RunCK(P4T2C40_Type_1().Run(T2C40[0][0],1,T2C40[0][1],RobotAction,Robot,50000,200,DL),T2C40[0][2],DL)):DL.fails=DL.fails+1
for Case in C2C41:
	if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(Case[0],Case[1],3000,False,DL),Case[2],DL)):DL.fails=DL.fails+1
if(Robot == True):  DL.Robot_RemoveCard()

if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[1][0],C2C01[1][1],30000,False,DL),C2C01[1][2],DL)):DL.warnings = DL.warnings +1

#Check device memory not change after script
if(10<DeviceType):
    if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C0930[0][0],C0930[0][1],5000,False,DL),strMemory,DL)): 
        DL.fails = DL.fails +1
        DL.setText("RED","Device memory changed after script")

# Result Count ####################################
# Warning Count & Fail Count
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )

##################################################

#! Script END