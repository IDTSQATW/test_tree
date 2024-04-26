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
CCExx = [
	#Setup for further test
	["CE-01 card emulation off","CE 01 00","CE 00 0000"],
	["CE-02 create Card 00 ","CE 02 00 04 A1 A2 A3 A4 00 17 20 00 FF 00 FF 04 06 E1 04 00 19 00 00 05 06 E1 05 00 0B 00 00 00 17 D1 01 13 55 01 69 64 74 65 63 68 70 72 6F 64 75 63 74 73 2E 63 6F 6D 00 09 01 02 03 04 05 06 07 08 09","CE 00 0000"],
	["CE-02 create card 01","CE 02 01 04 A1 A2 A3 A4 00 17 20 00 FF 00 FF 04 06 E1 04 00 26 00 00 05 06 E1 05 00 0B 00 00 00 24 D1 01 20 55 01 69 64 74 65 63 68 70 72 6F 64 75 63 74 73 2E 63 6F 6D 2F 6B 69 6F 73 6B 2D 76 2D 64 65 6D 6F 00 09 01 02 03 04 05 06 07 08 09","CE 0B 0000"],
	["CE-05 select 00","CE 05 00","CE 00 0000"],
	#Update profile related commands not allowed if card simulator on
	["CE-01 card emulation on","CE 01 01","CE 00 0000"],
	["CE-02 update card 00 - fail","CE 02 00 04 A1 A2 A3 A4 00 17 20 00 FF 00 FF 04 06 E1 04 00 26 00 00 05 06 E1 05 00 0B 00 00 00 24 D1 01 20 55 01 69 64 74 65 63 68 70 72 6F 64 75 63 74 73 2E 63 6F 6D 2F 6B 69 6F 73 6B 2D 76 2D 64 65 6D 6F 00 09 01 02 03 04 05 06 07 08 09","CE 0B 0000"],
	["CE-03 read card 00 - not updated","CE 03 00","00 04 A1 A2 A3 A4 00 17 20 00 FF 00 FF 04 06 E1 04 00 19 00 00 05 06 E1 05 00 0B 00 00 00 17 D1 01 13 55 01 69 64 74 65 63 68 70 72 6F 64 75 63 74 73 2E 63 6F 6D 00 09 01 02 03 04 05 06 07 08 09"],
	["CE-05 select 01 -fail","CE 05 01","CE 0B 0000"],
	["CE-06 Check card - not updated","CE 06","CE 06 00 01 00"],
	#Update profile related commands allowed if card simulator pause
	["CE-01 card emulation pause","CE 01 02","CE 00 0000"],
	["CE-02 update card 00 -success","CE 02 00 04 A1 A2 A3 A4 00 17 20 00 FF 00 FF 04 06 E1 04 00 26 00 00 05 06 E1 05 00 0B 00 00 00 24 D1 01 20 55 01 69 64 74 65 63 68 70 72 6F 64 75 63 74 73 2E 63 6F 6D 2F 6B 69 6F 73 6B 2D 76 2D 64 65 6D 6F 00 09 01 02 03 04 05 06 07 08 09","CE 00 0000"],
	["CE-03 read card 00 -updated","CE 03 00","04 A1 A2 A3 A4 00 17 20 00 FF 00 FF 04 06 E1 04 00 26 00 00 05 06 E1 05 00 0B 00 00 00 24 D1 01 20 55 01 69 64 74 65 63 68 70 72 6F 64 75 63 74 73 2E 63 6F 6D 2F 6B 69 6F 73 6B 2D 76 2D 64 65 6D 6F 00 09 01 02 03 04 05 06 07 08 09"],
	["CE-05 select 01 -success","CE 05 01","CE 00 0000"],
	["CE-06 Check card -updated","CE 06","CE 06 00 01 01"],
	#Update profile related commands not allowed if card simulator resume
	["CE-01 card emulation resume","CE 01 03","CE 00 0000"],
	["CE-02 update card 00 -fail","CE 02 00 04 A1 A2 A3 A4 00 17 20 00 FF 00 FF 04 06 E1 04 00 19 00 00 05 06 E1 05 00 0B 00 00 00 17 D1 01 13 55 01 69 64 74 65 63 68 70 72 6F 64 75 63 74 73 2E 63 6F 6D 00 09 01 02 03 04 05 06 07 08 09","CE 0B 0000"],
	["CE-03 read card 00 -updated","CE 03 00","04 A1 A2 A3 A4 00 17 20 00 FF 00 FF 04 06 E1 04 00 26 00 00 05 06 E1 05 00 0B 00 00 00 24 D1 01 20 55 01 69 64 74 65 63 68 70 72 6F 64 75 63 74 73 2E 63 6F 6D 2F 6B 69 6F 73 6B 2D 76 2D 64 65 6D 6F 00 09 01 02 03 04 05 06 07 08 09"],
	["CE-05 select 00 -fail","CE 05 00","CE 0B 0000"],
	["CE-06 Check card - not updated","CE 06","CE 06 00 01 01"],
	#Trun off card simulator and delete profiles
	["CE-01 card emulation off","CE 01 00","CE 00 0000"],
	["CE-04 delete 00","CE 04 00","CE 00 0000"],
	["CE-04 delete 01","CE 04 01","CE 00 0000"]
]

for Case in CCExx:
	if (False == Pro_SendCmd().RunCK(Pro_SendCmd().Run(Case[0],Case[1], 3000, False, DL),Case[2], DL)): DL.fails = DL.fails + 1

##################################################

# Result Count ####################################
# Warning Count & Fail Count
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )

##################################################

#! Script END