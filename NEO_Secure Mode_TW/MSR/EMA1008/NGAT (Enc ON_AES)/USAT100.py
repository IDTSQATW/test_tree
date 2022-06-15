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

# Encryption status verification		
if (Result):
	RetOfStep = DL.SendCommand('Get Data Encryption (C7-37) = 03')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 03")	
if (Result):
	RetOfStep = DL.SendCommand('Get account DUKPT encryption type (C7-33) = AES')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 01")
		
# Set MSR Secure Parameters (C7-38)
if (Result):
	RetOfStep = DL.SendCommand('Set MSR Secure Parameters (C7-38)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 00")	
		
# Burst mode OFF & Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Burst mode Off')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")

# cmd 02-40, swipe card
if (Result):
	for i in range (1, 7):
		if i == 1:
			RetOfStep = DL.SendCommand('Activate Transaction (Card: USAT Maintenance)')
		if i == 2:
			RetOfStep = DL.SendCommand('Activate Transaction (Card: Blackboard-Valid card)')
		if i == 3:
			RetOfStep = DL.SendCommand('Activate Transaction (Card: Blackboard-Invalid account)')
		if i == 4:
			RetOfStep = DL.SendCommand('Activate Transaction (Card: Blackboard -$0.00 balance)')
		if i == 5:
			RetOfStep = DL.SendCommand('Activate Transaction (Card: Blackboard-Expired)')
		if i == 6:
			RetOfStep = DL.SendCommand('Activate Transaction (Card: Blackboard-lost card)')
				
		if (RetOfStep):
			Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EA DF EE 25 02 00 11 DF EE 23")	
			if (Result):
				if i == 1:
					Result = DL.Check_RXResponse("02 ** 80 1E 00 1F 00 92 92")
				if i == 2:
					Result = DL.Check_RXResponse("02 ** 83 1F 25 13 00 93 00")
				if i == 3:
					Result = DL.Check_RXResponse("02 ** 83 1F 1D 13 00 93 00")
				if i == 4:
					Result = DL.Check_RXResponse("02 ** 83 1F 28 13 00 93 00")
				if i == 5:
					Result = DL.Check_RXResponse("02 ** 83 1F 1F 13 00 93 00")
				if i == 6:
					Result = DL.Check_RXResponse("02 ** 83 1F 17 13 00 93 00")
					
				if (Result):			
					sResult=DL.Get_RXResponse(0)
					if sResult!=None and sResult!="":
						sResult=sResult.replace(" ","")
						CardData=DL.GetTLV(sResult,"DFEE23")
						bresult = False
						if CardData!=None and CardData!='':
							objectMSR = DL.ParseCardData(CardData ,bresult,Key,MacKey)
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
									TRK1DecryptData = TRK1DecryptData[0:((objectMSR[0].msr_track1Length)*2)]
								if len(TRK2)> 0:
									DL.SetWindowText("blue", "Track 2:")
									TRK2DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK2)
									TRK2DecryptData = TRK2DecryptData[0:((objectMSR[0].msr_track2Length)*2)]
								if len(TRK3) > 0:
									DL.SetWindowText("blue", "Track 3:")
									TRK3DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK3)
									TRK3DecryptData = TRK3DecryptData[0:((objectMSR[0].msr_track3Length)*2)]
									
					if i == 1:
						TR2maskdata = ";6396**********1212=3712*****?*"
						TR2plaintextdata = "3B 36 33 39 36 32 31 31 32 30 30 31 30 30 30 31 32 31 32 3D 33 37 31 32 35 34 33 30 32 3F 35"
									
						Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
						if Result != True:
							DL.SetWindowText("red", "TR2maskdata: FAIL")
						Result = DL.Check_StringAB(TR2plaintextdata, TRK2DecryptData)
						if Result != True:
							DL.SetWindowText("red", "TR2plaintextdata: FAIL")
						
					if i == 2:
						TR1maskdata = "%BLACKBOARD VALID CARD, BAL $999.00?5"					
						TR2maskdata = ";9987770000001220?:"

						Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
						if Result != True:
							DL.SetWindowText("red", "TR1maskdata: FAIL")	
						Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
						if Result != True:
							DL.SetWindowText("red", "TR2maskdata: FAIL")		

					if i == 3:
						TR1maskdata = "%BLACKBOARD INVALID ACCOUNT?7"					
						TR2maskdata = ";9987770000001222?8"

						Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
						if Result != True:
							DL.SetWindowText("red", "TR1maskdata: FAIL")	
						Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
						if Result != True:
							DL.SetWindowText("red", "TR2maskdata: FAIL")

					if i == 4:
						TR1maskdata = "%BLACKBOARD VALID CARD BALANCE = $0.00?$"					
						TR2maskdata = ";9987770000001221?;"

						Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
						if Result != True:
							DL.SetWindowText("red", "TR1maskdata: FAIL")	
						Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
						if Result != True:
							DL.SetWindowText("red", "TR2maskdata: FAIL")

					if i == 5:
						TR1maskdata = "%BLACKBOARD EXPIRED BAL $5.00? "					
						TR2maskdata = ";9987770000001224?>"

						Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
						if Result != True:
							DL.SetWindowText("red", "TR1maskdata: FAIL")	
						Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
						if Result != True:
							DL.SetWindowText("red", "TR2maskdata: FAIL")

					if i == 6:
						TR1maskdata = "%BLACKBOARD LOST CARD?7"					
						TR2maskdata = ";9987770000001223?9"

						Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
						if Result != True:
							DL.SetWindowText("red", "TR1maskdata: FAIL")	
						Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
						if Result != True:
							DL.SetWindowText("red", "TR2maskdata: FAIL")