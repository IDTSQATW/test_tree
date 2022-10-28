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
T0240.append(["ACT-Only CTLS","02 40 1E 9F 02 06 00 00 00 00 02 00 9C 01 00 DF EF 37 01 02","02"])

C2C01 = [["Passthrough Enable","2C0101","2C00"],["Passthrough Disable","2C0100","2C00"]]

C2801 = []
C2801.append(["Enable Antenna","28 01 01","28 00"])

C2C44 = []
C2C44.append(["Polling Felica Card","2C 44 05 00 FF FF 01 01","2C 00 00 13 01 ** 00 F1 00 00 00 01 43 00 88 B4"])

C0930 = [["Get device memory","09 30"]]


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

strMemory = Pro_SendCmd().Run(C0930[0][0],C0930[0][1],5000,False,DL)
strMemory = strMemory.replace(" ","")
strMemory = strMemory[0:len(strMemory)-12]

#Type B
if(Robot):DL.Robot_CTLSCard(17)
else:DL.ShowMessageBox("Message","Please tap any CTLS typeB card",0)
if(False==Pro_SendCmd().RunCK( Pro_SendCmd().Run(T0240[0][0],T0240[0][1],50000,False,DL),T0240[0][2],DL)):DL.fails=DL.fails+1
if(Robot):DL.Robot_RemoveCard()
#Operate Felica
if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],30000,False,DL),C2C01[0][2],DL)):DL.warnings = DL.warnings +1
if(Robot):DL.Robot_CTLSCard(12)
else:DL.ShowMessageBox("Message","Please tap Felica card before clicking, not remove until next message",0)
if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2801[0][0],C2801[0][1],3000,False,DL),C2801[0][2],DL)):DL.fails=DL.fails+1
if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C44[0][0],C2C44[0][1],5000,False,DL),C2C44[0][2],DL)):DL.fails=DL.fails+1
if(Robot):DL.Robot_RemoveCard()
else:DL.ShowMessageBox("Message","Please remove card",0)
if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[1][0],C2C01[1][1],30000,False,DL),C2C01[1][2],DL)):DL.warnings = DL.warnings +1

Pro_SendCmd().Run(C2C01[1][0],C2C01[1][1],30000,False,DL)

#Check device memory not change after script
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