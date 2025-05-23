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

C2C40Tag1 = []
C2C40Tag1.append(["0.2C-40 poll tag1","2C 40 FF 22","2C 00 00 ?? 0A"])
C2C40Tag1.append(["1.Tag1 Static Get All Data","2C 40 11","56 69 56 4F 74 65 63 68 32 00 2C 00 0090 0080** 000A** 0000"," 00 7A"])
C2C40Tag1.append(["2.Tag1 Static Read a byte 01","2C 40 12 01","2C 00 0020 0010** 000A** 0000","00 02 01 "])
C2C40Tag1.append(["3.Tag1 Static Read a byte 02 ","2C 40 12 02","2C 00 0020 0010** 000A** 0000","00 02 02 "])
C2C40Tag1.append(["4.Tag1 Static Read a byte 0A","2C 40 12 0A","2C 00 0020 0010** 000A** 0000","00 02 0A "])
C2C40Tag1.append(["5.Tag1 Static Read a byte 09","2C 40 12 09","2C 00 0020 0010** 000A** 0000","00 02 09 "])
C2C40Tag1.append(["6.Tag1 Static Write a byte","2C 40 13 09 F2","2C 00 0020 0010** 000A** 0000","00 02 09 "])
C2C40Tag1.append(["7.Tag1 Static Write a byte NE","2C 40 14 0A FF","2C 00 0020 0010** 000A** 0000","00 02 0A"])
C2C40Tag1.append(["8.Tag1 Dynamic Read a segment","2C 40 15 12","2C 00 00A0 0090** 000A** 0000","00 81 12 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"])
C2C40Tag1.append(["9.Tag1 Dynamic Write 8 bytes","2C 40 17 01 00 01 02 03 04 05 06 07","2C 00 0020 0010** 000A** 0000 ","00 09 01 00 01 02 03 04 05 06 07"])
C2C40Tag1.append(["10.Tag1 Dynamic Write 8 bytes NE","2C 40 18 01 00 01 02 03 04 05 06 07","2C 00 0020 0010** 000A** 0000","00 09 01 00 01 02 03 04 05 06 07 "])

C0930 = [["Get device memory","09 30"]]

CC733=[["Get Dukpt Encryption","C7 33","C7 00 00 01 01"]]
CC7A3 = [["Get DataKey Encrp Type","C7 a3 01 00"," C7 00 00 06 00 01"]]
C8140 = [["Get MAC Verification output","81 40 00","81 00 00 01 00"]]
strKey = "0123456789ABCDEFFEDCBA9876543210"
CC78X = []
CC78X.append(["Get customer config","C7 83","C7 00 00 05 00 01 02 00 00"])
CC78X.append(["Set customer config-2","C7 82 0001 02 0000","C7 00 00 00"])
ListKSN=[]
##################################################

def DecRAPDU1(strRes,strKey,DATAORPIN,EncryptMode,DL):
	DL.setText("BLUE","===Decrypt RAPDU===")
	strRes = strRes.replace(" ","")
	strRes = strRes[28:len(strRes)-4]
	LenRAPDU = int(strRes[0:4],16)
	strRAPDU = strRes[4:4+2*LenRAPDU]
	DL.setText("BLUE","strRAPDU: "+strRAPDU)
	strRes1 = strRes[4+2*LenRAPDU:]
	DL.setText("BLUE","strRes1: "+strRes1)
	LenKSN = int(strRes1[0:4],16)
	strKSN = strRes1[4:4+2*LenKSN]
	DL.setText("BLUE","strKSN: "+strKSN)
	DecRAPDU = DL.DecryptDLL(DATAORPIN,EncryptMode,strKey,strKSN,strRAPDU)
	return DecRAPDU


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
	else:
		Pro_KeyInjection().Run(6,DL)
else:
    if(False == Pro_SendCmd().RunCK(Pro_SendCmd().Run(C8140[0][0],C8140[0][1],30000,False,DL),C8140[0][2],DL)):
        Pro_PKI().MasterReset(DL)
        Pro_PKI().Activate(DL)
        if(False == Pro_PKI().EnsureActive(DL)):DL.warnings=DL.warnings+1
        else:
            Pro_KeyInjection().Run(6,DL)
if(False == Pro_SendCmd().RunCK(Pro_SendCmd().Run(CC78X[0][0],CC78X[0][1],30000,False,DL),CC78X[0][2],DL)):
	if(False == Pro_SendCmd().RunCK(Pro_SendCmd().Run(CC78X[1][0],CC78X[1][1],30000,False,DL),CC78X[1][2],DL)):DL.fails = DL.fails +1


if(10<DeviceType):
	strMemory = Pro_SendCmd().Run(C0930[0][0],C0930[0][1],5000,False,DL)
	strMemory = strMemory.replace(" ","")
	strMemory = strMemory[0:len(strMemory)-12]

#Start Pass through
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[1][0],C2C01[1][1],50000,False,DL),C2C01[1][2],DL)): DL.warnings = DL.warnings +1

#Operate tag1
if(Robot == False):	DL.ShowMessageBox("card","Please Tap tag1 card after clicking",0)
else: DL.Robot_SwipeorTapCard(28,0)
index = 0
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C40Tag1[index][0],C2C40Tag1[index][1],5000,False,DL),C2C40Tag1[index][2][0],DL)): DL.fails = DL.fails +1
index=index+1
## Tag 1 get all data
strRes = Pro_SendCmd().Run(C2C40Tag1[index][0],C2C40Tag1[index][1],5000,False,DL)
if(False == DL.CompareString(strRes,C2C40Tag1[index][2])):DL.fails = DL.fails +1
strData = DecRAPDU1(strRes,strKey,0,2,DL)
strByte1 = strData[10:12]
strByte2 = strData[12:14]
strByteA = strData[28:30]
strByte9 = strData[26:28]
strRead = ["","",strByte1,strByte2,strByteA,strByte9]
index = index+1
## Tag 1 read
while (index<6):
	strRes=Pro_SendCmd().Run(C2C40Tag1[index][0],C2C40Tag1[index][1],50000,False,DL)
	if(False ==  Pro_SendCmd().RunCK_C(strRes,C2C40Tag1[index][2],DL)):DL.fails = DL.fails + 1
	ListAPDU = Pro_Encryption().DecRAPDU(strRes,strKey,0,2,False,False,C2C40Tag1[index][3]+strRead[index],DL)
	ListKSN.append(ListAPDU[0])
	index = index+1
## Tag 1 write & so on
while (index < 11):
	strRes=Pro_SendCmd().Run(C2C40Tag1[index][0],C2C40Tag1[index][1],50000,False,DL)
	if(False ==  Pro_SendCmd().RunCK_C(strRes,C2C40Tag1[index][2],DL)):DL.fails = DL.fails + 1
	ListAPDU = Pro_Encryption().DecRAPDU(strRes,strKey,0,2,False,False,C2C40Tag1[index][3],DL)
	ListKSN.append(ListAPDU[0])
	index = index+1
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