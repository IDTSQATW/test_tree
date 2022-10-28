#ID:ePurse-WithSpecifiedKeyWithBackup

# Head #########################################
#LABLE:
#POURPOSE:Operate one block with specified + backup with specified key; backup will fail when keys different
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


C2C01 = []
C2C01.append(["PT Start","2C 01 01","2C 00 00 00"])
C2C01.append(["PT Stop","2C 01 00","2C ?? 00 00"])

C2C02 = [["Poll for token","2C 02 1F 00","56 69 56 4F 74 65 63 68 32 00 2C 00 00 05 03","CTLSCARD20"]]

C2C06 = []
C2C06.append(["Authenticate - Default","2C 06 31 01 FF FF FF FF FF FF","5669564F7465636832002C0000001C9B"])
C2C06.append(["Authenticate Block 52 - Changed Key","2C 06 34 01 11 22 33 44 55 66","5669564F7465636832002C0000001C9B"])

C2C07 = []
C2C07.append(["Read Initialized Blocks 52","2C 07 31 34","5669564F7465636832002C0000108719000078E6FFFF8719000000FF00FF"])
C2C07.append(["Read Initialized Blocks 54","2C 07 31 36","5669564F7465636832002C00001011111111111111111111111111111111"])
C2C07.append(["Read 52 -DECed","2C 07 31 34","5669564F7465636832002C0000108619000079E6FFFF8619000000FF00FF"])
C2C07.append(["Read 54 -Changed","2C 07 31 36","5669564F7465636832002C0000108619000079E6FFFF8619000000FF00FF"])

C2C08 = []
C2C08.append(["Initialize Blocks 52","2C 08 31 34 87 19 00 00 78 E6 FF FF 87 19 00 00 00 FF 00 FF","5669564F7465636832002C0000001C9B"])
C2C08.append(["Initialize Blocks 54","2C 08 31 36 11111111111111111111111111111111","5669564F7465636832002C0000001C9B"])
C2C08.append(["Write KeyA Block 55 - 11 22 33 44 55 66","2C 08 31 37 11 22 33 44 55 66 FF 07 80 69 FF FF FF FF FF FF","5669564F7465636832002C0000001C9B"])
C2C08.append(["Write Key A, Block 55 - FF FF FF FF FF FF","2C 08 31 37 FF FF FF FF FF FF FF 07 80 69 FF FF FF FF FF FF","5669564F7465636832002C0000001C9B"])

C2C0A = []
C2C0A.append(["0.Decrement Block 52 with backup -Backup with correct keyA","2C 0A 32 34 0B 01 00 00 00 01 11 22 33 44 55 66 36 08 34 01 11 22 33 44 55 66","5669564F7465636832002C000000"])

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

if(10<DeviceType):
	strMemory = Pro_SendCmd().Run(C0930[0][0],C0930[0][1],5000,False,DL)
	strMemory = strMemory.replace(" ","")
	strMemory = strMemory[0:len(strMemory)-12]
    
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[0][0],C2C01[0][1],5000,False,DL),C2C01[0][2],DL)): DL.warnings = DL.warnings +1
if(Robot == False):DL.ShowMessageBox("card","Please Tap S70 card after clicking",0)
else: DL.Robot_CTLSCard(20,1)
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C02[0][0],C2C02[0][1],50000,False,DL),C2C02[0][2][0],DL)): DL.fails = DL.fails +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C06[0][0],C2C06[0][1],5000,False,DL),C2C06[0][2],DL)): DL.warnings = DL.warnings +1
#initialize block
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C08[0][0],C2C08[0][1],5000,False,DL),C2C08[0][2],DL)): DL.warnings = DL.warnings +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C07[0][0],C2C07[0][1],5000,False,DL),C2C07[0][2],DL)): DL.warnings = DL.warnings +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C08[1][0],C2C08[1][1],5000,False,DL),C2C08[1][2],DL)): DL.warnings = DL.warnings +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C07[1][0],C2C07[1][1],5000,False,DL),C2C07[1][2],DL)): DL.warnings = DL.warnings +1
#change key
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C08[2][0],C2C08[2][1],5000,False,DL),C2C08[2][2],DL)): DL.warnings = DL.warnings +1


#Test
#Decrement Block 52 with backup -Backup with correct keyA
if(Robot == False):	DL.ShowMessageBox("card","Please Remove then ReTap S70 card",0)
else: 
	DL.Robot_RemoveCard()
	DL.Robot_CTLSCard(20,1)
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C02[0][0],C2C02[0][1],50000,False,DL),C2C02[0][2][0],DL)): DL.fails = DL.fails +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C0A[0][0],C2C0A[0][1],5000,False,DL),C2C0A[0][2],DL)): DL.fails = DL.fails +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C06[1][0],C2C06[1][1],5000,False,DL),C2C06[1][2],DL)): DL.fails = DL.fails +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C07[2][0],C2C07[2][1],5000,False,DL),C2C07[2][2],DL)): DL.fails = DL.fails +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C07[3][0],C2C07[3][1],5000,False,DL),C2C07[3][2],DL)): DL.fails = DL.fails +1

#Write keys back + Remove card + stop PT
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C02[0][0],C2C02[0][1],50000,False,DL),C2C02[0][2][0],DL)): DL.warnings = DL.warnings +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C06[1][0],C2C06[1][1],5000,False,DL),C2C06[1][2],DL)): DL.warnings = DL.warnings +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C08[3][0],C2C08[3][1],5000,False,DL),C2C08[3][2],DL)): DL.warnings = DL.warnings +1
if(Robot == True):  DL.Robot_RemoveCard()
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run(C2C01[1][0],C2C01[1][1],5000,False,DL),C2C01[1][2],DL)): DL.warnings = DL.warnings +1

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