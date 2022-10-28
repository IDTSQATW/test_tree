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

C2C01 = [["Start PT","2C 01 01","2C 00"],["Stop PT","2C 01 00","2C 00"]]

P4T=[]
P4T.append(["2C-02 poll card","2C 02 1F 00","2C 00"])
P4T.append(["2C-0C 0001","2C 0C 1F 00 00 01","2C 00"])
P4T.append(["2C-0C 0002","2C 0C 1F 00 00 02","2C 00"])
P4T.append(["2C-0C 0003","2C 0C 1F 00 00 03","2C 00"])
P4T.append(["2C-0B poll card","2C 0B 05 00 00 00 00 1F 00","2C 00"])

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

if(Robot):DL.Robot_CTLSCard(4)
else:DL.ShowMessageBox("Message","Please tap a CTLS card, not remove until the end",0)

if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],50000,False,DL),C2C01[0][2],DL)): DL.warnings = DL.warnings +1

strResponse = Pro_SendCmd().Run(P4T[0][0],P4T[0][1],50000,False,DL)
strRes=DL.Get_RXResponse(0)
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(P4T[1][0],P4T[1][1],50000,False,DL),strRes,DL)):DL.fails=DL.fails+1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(P4T[2][0],P4T[2][1],50000,False,DL),strRes,DL)):DL.fails=DL.fails+1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(P4T[3][0],P4T[3][1],50000,False,DL),strRes,DL)):DL.fails=DL.fails+1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(P4T[4][0],P4T[4][1],50000,False,DL),strRes,DL)):DL.fails=DL.fails+1

if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[1][0],C2C01[1][1],50000,False,DL),C2C01[1][2],DL)): DL.warnings = DL.warnings +1

if(Robot):DL.Robot_RemoveCard()
else:DL.ShowMessageBox("Message","Please remove the card",50000)

##################################################

##################################################

# Result Count ####################################
# Warning Count & Fail Count
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )

##################################################

#! Script END