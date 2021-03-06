#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''

# Get Data Encryption Enable Flag (C7-37)
if (Result):
	RetOfStep = DL.SendCommand('Get Data Encryption Enable Flag (C7-37)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 03")
		
# Encryption Type -- TransArmor TDES
if (Result):
	RetOfStep = DL.SendCommand('2-use TransArmor TDES to encrypt (C7-32)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 00")
		if Result != True:
			Result = DL.SendCommand('0-use TDES to encrypt (C7-32)')
			if (Result):
				Result = DL.SendCommand('2-use TransArmor TDES to encrypt (C7-32)')
		
# Burst mode OFF		
if (Result):
	RetOfStep = DL.SendCommand('Burst mode Off')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	
		
# Poll on Demand		
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00")	

# cmd 02-40, swipe Discover card
if (Result):
	Result = DL.SendCommand('Activate Transaction')
	if (Result):
		Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EC DF EE 25 02 00 11 DF EE 23 ** 02 ** 80 4F 6A 00 00 A1 89 01 12")
		sResult=DL.Get_RXResponse(0)
			
		if Result == True and sResult!=None and sResult!="":
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
							
					Tag9F39 = DL.GetTLV(sResult,"9F39")
					TagFFEE01 = DL.GetTLV(sResult,"FFEE01")
					TagDFEE26 = DL.GetTLV(sResult,"DFEE26")
								
					# Verify specific tags
					Result = DL.Check_StringAB(Tag9F39, '90')
					if Result != True:
						DL.SetWindowText("red", "Tag9F39: FAIL")	
						
					Result = DL.Check_StringAB(TagFFEE01, 'DFEE30010C')
					if Result != True:
						DL.SetWindowText("red", "TagFFEE01: FAIL")	
						
					Result = DL.Check_StringAB(TagDFEE26, 'EC06')
					if Result != True:
						DL.SetWindowText("red", "TagDFEE26: FAIL")	
																								
					# Transaction result verification
					TR1maskdata = "%*6510********0026^CARD/IMAGE 03             ^1712****************?;6510********0026=1712****************?"
					TR1plaintextdata = "25 42 36 35 31 30 30 30 30 30 30 30 30 30 30 30 32 36 5E 43 41 52 44 2F 49 4D 41 47 45 20 30 33 20 20 20 20 20 20 20 20 20 20 20 20 20 5E 31 37 31 32 32 30 31 31 30 30 30 30 32 31 30 30 30 30 30 30 3F 3B 36 35 31 30 30 30 30 30 30 30 30 30 30 30 32 36 3D 31 37 31 32 32 30 31 31 30 30 30 30 32 31 30 30 30 30 30 30 3F"
									
					Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
					if Result != True:
						DL.SetWindowText("red", "TR1maskdata: FAIL")

					Result = DL.Check_StringAB(TR1plaintextdata, TRK1DecryptData)
					if Result != True:
						DL.SetWindowText("red", "TR1plaintextdata: FAIL")
									
			else:
				DL.SetWindowText("RED", "Parse Card Data Fail")