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

C2C02 = []
C2C02.append(["2C-02 Poll for token","2C 02 1E 00 ","56 69 56 4F 74 65 63 68 32 00 2C 00 00"])
C2C0C = []
C2C0C.append(["2C-0C Poll for token","2C 0C 1E 00 00 02","56 69 56 4F 74 65 63 68 32 00 2C 00 00"])
C2C0B = []
C2C0B.append(["2C-0B Poll for token","2C 0B 05 00 00 00 00 1F 00","56 69 56 4F 74 65 63 68 32 00 2C 00 00"])

C2C03 = []
C2C03.append(["PPSE ","2C 03 00 A4 04 00 0E 32 50 41 59 2E 53 59 53 2E 44 44 46 30 31 00  ","56 69 56 4F 74 65 63 68 32 00 2C00 0052 0030** 9000 000A** 0010","00 25 6F 23 84 0E 32 50 41 59 2E 53 59 53 2E 44 44 46 30 31 A5 11 BF 0C 0E 61 0C 4F 07 A0 00 00 00 04 10 10 87 01 01"])

C2C07= []
C2C07.append(["Read Block #1 - 11","2C 07 41 01","5669564F7465636832002C00 0040 0020** 000A** 0010","0010 "])

C2C40 = []
C2C40.append(["Poll tag 2","2C 40 FF 22","2C 00 00 08 0B "])
C2C40.append(["Tag2 Read Data(16 bytes)","2C 40 21 06","2C 00 0040 0020** 000A** 0010","00 10 11 11 11 11"])


C2C44 = []
C2C44.append(["Polling Felica Card","2C 44 05 00 FF FF 01 01","2C 00 00 13 01 ** 00 F1 00 00 00 01 43 00 88 B4"])
C2C44.append(["Normal Read S_PAD1 -- 00",["2C 44 0F 06","01 09 00 01 80 01"],"2C00 0040 0020** 000A** 0010",["00 1C 07","00 00 01"]])


CC733=[["Get Dukpt Encryption","C7 33","C7 00 00 01 01"]]
CC7A3 = [["Get DataKey Encrp Type","C7 a3 01 00"," C7 00 00 06 00 01"]]
C8140 = [["Get MAC Verification output","81 40 00","81 00 00 01 01"]]
C81401 = [["Set MAC Verification output on","81 40 01","81 00 00 00"]]
strKey = "0123456789ABCDEFFEDCBA9876543210"
CC78X = []
CC78X.append(["Get customer config","C7 83","C7 00 00 05 00 01 02 00 00"])
CC78X.append(["Set customer config-2","C7 82 0001 02 0000","C7 00 00 00"])
ListKSN=[]

C9019 = [["RAPDU Output Plaintext","901900","9000"]]
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

#AES + MAC off + CustomerID2
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

if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],5000,False,DL),C2C01[0][2],DL)):DL.fails = DL.fails + 1

if(Robot):DL.Robot_CTLSCard(2)
else:DL.ShowMessageBox("Poll Card", "Present MC21 card and ot move until next message",0)
#Polling with 2C-0C
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C0C[0][0],C2C0C[0][1],30000,False,DL),C2C0C[0][2],DL)):DL.fails = DL.fails + 1
strRes = Pro_SendCmd().Run(C2C03[0][0],C2C03[0][1],5000,False,DL)
if(False ==  Pro_SendCmd().RunCK_C(strRes,C2C03[0][2],DL)):DL.fails = DL.fails + 1
ListAPDU = Pro_Encryption().DecRAPDU(strRes,strKey,0,2,True,True,C2C03[0][3],DL)
ListKSN.append(ListAPDU[0])
#Polling with 2C-0B
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C0B[0][0],C2C0B[0][1],30000,False,DL),C2C0B[0][2],DL)):DL.fails = DL.fails + 1
strRes = Pro_SendCmd().Run(C2C03[0][0],C2C03[0][1],5000,False,DL)
if(False ==  Pro_SendCmd().RunCK_C(strRes,C2C03[0][2],DL)):DL.fails = DL.fails + 1
ListAPDU = Pro_Encryption().DecRAPDU(strRes,strKey,0,2,True,True,C2C03[0][3],DL)
ListKSN.append(ListAPDU[0])
if(Robot):DL.Robot_RemoveCard()
#Polling with 2C-0C again
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C0C[0][0],C2C0C[0][1],30000,False,DL),C2C0C[0][2],DL)):DL.fails = DL.fails + 1
strRes = Pro_SendCmd().Run(C2C03[0][0],C2C03[0][1],5000,False,DL)
if(False ==  Pro_SendCmd().RunCK_C(strRes,C2C03[0][2],DL)):DL.fails = DL.fails + 1
ListAPDU = Pro_Encryption().DecRAPDU(strRes,strKey,0,2,True,True,C2C03[0][3],DL)
ListKSN.append(ListAPDU[0])

