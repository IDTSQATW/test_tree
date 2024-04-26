#ID:6201_GetPIN

# Head #########################################
#LABLE:
#POURPOSE: 4.Check PIN encryption in TDES
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

if (DL.isRobot==True):
	DL.setText("RED","Please run manually")
 	DL.pyresult = DL.RUN_AUTO_NOT_SUPPORT
 	sys.exit()
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

if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run("Card emulation on","CE 01 01",3000,False,DL),"CE 00 00 00",DL)): DL.fails = DL.fails +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run("ACT","02 40 05",8000,False,DL),"02 0B 00 00",DL)): DL.fails = DL.fails +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run("Reboot","77 05",8000,False,DL),"77 00 00 00",DL)): DL.fails = DL.fails +1
time.sleep(20)
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run("ACT","02 40 05",8000,False,DL),"02 0B 00 00",DL)): DL.fails = DL.fails +1


if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run("Card emulation pause","CE 01 02",3000,False,DL),"CE 00 00 00",DL)): DL.fails = DL.fails +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run("ACT","02 40 05",8000,False,DL),"02 08 00 00",DL)): DL.fails = DL.fails +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run("Reboot","77 05",8000,False,DL),"77 00 00 00",DL)): DL.fails = DL.fails +1
time.sleep(20)
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run("ACT","02 40 05",8000,False,DL),"02 08 00 00",DL)): DL.fails = DL.fails +1

if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run("Card emulation resume","CE 01 03",3000,False,DL),"CE 00 00 00",DL)): DL.fails = DL.fails +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run("ACT","02 40 05",8000,False,DL),"02 0B 00 00",DL)): DL.fails = DL.fails +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run("Reboot","77 05",8000,False,DL),"77 00 00 00",DL)): DL.fails = DL.fails +1
time.sleep(20)
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run("ACT","02 40 05",8000,False,DL),"02 08 00 00",DL)): DL.fails = DL.fails +1

if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run("Card emulation off","CE 01 00",3000,False,DL),"CE 00 00 00",DL)): DL.fails = DL.fails +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run("ACT","02 40 05",8000,False,DL),"02 08 00 00",DL)): DL.fails = DL.fails +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run("Reboot","77 05",8000,False,DL),"77 00 00 00",DL)): DL.fails = DL.fails +1
time.sleep(20)
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run("ACT","02 40 05",8000,False,DL),"02 08 00 00",DL)): DL.fails = DL.fails +1

if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run("Card emulation undefiend","CE 01 04",3000,False,DL),"CE 06 00 00",DL)): DL.fails = DL.fails +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run("ACT","02 40 05",8000,False,DL),"02 08 00 00",DL)): DL.fails = DL.fails +1
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run("Reboot","77 05",8000,False,DL),"77 00 00 00",DL)): DL.fails = DL.fails +1
time.sleep(20)
if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run("ACT","02 40 05",8000,False,DL),"02 08 00 00",DL)): DL.fails = DL.fails +1

##################################################

# Result Count ####################################
# Warning Count & Fail Count
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )

##################################################

#! Script END