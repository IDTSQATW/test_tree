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
C2C01.append(["PT Stop","2C 01 00","5669564F7465636832002C"])
C2C01.append(["PT Start","2C 01 01","5669564F7465636832002C0000001C9B"])

C2C02 = []
C2C02.append([" Poll for Token (OK)","2C 02 1F 00","5669564F7465636832002C00000503"])

C2C06 = []
C2C06.append(["Mifare auth - Sector 1","2C 06 01 01 FF FF FF FF FF FF","5669564F7465636832002C0000001C9B"])

C2C08 = []
C2C08.append(["Write Block #1 - 11","2C 08 31 01 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11","5669564F7465636832002C0000001C9B"])
C2C08.append(["-- Write Blocks #1,2 -----","2C 08 32 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00","5669564F7465636832002C0000001C9B"])

C2C07= []
C2C07.append(["Read Block #1 - 11","2C 07 31 01","5669564F7465636832002C00 0038 0018** 000A** 0010","0010 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11"])
C2C07.append(["Read 15Blocks, starting Block #0","2C 07 3F 00","5669564F7465636832002C00 0118 00F8** 000A** 0010","00F0 ???????????????????????????????? 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 **"])

C0930 = [["Get device memory","09 30"]]

CC733=[["Get Dukpt Encryption","C7 33","C7 00 00 01 00"]]
CC7A3 = [["Get DataKey Encrp Type","C7 a3 01 00"," C7 00 00 06 00 00"]]
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


if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],5000,False,DL),C2C01[0][2],DL)): DL.warnings = DL.warnings +1

#Get K81 memory before test
strMemory = Pro_SendCmd().Run(C0930[0][0],C0930[0][1],5000,False,DL)
strMemory = strMemory.replace(" ","")
strMemory = strMemory[0:len(strMemory)-12]

if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[1][0],C2C01[1][1],5000,False,DL),C2C01[1][2],DL)): DL.warnings = DL.warnings +1

if (Robot == True):	DL.Robot_SwipeorTapCard(4)
else: DL.ShowMessageBox("Note", "Tap Mafire S50, not move until the end", 0)
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C02[0][0],C2C02[0][1],35000,False,DL),C2C02[0][2],DL)): DL.warnings = DL.warnings +1

if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C06[0][0],C2C06[0][1],5000,False,DL),C2C06[0][2],DL)): DL.fails = DL.fails +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C08[0][0],C2C08[0][1],5000,False,DL),C2C08[0][2],DL)): DL.fails = DL.fails +1
strRes=Pro_SendCmd().Run(C2C07[0][0],C2C07[0][1],5000,False,DL)
if(False ==  Pro_SendCmd().RunCK_C(strRes,C2C07[0][2],DL)):DL.fails = DL.fails + 1
ListAPDU = Pro_Encryption().DecRAPDU(strRes,strKey,0,1,False,True,C2C07[0][3],DL)
ListKSN.append(ListAPDU[0])

if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C08[1][0],C2C08[1][1],5000,False,DL),C2C08[1][2],DL)): DL.fails = DL.fails +1
strRes=Pro_SendCmd().Run(C2C07[1][0],C2C07[1][1],5000,False,DL)
if(False ==  Pro_SendCmd().RunCK_C(strRes,C2C07[1][2],DL)):DL.fails = DL.fails + 1
ListAPDU = Pro_Encryption().DecRAPDU(strRes,strKey,0,1,False,True,C2C07[1][3],DL)
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

if(Robot == True):  DL.Robot_RemoveCard()
else: DL.ShowMessageBox("Note", "Remove card", 30000)

if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],50000,False,DL),C2C01[0][2],DL)): DL.fails = DL.fails +1

#Check device memory not change after script
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