if (Robot):	DL.Robot_SwipeorTapCard(14)
else: DL.ShowMessageBox("Note", "Tap Mafire Ultra, not move until next message", 0)
#Polling with 2C-02
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C02[0][0],C2C02[0][1],30000,False,DL),C2C02[0][2],DL)):DL.fails = DL.fails + 1
strRes=Pro_SendCmd().Run(C2C07[0][0],C2C07[0][1],5000,False,DL)
if(False ==  Pro_SendCmd().RunCK_C(strRes,C2C07[0][2],DL)):DL.fails = DL.fails + 1
ListAPDU = Pro_Encryption().DecRAPDU(strRes,strKey,0,2,False,True,C2C07[0][3],DL)
ListKSN.append(ListAPDU[0])
#Polling with 2C-40
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C40[0][0],C2C40[0][1],30000,False,DL),C2C40[0][2],DL)): DL.fails = DL.fails +1
strRes = Pro_SendCmd().Run(C2C40[1][0],C2C40[1][1],5000,False,DL)
if(False ==  Pro_SendCmd().RunCK_C(strRes,C2C40[1][2],DL)):DL.fails = DL.fails + 1
ListAPDU = Pro_Encryption().DecRAPDU(strRes,strKey,0,2,False,True,C2C40[1][3],DL)
ListKSN.append(ListAPDU[0])
if(Robot):DL.Robot_RemoveCard()

if(Robot):DL.Robot_CTLSCard(12)
else:DL.ShowMessageBox("Message","Please tap Felica card before clicking",0)
#Polling with 2C-44
if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C44[0][0],C2C44[0][1],30000,False,DL),C2C44[0][2],DL)):DL.fails=DL.fails+1
strResponse = DL.Get_RXResponse(0)
strResponse = strResponse.replace(" ", "")
strUID = strResponse[30:46]
command = C2C44[1][1][0]+strUID+C2C44[1][1][1]
EXRAPDU = C2C44[1][3][0]+strUID+C2C44[1][3][1]
strRes = Pro_SendCmd().Run(C2C44[1][0],command,5000,False,DL)
if(False ==  Pro_SendCmd().RunCK_C(strRes,C2C44[1][2],DL)):DL.fails = DL.fails + 1
ListAPDU = Pro_Encryption().DecRAPDU(strRes,strKey,0,2,False,True,EXRAPDU,DL)
ListKSN.append(ListAPDU[0])


#CheckKSN
DL.setText("BLUE","KSN list: "+str(ListKSN))
i=0
while(i<len(ListKSN)-1):
    if(int(ListKSN[i+1][18:20],16)-int(ListKSN[i][18:20],16)!=1):
        DL.fails = DL.fails + 1
        DL.setText("RED","KSN should increase")
        break
    i=i+1


if(False == Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[1][0],C2C01[1][1],30000,False,DL),C2C01[1][2],DL)):DL.fails = DL.fails + 1

#Reset reader to TDES encryption + MAC off
if(Robot):
	Pro_PKI().MasterReset(DL)
	DL.SendIOCommand("IDG","900700",5000)
	if(False == Pro_SendCmd().RunCK(Pro_SendCmd().Run(C9019[0][0],C9019[0][1],30000,False,DL),C9019[0][2],DL)):DL.fails = DL.fails +1
	DL.SendIOCommand("IDG","900701",5000)
	Pro_PKI().Activate(DL)
	if(False == Pro_PKI().EnsureActive(DL)):DL.warnings=DL.warnings+1
	else:Pro_KeyInjection().Run(5,DL)
else:
	DL.setText("RED", "[Test Result]\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
	if(True==DL.ShowMessageBox("message", "Set reader back to 'RAPDU Plaintext' + TDES + MAC off?", 0)):
		Pro_PKI().MasterReset(DL)
		DL.SendIOCommand("IDG","900700",5000)
		if(False == Pro_SendCmd().RunCK(Pro_SendCmd().Run(C9019[0][0],C9019[0][1],30000,False,DL),C9019[0][2],DL)):DL.fails = DL.fails +1
		DL.SendIOCommand("IDG","900701",5000)
		Pro_PKI().Activate(DL)
		if(False == Pro_PKI().EnsureActive(DL)):DL.warnings=DL.warnings+1
		else:Pro_KeyInjection().Run(5,DL)
##################################################


# Result Count ####################################
# Warning Count & Fail Count
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )

##################################################

#! Script END