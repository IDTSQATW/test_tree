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


Site1 = [
	["03","0406E104 0023 0000","0021","D101 1D 5501 69647465636870726f64756374732e61746c61737369616e2e6e6574","idtechproducts.atlassian.net"],
	["07","0406E104 001B 0000","0019","D101 15 5501 7777772E696363736F6C7574696F6E732E636F6D","www.iccsolutions.com"]
]

Site2 = [
	["07","0406E104 0023 0000","0021","D101 1D 5501 69647465636870726f64756374732e61746c61737369616e2e6e6574","idtechproducts.atlassian.net"],
	["03","0406E104 001B 0000","0019","D101 15 5501 7777772E696363736F6C7574696F6E732E636F6D","www.iccsolutions.com"]
]


if(False ==  Pro_SendCmd().RunCK(Pro_SendCmd().Run("Card emulation off","CE 01 00",3000,False,DL),"CE 00 00 00",DL)): DL.fails = DL.fails +1
for Case in Site1:
	strProfileID = Case[0]
	strUID = "04 A1A2A3A4"
	strCCLEN = "00 17"
	strT4T = "20"
	strMLe = "00 FF"
	strMLc = "00 FF"
	strNDEFFile = Case[1]
	strPropFile = " 05 06 E1 05 00 0B 00 00"
	strNLEN = Case[2]
	strNDEFMes = Case[3]#len = strNLEN
	strPLEN = "00 09"
	strPropriData = "01 02 03 04 05 06 07 08 09"#len = strPLEN
	CardProfile = strProfileID+strUID+strCCLEN+strT4T+strMLe+strMLc+strNDEFFile+strPropFile+strNLEN+strNDEFMes+strPLEN+strPropriData
	if (False == Pro_SendCmd().RunCK(Pro_SendCmd().Run("Read card profile"+Case[0], "CE 03"+Case[0], 3000, False, DL),"CE 00 00 ??"+CardProfile, DL)): DL.fails = DL.fails + 1
if (DL.fails>0):
	DL.setText("RED","Ensure FW.K.10.01-02_CE-XXCardEmulation_CreateCard.py ran and success before this case")
 	sys.exit()
for Case in Site2:
	strProfileID = Case[0]
	strUID = "04 A1A2A3A4"
	strCCLEN = "00 17"
	strT4T = "20"
	strMLe = "00 FF"
	strMLc = "00 FF"
	strNDEFFile = Case[1]
	strPropFile = " 05 06 E1 05 00 0B 00 00"
	strNLEN = Case[2]
	strNDEFMes = Case[3]#len = strNLEN
	strPLEN = "00 09"
	strPropriData = "01 02 03 04 05 06 07 08 09"#len = strPLEN
	CardProfile = strProfileID+strUID+strCCLEN+strT4T+strMLe+strMLc+strNDEFFile+strPropFile+strNLEN+strNDEFMes+strPLEN+strPropriData
	if (False == Pro_SendCmd().RunCK(Pro_SendCmd().Run("Create card profile"+Case[0], "CE 02"+CardProfile, 3000, False, DL),"CE 00 00 00", DL)): DL.fails = DL.fails + 1
	if (False == Pro_SendCmd().RunCK(Pro_SendCmd().Run("Read card profile"+Case[0], "CE 03"+Case[0], 3000, False, DL),"CE 00 00 ??"+CardProfile, DL)): DL.fails = DL.fails + 1



##################################################

# Result Count ####################################
# Warning Count & Fail Count
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )

##################################################

#! Script END