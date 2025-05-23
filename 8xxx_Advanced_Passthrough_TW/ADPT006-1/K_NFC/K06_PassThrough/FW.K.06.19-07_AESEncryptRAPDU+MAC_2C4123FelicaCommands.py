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

#2C41&2C43 not encrypt even customer ID 02
C2C4X=[]
C2C4X.append(["Normal Write S_PADx -- BLOCK 03","2C 41 08 01 09 00 01 80 03 03 03 03 03 03 03 03 03 03 03 03 03 03 03 03 03","56 69 56 4F 74 65 63 68 32 00 2C 00 00 02 00 00","",False])
C2C4X.append(["Normal Read S_PADx -- BLOCK 03","2C 41 06 01 0B 00 01 80 03","2C 00 00 13 00 00 01 03 03 03 03 03 03 03 03 03 03 03 03 03 03 03 03","",False])
C2C4X.append(["S-Read S_PADx-x+3 -- BLOCK 03, 06, 05","2C 43 06 03 80 03 80 06 80 05","56 69 56 4F 74 65 63 68 32 00 2C 00 00 30 03 03 03 03 03 03 03 03 03 03 03 03 03 03 03 03 **","",False])

T2C40=[]
T2C40.append(["Please Tap Felica Lite Card","FF 0A","2C 00 00 09 0C "])

C0930 = [["Get device memory","09 30"]]

CC733=[["Get Dukpt Encryption","C7 33","C7 00 00 01 01"]]
CC7A3 = [["Get DataKey Encrp Type","C7 a3 01 00"," C7 00 00 06 00 01"]]
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
RobotAction = "ROBOT:CTLSCARD12"

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

if(10<DeviceType):
	strMemory = Pro_SendCmd().Run(C0930[0][0],C0930[0][1],5000,False,DL)
	strMemory = strMemory.replace(" ","")
	strMemory = strMemory[0:len(strMemory)-12]
    
if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],3000,False,DL),C2C01[0][2],DL)):DL.warnings = DL.warnings +1

if(False==Pro_SendCmd().RunCK(P4T2C40_Type_1().Run(T2C40[0][0],1,T2C40[0][1],RobotAction,Robot,50000,200,DL),T2C40[0][2],DL)):DL.fails=DL.fails+1
if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C42[0][0],C2C42[0][1],30000,False,DL),C2C42[0][2],DL)):DL.fails=DL.fails+1
for Case in C2C4X:
	if (Case[4]):
		strRes = Pro_SendCmd().Run(Case[0],Case[1],5000,False,DL)
		if(False ==  Pro_SendCmd().RunCK_C(strRes,Case[2],DL)):DL.fails = DL.fails + 1
		Pro_Encryption().DecRAPDU(strRes,strKey,0,1,False,False,Case[3],DL)
	else:
		if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(Case[0],Case[1],5000,False,DL),Case[2],DL)): DL.fails = DL.fails +1
	time.sleep(0.2)
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