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

C2801 = []
C2801.append(["Antenna Enable","28 01 01","5669564F74656368320028000000D66A"])

C2C02 = []
C2C02.append(["Poll for Token","2C 02 1F 00","5669564F7465636832002C00000503"])

C2C06 = []
C2C06.append(["Authenticate Block 49 -Default","2C 06 31 01 FF FF FF FF FF FF","5669564F7465636832002C0000001C9B"])
C2C06.append(["Authenticate Block 54 -Changed","2C 06 37 01 11 22 33 44 55 66","5669564F7465636832002C0000001C9B"])

C2C08 = []
C2C08.append(["Write Key A, Block 55 - 11 22 33 44 55 66","2C 08 31 37 11 22 33 44 55 66 FF 07 80 69 FF FF FF FF FF FF","5669564F7465636832002C0000001C9B"])
C2C08.append(["Write Key A, Block 55 - FF FF FF FF FF FF","2C 08 31 37 FF FF FF FF FF FF FF 07 80 69 FF FF FF FF FF FF","5669564F7465636832002C0000001C9B"])

CCase = []
CCase.append(["Poll for Token","2C 02 1F 00","5669564F7465636832002C00000503"])
CCase.append(["Authenticate Block 49 - CORRECT1","2C 06 31 01 FF FF FF FF FF FF","5669564F7465636832002C0000001C9B"])
CCase.append(["Read Block 49","2C 07 31 31","5669564F7465636832002C000010"])
CCase.append(["Read Block 50","2C 07 31 32","5669564F7465636832002C000010"])
CCase.append(["Read Block 51","2C 07 31 33","5669564F7465636832002C000010"])
CCase.append(["Read Block 56","2C 07 31 38","5669564F7465636832002C000010"])
CCase.append(["Read Block 57","2C 07 31 39","5669564F7465636832002C000010"])
CCase.append(["Read Block 54","2C 07 31 36","5669564F7465636832002C0A0000"])
CCase.append(["Read Block 55","2C 07 31 37","5669564F7465636832002C0A0000"])
CCase.append(["Read Block 49","2C 07 31 31","5669564F7465636832002C000010"])
CCase.append(["Read Block 57","2C 07 31 39","5669564F7465636832002C000010"])

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

  
Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],50000,False,DL)
if(10<DeviceType):
	strMemory = Pro_SendCmd().Run(C0930[0][0],C0930[0][1],5000,False,DL)
	strMemory = strMemory.replace(" ","")
	strMemory = strMemory[0:len(strMemory)-12]

if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[1][0],C2C01[1][1],5000,False,DL),C2C01[1][2],DL)): DL.warnings = DL.warnings +1
if (Robot == True):	DL.Robot_SwipeorTapCard(4,2)
else: DL.ShowMessageBox("Note!", "Tap Mafire S50, not move until the end", 0)

#Write key A of block 55
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C02[0][0],C2C02[0][1],35000,False,DL),C2C02[0][2],DL)): DL.warnings = DL.warnings +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C06[0][0],C2C06[0][1],5000,False,DL),C2C06[0][2],DL)): DL.warnings = DL.warnings +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C08[0][0],C2C08[0][1],5000,False,DL),C2C08[0][2],DL)): DL.warnings = DL.warnings +1

for Case in CCase:
	if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(Case[0],Case[1],5000,False,DL),Case[2],DL)): DL.fails = DL.fails +1

#Write key block 55 back to default
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C02[0][0],C2C02[0][1],5000,False,DL),C2C02[0][2],DL)): DL.warnings = DL.warnings +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C06[1][0],C2C06[1][1],5000,False,DL),C2C06[1][2],DL)): DL.warnings = DL.warnings +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C08[1][0],C2C08[1][1],5000,False,DL),C2C08[1][2],DL)): DL.warnings = DL.warnings +1

if(Robot == True):  DL.Robot_RemoveCard()
else: DL.ShowMessageBox("Note!", "Remove card", 0)
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],5000,False,DL),C2C01[0][2],DL)): DL.warnings = DL.warnings +1


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