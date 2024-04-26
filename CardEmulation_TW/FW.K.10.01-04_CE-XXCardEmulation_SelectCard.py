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
Site = [
	["00","0406E104 0019 0000","0017","D1 01 13 55 01 69647465636870726F64756374732E636F6D","idtech.com"],
	["01","0406E104 0010 0000","000E","D101 0A 5501 62616964752E636F6D","baidu.com"],
	["02","0406E104 0026 0000","0024","D101 20 5501 69647465636870726F64756374732E636F6D2F6B696F736B2D762D64656D6F","idtechproducts.com/kiosk-v-demo"],
	["07","0406E104 0023 0000","0021","D101 1D 5501 69647465636870726f64756374732e61746c61737369616e2e6e6574","idtechproducts.atlassian.net"],
	["04","0406E104 0014 0000","0012","D101 0E 5501 6D66692E6170706C652E636F6D","mfi.apple.com"],
	["05","0406E104 0014 0000","0012","D101 0E 5501 7777772E656D76636F2E636F6D","www.emvco.com"],
	["06","0406E104 0013 0000","0011","D101 0D 5501 7777772E66696D652E636F6D","www.fime.com"],
	["03","0406E104 001B 0000","0019","D101 15 5501 7777772E696363736F6C7574696F6E732E636F6D","www.iccsolutions.com"],
	["08","0406E104 0023 0000","0021","D101 1D 5501 7777772E70636973656375726974797374616E64617264732E6F7267","www.pcisecuritystandards.org"],
	["09","0406E104 001A 0000","0018","D101 14 5501 7777772E756C74657374746F6F6C732E636F6D","www.ultesttools.com"],
]

if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run("Card emulation off","CE 01 00",3000,False,DL),"CE 00 00 00",DL)): DL.fails = DL.fails +1
for Case in Site:
	if (False == Pro_SendCmd().RunCK(Pro_SendCmd().Run("Card emulation off", "CE 01 00", 3000, False, DL),"CE 00 00 00", DL)): DL.fails = DL.fails + 1
	if (False == Pro_SendCmd().RunCK(Pro_SendCmd().Run("Select Card", "CE 05"+Case[0], 3000, False, DL),"CE 00 00 00", DL)): DL.fails = DL.fails + 1
	if (False == Pro_SendCmd().RunCK(Pro_SendCmd().Run("Get Card ID", "CE 06", 3000, False, DL),"CE 00 00 01"+Case[0], DL)): DL.fails = DL.fails + 1
	if (False == Pro_SendCmd().RunCK(Pro_SendCmd().Run("Card emulation on", "CE 01 01", 3000, False, DL),"CE 00 00 00", DL)): DL.fails = DL.fails + 1
	if (False == DL.ShowMessageBox("","Tap iPhone with NFC on, check if mobile tried to open site "+Case[4],0)):
		DL.fails = DL.fails+1
		DL.setText("RED","Card profile "+Case[0]+" FAIL")


##################################################

# Result Count ####################################
# Warning Count & Fail Count
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )

##################################################

#! Script END