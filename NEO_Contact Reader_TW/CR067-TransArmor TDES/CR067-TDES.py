#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True
readertype = 0

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''
strKey = '0123456789ABCDEFFEDCBA9876543210'

# Check project type (NEOI or NEOII)
readertype = DL.ShowMessageBox("", "Is this NEOII project?", 0)
if readertype == 1:
	DL.SetWindowText("Green", "*** NEOII project ***")
else:
	DL.SetWindowText("Green", "*** NEOI project ***")

# Check Encryption status(03)
if (Result):
	RetOfStep = DL.SendCommand('Check Encryption status(03)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 03")
		if Result == False:
			DL.SetWindowText("Red", "Please ENABLE data encryption (03)...")

# Encryption Type -- TransArmor TDES
if (Result):
	RetOfStep = DL.SendCommand('2-use TransArmor TDES to encrypt (C7-32)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 00")
		if Result != True:
			Result = DL.SendCommand('0-use TDES to encrypt (C7-32)')
			if (Result):
				Result = DL.SendCommand('2-use TransArmor TDES to encrypt (C7-32)')
				if Result == False:
					DL.SetWindowText("Red", "Please set data key type as TransArmor TDES...")
if (Result):
	RetOfStep = DL.SendCommand('Encryption Type -- TransArmor TDES')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 02")		
		
# Burst mode OFF & Poll on demand		
if (Result):
	if readertype == 1:	
		RetOfStep = DL.SendCommand('Burst mode Off (NEOII)')
	else:
		RetOfStep = DL.SendCommand('Burst mode Off (NEOI)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")

if readertype == 1:	
	# CT config		
	if (Result):
		RetOfStep = DL.SendCommand('60-16 Contact Set ICS Identification (02)')
		if (RetOfStep):
			Result = Result and DL.Check_RXResponse("60 00 00 00")	
	if (Result):
		RetOfStep = DL.SendCommand('60-03 Contact Set Application Data (VISA)')
		if (RetOfStep):
			Result = Result and DL.Check_RXResponse("60 00 00 00")	
	if (Result):
		RetOfStep = DL.SendCommand('60-06 Contact Set Terminal Data (NEOII)')
		if (RetOfStep):
			Result = Result and DL.Check_RXResponse("60 00 00 00")	
	if (Result):
		RetOfStep = DL.SendCommand('60-0A Contact Set CA Public Key')
		if (RetOfStep):
			Result = Result and DL.Check_RXResponse("60 00 00 00")	
else:
	if (Result):
		RetOfStep = DL.SendCommand('60-06 Contact Set Terminal Data (NEOI)')
		if (RetOfStep):
			Result = Result and DL.Check_RXResponse("60 00 00 00")		
		
# cmd 60-10, fallback to MSR, swipe card
if (Result):
	if readertype == 1:
		RetOfStep = DL.SendCommand('Activate Transaction_NEOII')
	else:
		RetOfStep = DL.SendCommand('Activate Transaction_NEOI')
	if (RetOfStep):
		Result = DL.Check_RXResponse("60 63 00 00")
		if (Result):
			if readertype == 0:
				Result = DL.Check_StringAB(DL.Get_RXResponse(3), '56 69 56 4F 74 65 63 68 32 00 61 01 00 10 03 00 00 02 00 45 4E 03 00 81 13 1C 02 00 00 00 23 0F')
			if (Result):	
				if readertype == 0:
					Result = DL.Check_StringAB(DL.Get_RXResponse(5), '56 69 56 4F 74 65 63 68 32 00 60 00')
					sResult=DL.Get_RXResponse(5)
				else:
					Result = DL.Check_StringAB(DL.Get_RXResponse(3), '56 69 56 4F 74 65 63 68 32 00 60 00')
					sResult=DL.Get_RXResponse(3)
				if (Result):	
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


								TR1maskdata1 = "%*6510********"
								TR1maskdata2 = "^CARD/IMAGE"
								TR1maskdata3 = "^1712*************"
								TR1maskdata4 = "?;6510********"
								TR1maskdata5 = "=1712*************"
								TR1plaintextdata1 = "2542363531303030303030303030"
								TR1plaintextdata2 = "5E434152442F494D414745"
								TR1plaintextdata3 = "5E31373132323031"
								TR1plaintextdata4 = "3F3B363531303030303030303030"
								TR1plaintextdata5 = "3D31373132323031"

								TagDFEE25 = DL.GetTLV(sResult,"DFEE25")
								Tag9F39 = DL.GetTLV(sResult,"9F39")
								TagFFEE01 = DL.GetTLV(sResult,"FFEE01")
								TagDFEE26 = DL.GetTLV(sResult,"DFEE26")
								TagDFEF4C = DL.GetTLV(sResult,"DFEF4C")
								TagDFEF4D = DL.GetTLV(sResult,"DFEF4D")
								decDFEF4D = DL.DecryptDLL(0,1, strKey, KSN, TagDFEF4D)	

								# Verify Mask (or clear) track data
								if DL.Check_StringAB(Track1_CardData, TR1maskdata1) and DL.Check_StringAB(Track1_CardData, TR1maskdata2) and DL.Check_StringAB(Track1_CardData, TR1maskdata3) and DL.Check_StringAB(Track1_CardData, TR1maskdata4) and DL.Check_StringAB(Track1_CardData, TR1maskdata5): 
									DL.SetWindowText("Blue", "Track 1 Mask data: PASS")
								else:
									DL.SetWindowText("Red", "Track 1 Mask data: FAIL")
									
								if TRK2 == None or TRK2 == "": 
									DL.SetWindowText("Blue", "Track 2 Mask data: NONE")
								else:
									DL.SetWindowText("Red", "Track 2 Mask data: FAIL")
									
								# Verify Encryption track data	
								if DL.Check_StringAB(TRK1DecryptData, TR1plaintextdata1) and DL.Check_StringAB(TRK1DecryptData, TR1plaintextdata2) and DL.Check_StringAB(TRK1DecryptData, TR1plaintextdata3) and DL.Check_StringAB(TRK1DecryptData, TR1plaintextdata4) and DL.Check_StringAB(TRK1DecryptData, TR1plaintextdata5):
									DL.SetWindowText("Blue", "Track 1 Decryption data: PASS")
								else:
									DL.SetWindowText("Red", "Track 1 Decryption data: FAIL")
									
								if TRK2 == None or TRK2 == "":
									DL.SetWindowText("Blue", "Track 2 Decryption data: NONE")
								else:
									DL.SetWindowText("Red", "Track 2 Decryption data: FAIL")
										
							# Verify specific tags
							Result = DL.Check_StringAB(CardData, '80 4F 6A 00 00 A1 89 01 12')
							if Result == False:
								DL.SetWindowText("Red", "Tag DFEE23: FAIL")
								
							if TagDFEE25 != "0007": 
								DL.SetWindowText("Red", "Tag DFEE25: FAIL")
								
							if Tag9F39 != "80": 
								DL.SetWindowText("Red", "Tag 9F39: FAIL")
								
							if readertype == 1:
								if TagFFEE01 != "DFEE30010C": 
									DL.SetWindowText("Red", "Tag FFEE01: FAIL")
							if readertype == 0:
								if TagFFEE01 != "DF30010C": 
									DL.SetWindowText("Red", "Tag FFEE01: FAIL")	
									
							if TagDFEE26 != "EC06": 
								DL.SetWindowText("Red", "Tag DFEE26: FAIL")
								
							if readertype == 0:	
								if TagDFEF4C != "6A0000000000": 
									DL.SetWindowText("Red", "Tag DFEF4C: FAIL")	
								r1 = DL.Check_StringAB(decDFEF4D, '2542363531303030303030303030')
								r2 = DL.Check_StringAB(decDFEF4D, '5E434152442F494D414745')
								r3 = DL.Check_StringAB(decDFEF4D, '5E31373132323031')
								r4 = DL.Check_StringAB(decDFEF4D, '3F3B363531303030303030303030')
								r5 = DL.Check_StringAB(decDFEF4D, '3D31373132323031')
								if r1 == False or r2 == False or r3 == False or r4 == False or r5 == False:
									DL.SetWindowText("Red", "Tag DFEF4D: FAIL")		
					else:
						DL.SetWindowText("RED", "Parse Card Data Fail")								