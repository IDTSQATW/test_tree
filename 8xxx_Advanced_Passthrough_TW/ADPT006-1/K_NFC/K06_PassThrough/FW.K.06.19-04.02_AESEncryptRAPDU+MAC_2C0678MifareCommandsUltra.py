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

C2C08 = []
C2C08.append(["WriteBlock#6 --11","2C 08 41 06 11 11 11 11","2C 00 00 00"])
C2C08.append(["WriteBlock#6 --00","2C 08 41 06 00 00 00 00","2C 00 00 00"])

C2C07 = []
C2C07.append(["ReadBlock6","2C 07 41 05","56 69 56 4F 74 65 63 68 32 00 2C 00 0040 0020** 000A** 0010"," 00 10 ?? ?? ?? ?? 11 11 11 11"])
C2C07.append(["ReadBlock6","2C 07 42 05","56 69 56 4F 74 65 63 68 32 00 2C 00 0050 0030** 000A** 0010","00 20 ?? ?? ?? ?? 00 00 00 00"])

C0930 = [["Get device memory","09 30"]]

CC733=[["Get Dukpt Encryption","C7 33","C7 00 00 01 01"]]
CC7A3 = [["Get DataKey Encrp Type","C7 a3 01 00"," C7 00 00 06 00 01"]]
C8140 = [["Get MAC Verification output","81 40 00","81 00 00 01 01"]]
C81401 = [["Set MAC Verification output on","81 40 01","81 00 00 00"]]
strKey = "0123456789ABCDEFFEDCBA9876543210"
CC78X = []
CC78X.append(["Get customer config","C7 83","C7 00 00 05 00 01 02 00 00"])
CC78X.append(["Set customer config-2","C7 82 0001 02 0000","C7 00 00 00"])
ListKSN=[]
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

#AES + MAC on + CustomerID2
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(CC7A3[0][0],CC7A3[0][1],30000,False,DL),CC7A3[0][2],DL) and False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(CC733[0][0],CC733[0][1],30000,False,DL),CC733[0][2],DL)): 
	Pro_PKI().MasterReset(DL)
	Pro_PKI().Activate(DL)
	if(False == Pro_PKI().EnsureActive(DL)):DL.warnings=DL.warnings+1
	else:Pro_KeyInjection().Run(6,DL)
if(False == Pro_SendCmd().RunCK(Pro_SendCmd().Run(C8140[0][0],C8140[0][1],30000,False,DL),C8140[0][2],DL)):
	if(False == Pro_SendCmd().RunCK(Pro_SendCmd().Run(C81401[0][0],C81401[0][1],30000,False,DL),C81401[0][2],DL)):DL.warnings=DL.warnings+1
if(False == Pro_SendCmd().RunCK(Pro_SendCmd().Run(CC78X[0][0],CC78X[0][1],30000,False,DL),CC78X[0][2],DL)):
	if(False == Pro_SendCmd().RunCK(Pro_SendCmd().Run(CC78X[1][0],CC78X[1][1],30000,False,DL),CC78X[1][2],DL)):DL.fails = DL.fails +1

if(Robot):
	DL.Robot_CTLSCard(2)
	DL.Robot_RemoveCard()

#Start PT
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],5000,False,DL),C2C01[0][2],DL)): DL.warnings = DL.warnings +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[1][0],C2C01[1][1],5000,False,DL),C2C01[1][2],DL)): DL.warnings = DL.warnings +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2801[1][0],C2801[1][1],5000,False,DL),C2801[1][3],DL)): DL.fails = DL.fails +1
if(10<DeviceType):
	strMemory = Pro_SendCmd().Run(C0930[0][0],C0930[0][1],5000,False,DL)
	strMemory = strMemory.replace(" ","")
	strMemory = strMemory[0:len(strMemory)-12]
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],5000,False,DL),C2C01[0][2],DL)): DL.warnings = DL.warnings +1

#Poll Ultra card + write + read for ensure
strResponse = P4T_Type_1().Run(C2C02[0][0],1,C2C02[0][1],RobotAction,Robot,30000,200,DL)
if(False==DL.Check_RXResponse(0,str(C2C02[0][2]))):DL.fails = DL.fails + 1

if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C08[0][0],C2C08[0][1],5000,False,DL),C2C08[0][2],DL)): DL.fails = DL.fails +1
strRes=Pro_SendCmd().Run(C2C07[0][0],C2C07[0][1],5000,False,DL)
if(False ==  Pro_SendCmd().RunCK_C(strRes,C2C07[0][2],DL)):DL.fails = DL.fails + 1
ListAPDU = Pro_Encryption().DecRAPDU(strRes,strKey,0,2,False,True,C2C07[0][3],DL)
ListKSN.append(ListAPDU[0])

if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C08[1][0],C2C08[1][1],5000,False,DL),C2C08[1][2],DL)): DL.fails = DL.fails +1
strRes=Pro_SendCmd().Run(C2C07[1][0],C2C07[1][1],5000,False,DL)
if(False ==  Pro_SendCmd().RunCK_C(strRes,C2C07[1][2],DL)):DL.fails = DL.fails + 1
ListAPDU = Pro_Encryption().DecRAPDU(strRes,strKey,0,2,False,True,C2C07[1][3],DL)
ListKSN.append(ListAPDU[0])

#CheckKSN
DL.setText("BLUE","KSN list: "+str(ListKSN))
i=0
while(i<len(ListKSN)-1):
    if(ListKSN[i]!=ListKSN[i+1]):
        DL.fails = DL.fails + 1
        DL.setText("RED","KSN should not change")
        break
    i=i+1

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