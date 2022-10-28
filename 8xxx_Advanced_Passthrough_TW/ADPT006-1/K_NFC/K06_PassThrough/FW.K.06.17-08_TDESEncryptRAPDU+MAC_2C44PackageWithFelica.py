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

CPolling = []
CPolling.append(["Polling Felica Card","2C 44 05 00 FF FF 01 01","2C 00 00 13 01 ** 00 F1 00 00 00 01 43 00 88 B4"])

C2C44=[]
C2C44.append(["Normal Write S_PAD1 -- 00",["2C 44 1F 08","01 09 00 01 80 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"],"2C00 0030 0010** 000A** 0010",["00 0B 09"," 00 00"]])
C2C44.append(["Normal Read S_PAD1 -- 00",["2C 44 0F 06","01 09 00 01 80 01"],"2C00 0040 0020** 000A** 0010",["00 1C 07","00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"]])
C2C44.append(["Normal Read S_PAD1&3&4&5 -- 11",["2C 44 15 06","01 09 00 04 80 01 80 03 80 04 80 05"],"2C00 0070 0050** 000A** 0010",["00 4C 07","00 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"]])

C2801 = []
C2801.append(["Enable Antenna","28 01 01","28 00"])

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
RobotAction = "ROBOT:CTLSCARD12"

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

if(10<DeviceType):
	strMemory = Pro_SendCmd().Run(C0930[0][0],C0930[0][1],5000,False,DL)
	strMemory = strMemory.replace(" ","")
	strMemory = strMemory[0:len(strMemory)-12]
    
if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],3000,False,DL),C2C01[0][2],DL)):DL.warnings = DL.warnings +1
if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2801[0][0],C2801[0][1],3000,False,DL),C2801[0][2],DL)):DL.warnings = DL.warnings +1

if(Robot):DL.Robot_CTLSCard(12)
else:DL.ShowMessageBox("Message","Please tap Felica card before clicking",0)
if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(CPolling[0][0],CPolling[0][1],30000,False,DL),CPolling[0][2],DL)):DL.fails=DL.fails+1
strResponse = DL.Get_RXResponse(0)
strResponse = strResponse.replace(" ", "")
strUID = strResponse[30:46]

for Case in C2C44:
	command = Case[1][0]+strUID+Case[1][1]
	EXRAPDU = Case[3][0]+strUID+Case[3][1]
	strRes = Pro_SendCmd().Run(Case[0],command,5000,False,DL)
	if(False ==  Pro_SendCmd().RunCK_C(strRes,Case[2],DL)):DL.fails = DL.fails + 1
	ListAPDU = Pro_Encryption().DecRAPDU(strRes,strKey,0,1,False,True,EXRAPDU,DL)
	ListKSN.append(ListAPDU[0])
	time.sleep(0.2)
if(Robot == True):  DL.Robot_RemoveCard()

#CheckKSN
DL.setText("BLUE","KSN list: "+str(ListKSN))
i=0
while(i<len(ListKSN)-1):
    if(ListKSN[i]!=ListKSN[i+1]):
        DL.fails = DL.fails + 1
        DL.setText("RED","KSN should not change")
        break
    i=i+1

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