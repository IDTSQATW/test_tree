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
C2C01.append(["PT Stop","2C 01 00","5669564F7465636832002C000000"])
C2C01.append(["PT Start","2C 01 01","5669564F7465636832002C0000001C9B"])

C2C40Tag3 = []
C2C40Tag3.append(["Poll tag 3","2C 40 FF 22","2C 00 00 09 0C","",False])
C2C40Tag3.append(["Tag3 Write Data","2C 40 42 01 09 00 01 80 08 31 32 33 34 35 36 37 38 31 32 33 34 35 36 37 38 ","2C 00 00 00 1C 9B","",False])
C2C40Tag3.append(["Tag3 Read Data","2C 40 41 01 09 00 01 80 08","2C 00 0028 0018** 000A** 0000","00 13 00 00 01 31 32 33 34 35 36 37 38 31 32 33 34 35 36 37 38",True])
C2C40Tag3.append(["Tag3 Write NDEF - block0","2C 40 42 01 09 00 01 80 00 10 04 01 00 0D 00 00 00 00 00 01 00 00 11 00 34","2C 00 00 00 1C 9B","",False])
C2C40Tag3.append(["Tag3 Write NDEF - block1","2C 40 42 01 09 00 01 80 01 D1 01 0D 54 02 65 6E 68 65 6C 6C 6F 57 6F 72 6C ","2C 00 00 00 1C 9B","",False])
C2C40Tag3.append(["Tag3 Write NDEF - block2","2C 40 42 01 09 00 01 80 02 64 00 00 00 00 00 00 00 00 00 00 00 00 00 DA B2","2C 00 00 00 1C 9B","",False])
C2C40Tag3.append(["Tag3 Read NDEF - block0-2","2C 40 41 01 0B 00 03 80 00 80 01 80 02","2C 00 0048 0038** 000A** 0000","00 33 00 00 03 10 04 01 00 0D 00 00 00 00 00 01 00 00 11 00 34 D1 01 0D 54 02 65 6E 68 65 6C 6C 6F 57 6F 72 6C 64 00 00 00 00 00 00 00 00 00 00 00 00 00 DA B2",True])

C0930 = [["Get device memory","09 30"]]
CC733=[["Get Dukpt Encryption","C7 33","C7 00 00 01 00"]]
CC7A3 = [["Get DataKey Encrp Type","C7 a3 01 00"," C7 00 00 06 00 00"]]
C8140 = [["Get MAC Verification output","81 40 00","81 00 00 01 00"]]
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

#TDES + MAC off + CustomerID2
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(CC7A3[0][0],CC7A3[0][1],30000,False,DL),CC7A3[0][2],DL) and False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(CC733[0][0],CC733[0][1],30000,False,DL),CC733[0][2],DL)): 
	Pro_PKI().MasterReset(DL)
	Pro_PKI().Activate(DL)
	if(False == Pro_PKI().EnsureActive(DL)):DL.warnings=DL.warnings+1
	else:
		Pro_KeyInjection().Run(5,DL)
else:
    if(False == Pro_SendCmd().RunCK(Pro_SendCmd().Run(C8140[0][0],C8140[0][1],30000,False,DL),C8140[0][2],DL)):
        Pro_PKI().MasterReset(DL)
        Pro_PKI().Activate(DL)
        if(False == Pro_PKI().EnsureActive(DL)):DL.warnings=DL.warnings+1
        else:
            Pro_KeyInjection().Run(5,DL)
if(False == Pro_SendCmd().RunCK(Pro_SendCmd().Run(CC78X[0][0],CC78X[0][1],30000,False,DL),CC78X[0][2],DL)):
	if(False == Pro_SendCmd().RunCK(Pro_SendCmd().Run(CC78X[1][0],CC78X[1][1],30000,False,DL),CC78X[1][2],DL)):DL.fails = DL.fails +1


if(10<DeviceType):
	strMemory = Pro_SendCmd().Run(C0930[0][0],C0930[0][1],5000,False,DL)
	strMemory = strMemory.replace(" ","")
	strMemory = strMemory[0:len(strMemory)-12]

#Start Pass through
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[1][0],C2C01[1][1],50000,False,DL),C2C01[1][2],DL)): DL.warnings = DL.warnings +1

#Operate tag3
if(Robot == False):DL.ShowMessageBox("card","Please Tap tag3 card after clicking",0)
else: DL.Robot_SwipeorTapCard(24,0)
for Case in C2C40Tag3:
	if (Case[4]):
		strRes = Pro_SendCmd().Run(Case[0],Case[1],5000,False,DL)
		if(False ==  Pro_SendCmd().RunCK_C(strRes,Case[2],DL)):DL.fails = DL.fails + 1
		ListAPDU = Pro_Encryption().DecRAPDU(strRes,strKey,0,1,False,False,Case[3],DL)
		ListKSN.append(ListAPDU[0])
	else:
		if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(Case[0],Case[1],5000,False,DL),Case[2],DL)): DL.fails = DL.fails +1
if(Robot == True): DL.Robot_RemoveCard()

#CheckKSN
DL.setText("BLUE","KSN list: "+str(ListKSN))
i=0
while(i<len(ListKSN)-1):
    if(ListKSN[i]!=ListKSN[i+1]):
        DL.fails = DL.fails + 1
        DL.setText("RED","KSN should not change")
        break
    i=i+1

#Stop Pass through
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],50000,False,DL),C2C01[0][2],DL)): DL.warnings = DL.warnings +1

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