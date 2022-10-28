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


T0240 = []
T0240.append(["ACT-CTLS","02 40 0A 9F 02 06 00 00 00 00 02 00 9C 01 00 DF EF 37 01 02",["02 08"]])

C2C01 = [["Passthrough Enable","2C0101","2C00"],["Passthrough Disable","2C0100","2C00"]]

CFelica=[]
CFelica.append(["Poll Felica","2C 40 FF 0A","2C 00 00 09 0C  "])
CFelica.append(["Authen Key All 00","2C 42 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00","2C "])
CFelica.append(["S-Read S_PADx-x+2","2C 43 06 03 80 03 80 06 80 05","56 69 56 4F 74 65 63 68 32 00 2C 00 00 30"])
CFelica.append(["Normal Read S_PADx -- BLOCK 03","2C 41 06 01 0B 00 01 80 03","56 69 56 4F 74 65 63 68 32 00 2C 00 00 13 00 00 01"])

C0930 = [["Get device memory","09 30"]]

C0501=[["Cancel","05 01","05 00"]]

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

if(Robot):DL.Robot_CTLSCard(46)
else:DL.ShowMessageBox("Message","Please tap SeePhone card, then wait until timeout after clicking",0)
if(False==Pro_SendCmd().RunCK_1( Pro_SendCmd().Run_1(1,T0240[0][0],T0240[0][1],50000,False,DL),T0240[0][2],DL)):DL.fails=DL.fails+1
#Operate Felica
if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],30000,False,DL),C2C01[0][2],DL)):DL.warnings = DL.warnings +1
if(Robot):DL.Robot_CTLSCard(12)
else:DL.ShowMessageBox("Message","Please tap Felica card before clicking",0)
for Felica in CFelica:
	if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(Felica[0],Felica[1],5000,False,DL),Felica[2],DL)):DL.fails=DL.fails+1
if(Robot):DL.Robot_RemoveCard()
else:DL.ShowMessageBox("Message","Please remove card",0)
if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[1][0],C2C01[1][1],30000,False,DL),C2C01[1][2],DL)):DL.warnings = DL.warnings +1

Pro_SendCmd().Run(C2C01[1][0],C2C01[1][1],30000,False,DL)


# Result Count ####################################
# Warning Count & Fail Count
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )

##################################################

#! Script END