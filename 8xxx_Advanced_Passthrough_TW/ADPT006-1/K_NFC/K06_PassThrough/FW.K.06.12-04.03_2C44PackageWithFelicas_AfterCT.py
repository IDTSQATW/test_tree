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


CSetting = []
CSetting.append(["Poll on demand","01 01 01","01 00"])
CSetting.append(["ICS 1C","60 16 01","56 69 56 4F 74 65 63 68 32 00 60 00"])
CSetting.append(["Set Terminal Data","60 06 18 00 5F 36 01 02 9F 1A 02 08 40 9F 35 01 22 9F 33 03 60 F8 C8 9F 40 05 F0 00 F0 A0 01 9F 1E 08 54 65 72 6D 69 6E 61 6C 9F 15 02 12 34 9F 16 0F 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 9F 1C 08 38 37 36 35 34 33 32 31 9F 4E 22 31 30 37 32 31 20 57 61 6C 6B 65 72 20 53 74 2E 20 43 79 70 72 65 73 73 2C 20 43 41 20 2C 55 53 41 2E DF 26 01 01 DF 10 08 65 6E 66 72 65 73 7A 68 DF 11 01 01 DF 27 01 00 DF EE 15 01 01 DF EE 16 01 00 DF EE 17 01 07 DF EE 18 01 80 DF EE 1E 08 F0 DC 3C F0 C2 9E 94 00 DF EE 1F 01 80 DF EE 1B 08 30 30 30 31 35 31 30 30 DF EE 20 01 3C DF EE 21 01 0A DF EE 22 03 32 3C 3C","56 69 56 4F 74 65 63 68 32 00 60 00"])
CSetting.append(["Set Application data-VISA","60 03 07 00 A0 00 00 00 03 10 10 14 00 9F 01 06 01 23 45 67 89 10 5F 57 01 00 5F 2A 02 08 40 9F 09 02 00 96 5F 36 01 02 9F 15 02 12 34 9F 1C 08 46 72 6F 6E 74 31 32 33 9F 4E 06 53 48 4F 50 20 31 9F 1B 04 00 00 3A 98 9F 3C 02 08 40 9F 3D 01 02 DF 25 03 9F 37 04 DF 28 03 9F 08 02 DF EE 15 01 01 DF 13 05 00 00 00 00 00 DF 14 05 00 00 00 00 00 DF 15 05 00 00 00 00 00 DF 18 01 00 DF 17 04 00 00 27 10 DF 19 01 00","56 69 56 4F 74 65 63 68 32 00 60 00"])
CSetting.append(["Set Application data-MC","60 03 07 00 A0 00 00 00 04 10 10 14 00 9F 01 06 01 23 45 67 89 10 5F 57 01 00 5F 2A 02 08 40 9F 09 02 00 96 5F 36 01 02 9F 15 02 12 34 9F 1C 08 46 72 6F 6E 74 31 32 33 9F 4E 06 53 48 4F 50 20 31 9F 1B 04 00 00 3A 98 9F 3C 02 08 40 9F 3D 01 02 DF 25 03 9F 37 04 DF 28 03 9F 08 02 DF EE 15 01 01 DF 13 05 00 00 00 00 00 DF 14 05 00 00 00 00 00 DF 15 05 00 00 00 00 00 DF 18 01 00 DF 17 04 00 00 27 10 DF 19 01 00","56 69 56 4F 74 65 63 68 32 00 60 00"])

T0240 = []
T0240.append(["ACT-Only CT","02 40 1E 9F 02 06 00 00 00 00 02 00 9C 01 00 DF EF 37 01 04 DF EF 1F 02 01 00",["02 63","02 ** DF EE 25 02 00 00"]])

C2C01 = [["Passthrough Enable","2C0101","2C00"],["Passthrough Disable","2C0100","2C00"]]

C2801 = []
C2801.append(["Enable Antenna","28 01 01","28 00"])

C2C44 = []
C2C44.append(["Polling Felica Card","2C 44 05 00 FF FF 01 01","2C 00 00 13 01 ** 00 F1 00 00 00 01 43 00 88 B4"])

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

strMemory = Pro_SendCmd().Run(C0930[0][0],C0930[0][1],5000,False,DL)
strMemory = strMemory.replace(" ","")
strMemory = strMemory[0:len(strMemory)-12]

for Set in CSetting:
    if(False==Pro_SendCmd().RunCK(Pro_SendCmd().Run(Set[0],Set[1],30000,False,DL),Set[2],DL)):DL.fails=DL.fails+1

#ICC
if(Robot):DL.Robot_ICCCard(1)
else:DL.ShowMessageBox("Message","Please insert V2CC023 test card",0)
if(False==Pro_SendCmd().RunCK_1( Pro_SendCmd().Run_1(2,T0240[0][0],T0240[0][1],50000,False,DL),T0240[0][2],DL)):DL.fails=DL.fails+1
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