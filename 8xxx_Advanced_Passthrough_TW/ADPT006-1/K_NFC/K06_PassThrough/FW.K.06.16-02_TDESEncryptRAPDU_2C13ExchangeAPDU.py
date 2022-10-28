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

C2C0B = []
C2C0B.append(["2C-0B poll card","2C 0B 05 00 00 00 00 1F 00","56 69 56 4F 74 65 63 68 32 00 2C 00 00 05 07"])

C2C13 = []
C2C13.append(["PPSE ","2C 13 00 00 A4 04 00 0E 32 50 41 59 2E 53 59 53 2E 44 44 46 30 31 00  ","56 69 56 4F 74 65 63 68 32 00 2C00 003A 0028** 9000 000A** 0000","00 25 6F 23 84 0E 32 50 41 59 2E 53 59 53 2E 44 44 46 30 31 A5 11 BF 0C 0E 61 0C 4F 07 A0 00 00 00 04 10 10 87 01 01"])
C2C13.append(["Select ","2C 13 00 00 A4 04 00 07 A0 00 00 00 04 10 10 00 ","56 69 56 4F 74 65 63 68 32 00 2C00 0032 0020** 9000 000A** 0000","00 1E 6F 1C 84 07 A0 00 00 00 04 10 10 A5 11 50 0F 50 50 43 20 4D 43 44 20 30 31 20 20 76 32 30"])
C2C13.append(["GPO ","2C 13 00 80 A8 00 00 02 83 00 00 ","56 69 56 4F 74 65 63 68 32 00 2C00 0032 0020** 9000 000A** 0000","00 18 77 16 82 02 59 80 94 10 08 01 01 00 10 01 01 01 18 01 02 00 20 01 02 00"])
C2C13.append(["Read Record ","2C 13 00 00 B2 01 0C 00 ","56 69 56 4F 74 65 63 68 32 00 2C00 009A 0088** 9000 000A** 0000","00 7F 70 7D 9F 6C 02 00 01 9F 62 06 00 00 00 38 00 00 9F 63 06 00 00 00 00 E0 E0 56 3C 42 35 34 31 33 33 33 30 30 38 39 36 30 30 30 31 30 5E 45 54 45 43 2F 50 41 59 50 41 53 53 5E 31 34 31 32 32 30 31 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 9F 64 01 03 9F 65 02 00 0E 9F 66 02 0E 70 9F 6B 13 54 13 33 00 89 60 00 10 D1 41 22 01 90 00 99 00 00 00 0F 9F 67 01 03"])
C2C13.append(["CCC","2C 13 00 80 2A 8E 80 04 00 00 00 00 00","56 69 56 4F 74 65 63 68 32 00 2C00 002A 0018** 9000 000A** 0000","00 11 77 0F 9F 60 02 A0 A9 9F 61 02 D9 B1 9F 36 02 00 02"])

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

if(Robot):
	DL.Robot_CTLSCard(2)
	DL.Robot_RemoveCard()

if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],5000,False,DL),C2C01[0][2],DL)):DL.fails = DL.fails + 1

if(Robot):DL.Robot_CTLSCard(2)
else:DL.ShowMessageBox("Poll Card", "Present MC21 card and ot move until the end",0)
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C0B[0][0],C2C0B[0][1],30000,False,DL),C2C0B[0][2],DL)):DL.fails = DL.fails + 1
for case in C2C13:
    strRes = Pro_SendCmd().Run(case[0],case[1],5000,False,DL)
    if(False ==  Pro_SendCmd().RunCK_C(strRes,case[2],DL)):DL.fails = DL.fails + 1
    ListAPDU = Pro_Encryption().DecRAPDU(strRes,strKey,0,1,True,False,case[3],DL)
    ListKSN.append(ListAPDU[0])
if(Robot):DL.Robot_RemoveCard()

#CheckKSN
DL.setText("BLUE","KSN list: "+str(ListKSN))
i=0
while(i<len(ListKSN)-1):
    if(ListKSN[i]!=ListKSN[i+1]):
        DL.fails = DL.fails + 1
        DL.setText("RED","KSN should not change")
        break
    i=i+1

if(False == Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[1][0],C2C01[1][1],5000,False,DL),C2C01[1][2],DL)):DL.fails = DL.fails + 1

##################################################


# Result Count ####################################
# Warning Count & Fail Count
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )

##################################################

#! Script END