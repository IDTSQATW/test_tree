#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''
strKey = '0123456789ABCDEFFEDCBA9876543210'

# Objective: to verify 6 test Blackboard card that provided by USAtech

# Check project type (NEOI or NEOII)
readertype = DL.ShowMessageBox("", "Is this NEOII and upward project?", 0)
if readertype == 1:
	DL.SetWindowText("Green", "*** NEOII and upward project ***")
else:
	DL.SetWindowText("Green", "*** NEOI project ***")  

# Check project has LCD or not
lcdtype = DL.ShowMessageBox("", "Does the project has LCD?", 0)
if lcdtype == 1:
	DL.SetWindowText("Green", "*** The project has LCD ***")
else:
	DL.SetWindowText("Green", "*** The project has NO LCD ***")

# Get DUKPT DEK Attribution based on KeySlot (C7-A3)
if readertype == 1:
    if (Result):
        RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("C7 00 00 06 00 00 00 00 00 00")	
			
# Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")

# cmd 02-40, swipe card
if (Result):
	for i in range (1, 7):
		if i == 1:
			if lcdtype == 1:
				RetOfStep = DL.SendCommand('Activate Transaction (Card: USAT Maintenance) w/ LCD')
			if lcdtype == 0:
				if readertype == 1:     #NEOII and upward project
					RetOfStep = DL.SendCommand('Activate Transaction (Card: USAT Maintenance) w/o LCD')
				else:     #NEOI project
					RetOfStep = DL.SendCommand('Activate Transaction (Card: USAT Maintenance) w/ LCD')
		if i == 2:
			if lcdtype == 1:
				RetOfStep = DL.SendCommand('Activate Transaction (Card: Blackboard-Valid card) w/ LCD')
			if lcdtype == 0:
				if readertype == 1:     #NEOII and upward project
					RetOfStep = DL.SendCommand('Activate Transaction (Card: Blackboard-Valid card) w/o LCD')
				else:     #NEOI project
					RetOfStep = DL.SendCommand('Activate Transaction (Card: Blackboard-Valid card) w/ LCD')
		if i == 3:
			if lcdtype == 1:
				RetOfStep = DL.SendCommand('Activate Transaction (Card: Blackboard-Invalid account) w/ LCD')
			if lcdtype == 0:
				if readertype == 1:     #NEOII and upward project
					RetOfStep = DL.SendCommand('Activate Transaction (Card: Blackboard-Invalid account) w/o LCD')
				else:     #NEOI project
					RetOfStep = DL.SendCommand('Activate Transaction (Card: Blackboard-Invalid account) w/ LCD')
		if i == 4:
			if lcdtype == 1:
				RetOfStep = DL.SendCommand('Activate Transaction (Card: Blackboard -$0.00 balance) w/ LCD')
			if lcdtype == 0:
				if readertype == 1:     #NEOII and upward project
					RetOfStep = DL.SendCommand('Activate Transaction (Card: Blackboard -$0.00 balance) w/o LCD')
				else:     #NEOI project
					RetOfStep = DL.SendCommand('Activate Transaction (Card: Blackboard -$0.00 balance) w/ LCD')
		if i == 5:
			if lcdtype == 1:
				RetOfStep = DL.SendCommand('Activate Transaction (Card: Blackboard-Expired) w/ LCD')
			if lcdtype == 0:
				if readertype == 1:     #NEOII and upward project
					RetOfStep = DL.SendCommand('Activate Transaction (Card: Blackboard-Expired) w/o LCD')
				else:     #NEOI project
					RetOfStep = DL.SendCommand('Activate Transaction (Card: Blackboard-Expired) w/ LCD')
		if i == 6:
			if lcdtype == 1:
				RetOfStep = DL.SendCommand('Activate Transaction (Card: Blackboard-lost card) w/ LCD')		
			if lcdtype == 0:
				if readertype == 1:     #NEOII and upward project
					RetOfStep = DL.SendCommand('Activate Transaction (Card: Blackboard-lost card) w/o LCD')
				else:     #NEOI project
					RetOfStep = DL.SendCommand('Activate Transaction (Card: Blackboard-lost card) w/ LCD')
				
		if (RetOfStep):
			if lcdtype == 1:
				rx = 0
				if readertype == 1:     #NEOII and upward project
					Result = DL.Check_RXResponse(rx, "56 69 56 4F 74 65 63 68 32 00 02 00 ** E8 ** DF EE 25 02 00 11 DF EE 23")
				if readertype == 0:     #NEOI project
					Result = DL.Check_RXResponse(rx, "56 69 56 4F 74 65 63 68 32 00 02 00 ** C8 ** DF EE 25 02 00 11 DF EE 23")
			if lcdtype == 0:
				if readertype == 1:     #NEOII and upward project
					rx = 3	
					Result = DL.Check_RXResponse(rx, "56 69 56 4F 74 65 63 68 32 00 02 00 ** E8 ** DF EE 25 02 00 11 DF EE 23")	
				if readertype == 0:     #NEOI project
					rx = 0
					Result = DL.Check_RXResponse(rx, "56 69 56 4F 74 65 63 68 32 00 02 00 ** C8 ** DF EE 25 02 00 11 DF EE 23")
			if (Result):
				if i == 1:
					Result = DL.Check_RXResponse(rx, "02 ** 80 1E 00 1F 00 82 92")
				if i == 2:
					Result = DL.Check_RXResponse(rx, "02 ** 83 1F 25 13 00 83 00")
				if i == 3:
					Result = DL.Check_RXResponse(rx, "02 ** 83 1F 1D 13 00 83 00")
				if i == 4:
					Result = DL.Check_RXResponse(rx, "02 ** 83 1F 28 13 00 83 00")
				if i == 5:
					Result = DL.Check_RXResponse(rx, "02 ** 83 1F 1F 13 00 83 00")
				if i == 6:
					Result = DL.Check_RXResponse(rx, "02 ** 83 1F 17 13 00 83 00")
					
				if (Result):			
					sResult=DL.Get_RXResponse(rx)
					if sResult!=None and sResult!="":
						sResult=sResult.replace(" ","")
						CardData=DL.GetTLV(sResult,"DFEE23")
						bresult = False
						if CardData!=None and CardData!='':
							objectMSR = DL.ParseCardData(CardData, Key)
							EncryptType = DL.Get_EncryptionKeyType_CardData()
							EncryptMode = DL.Get_EncryptionMode_CardData()
							if objectMSR!=None:
								DL.SetWindowText("blue", "Track 1:")
								Track1_CardData = DL.Get_TrackN_CardData(1)
								DL.SetWindowText("blue", "Track 2:")
								Track2_CardData = DL.Get_TrackN_CardData(2)
								DL.SetWindowText("blue", "Track 3:")
								Track3_CardData = DL.Get_TrackN_CardData(3)
								DL.SetWindowText("blue", "Track 1_Enc:")
								TRK1 = DL.Get_EncryptTrackN_CardData(1)
								DL.SetWindowText("blue", "Track 2_Enc:")
								TRK2 = DL.Get_EncryptTrackN_CardData(2)
								DL.SetWindowText("blue", "Track 3_Enc:")
								TRK3 = DL.Get_EncryptTrackN_CardData(3)
								DL.SetWindowText("blue", "KSN:")
								KSN=DL.Get_KSN_CardData()
								if len(TRK1)> 0:
									DL.SetWindowText("blue", "Track 1:")
									TRK1DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK1)
								if len(TRK2)> 0:
									DL.SetWindowText("blue", "Track 2:")
									TRK2DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK2)
								if len(TRK3) > 0:
									DL.SetWindowText("blue", "Track 3:")
									TRK3DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK3)
									
					if i == 1:
						TR2maskdata = ";6396**********1212=3712*****?*"
						TR2plaintextdata = "3B 36 33 39 36 32 31 31 32 30 30 31 30 30 30 31 32 31 32 3D 33 37 31 32 35 34 33 30 32 3F 35"
									
						Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
						if Result != True:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "TR2maskdata: FAIL")
						Result = DL.Check_StringAB(TR2plaintextdata, TRK2DecryptData)
						if Result != True:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "TR2plaintextdata: FAIL")
						
					if i == 2:
						TR1maskdata = "%BLACKBOARD VALID CARD, BAL $999.00?5"					
						TR2maskdata = ";9987770000001220?:"

						Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
						if Result != True:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "TR1maskdata: FAIL")	
						Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
						if Result != True:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "TR2maskdata: FAIL")		

					if i == 3:
						TR1maskdata = "%BLACKBOARD INVALID ACCOUNT?7"					
						TR2maskdata = ";9987770000001222?8"

						Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
						if Result != True:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "TR1maskdata: FAIL")	
						Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
						if Result != True:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "TR2maskdata: FAIL")

					if i == 4:
						TR1maskdata = "%BLACKBOARD VALID CARD BALANCE = $0.00?$"					
						TR2maskdata = ";9987770000001221?;"

						Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
						if Result != True:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "TR1maskdata: FAIL")	
						Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
						if Result != True:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "TR2maskdata: FAIL")

					if i == 5:
						TR1maskdata = "%BLACKBOARD EXPIRED BAL $5.00? "					
						TR2maskdata = ";9987770000001224?>"

						Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
						if Result != True:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "TR1maskdata: FAIL")	
						Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
						if Result != True:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "TR2maskdata: FAIL")

					if i == 6:
						TR1maskdata = "%BLACKBOARD LOST CARD?7"					
						TR2maskdata = ";9987770000001223?9"

						Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
						if Result != True:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "TR1maskdata: FAIL")	
						Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
						if Result != True:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "TR2maskdata: FAIL")
				else:
					DL.fails=DL.fails+1
else:
	DL.fails=DL.fails+1
                            
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )