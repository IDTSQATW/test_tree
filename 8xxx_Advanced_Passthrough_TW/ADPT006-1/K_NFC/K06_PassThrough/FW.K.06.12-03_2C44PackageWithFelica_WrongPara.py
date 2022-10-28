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
C2C44.append(["Normal Write S_PAD01 -- wrong para",["2C 44 18 08","01 09 00 01 80 01 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11"],["2C 05 00 00"]])
C2C44.append(["Normal Read S_PAD1&3&4&5 -- wrong para",["2C 44 0F 06","01 09 00 04 80 01 80 03 80 04 80 05"],["2C 05 00 00"]])


C2801 = []
C2801.append(["Enable Antenna","28 01 01","28 00"])

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
if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2801[0][0],C2801[0][1],3000,False,DL),C2801[0][2],DL)):DL.warnings = DL.warnings +1

if(Robot):DL.Robot_CTLSCard(12)
else:DL.ShowMessageBox("Message","Please tap Felica card before clicking",0)
if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(CPolling[0][0],CPolling[0][1],30000,False,DL),CPolling[0][2],DL)):DL.fails=DL.fails+1
strResponse = DL.Get_RXResponse(0)
strResponse = strResponse.replace(" ", "")
strUID = strResponse[30:46]


for Case in C2C44:
	command = Case[1][0]+strUID+Case[1][1]
	response = Case[2][0]
	if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(Case[0],command,3000,False,DL),response,DL)):DL.fails=DL.fails+1
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