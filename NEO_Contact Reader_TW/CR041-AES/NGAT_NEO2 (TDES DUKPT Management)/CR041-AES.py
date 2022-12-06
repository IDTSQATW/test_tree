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
readertype = DL.ShowMessageBox("", "Is this NEOII or upward project?", 0)
if readertype == 1:
	DL.SetWindowText("Green", "*** NEOII project ***")
else:
	DL.SetWindowText("Green", "*** NEOI project ***")
	
# Check project has LCD or not
lcdtype = DL.ShowMessageBox("", "Does the project has LCD?", 0)
if lcdtype == 1:
	DL.SetWindowText("Green", "*** The project has LCD ***")
else:
	DL.SetWindowText("Green", "*** The project has NO LCD ***")

if readertype == 1:     # NEO2 or upward
	# Check data encryption TYPE is TDES	
	if (Result):
		RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
		if (RetOfStep):
			Result = DL.Check_RXResponse("C7 00 00 06 00 01 00 00 00 00")
else:     # NEO1
	# Get Data Encryption (C7-37)
	if (Result):
		RetOfStep = DL.SendCommand('Get Data Encryption (C7-37)')
		if (RetOfStep):
			Result = DL.Check_RXResponse("C7 00 00 01 03")
			if Result == False:
				DL.SetWindowText("Red", "Please ENABLE data encryption (03)...")
	# Encryption Type -- AES
	if (Result):
		RetOfStep = DL.SendCommand('Encryption Type -- AES')
		if (RetOfStep):
			Result = DL.Check_RXResponse("C7 00 00 01 01")	
			if Result == False:
				DL.SetWindowText("Red", "Please set data key type as AES...")	
				
# Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")
		
if readertype == 0:	     # NEO1
	# CT config		
	if (Result):
		RetOfStep = DL.SendCommand('60-06 Contact Set Terminal Data (NEOI)')
		if (RetOfStep):
			Result = DL.Check_RXResponse("60 00 00 00")		
	if (Result):
		RetOfStep = DL.SendCommand('60-03 Contact Set Application Data (VISA)')
		if (RetOfStep):
			Result = DL.Check_RXResponse("60 00 00 00")		
	if (Result):
		RetOfStep = DL.SendCommand('60-0A Contact Set CA Public Key')
		if (RetOfStep):
			Result = DL.Check_RXResponse("60 00 00 00")		
		
# cmd 60-10, fallback to MSR, swipe card
if (Result):
	if readertype == 1:     # NEO2 or upward
		if lcdtype == 1:
			RetOfStep = DL.SendCommand('Activate Transaction_NEOII w/ LCD')
		if lcdtype == 0:
			RetOfStep = DL.SendCommand('Activate Transaction_NEOII w/o LCD')
	else:     # NEO1
		RetOfStep = DL.SendCommand('Activate Transaction_NEOI')
	if (RetOfStep):
		Result = DL.Check_RXResponse("60 63 00 00")
		if (Result):
			if readertype == 0:     # NEO1
				Result = DL.Check_RXResponse(2, '56 69 56 4F 74 65 63 68 32 00 61 01 00 10 03 00 00 02 00 ** 03 00 ** 0E 1C')
				if (Result):
					Result = DL.Check_RXResponse(4, '56 69 56 4F 74 65 63 68 32 00 61 01 00 10 03 00 00 02 00 ** 03 00 ** 13 1C')
					if (Result):
						Result = DL.Check_RXResponse(6, '56 69 56 4F 74 65 63 68 32 00 60 00')
						if (Result):
							Result = DL.Check_RXResponse(6, 'CA ** DF EE 25')
				sResult=DL.Get_RXResponse(6)
			if readertype == 1:	     # NEO2 or upward
				if lcdtype == 1:
					Result = DL.Check_RXResponse(5, '56 69 56 4F 74 65 63 68 32 00 60 00')
					if (Result):
						Result = DL.Check_RXResponse(5, 'EA DF EE 25')
					sResult=DL.Get_RXResponse(5)
				if lcdtype == 0:	
					Result = DL.Check_RXResponse(2, '56 69 56 4F 74 65 63 68 32 00 61 01 00 10 03 00 00 02 00 ** 03 00 ** 0E 1C')
					if (Result):
						Result = DL.Check_RXResponse(5, '56 69 56 4F 74 65 63 68 32 00 61 01 00 10 03 00 00 02 00 ** 03 00 ** 13 1C')
						if (Result):
							Result = DL.Check_RXResponse(6, '56 69 56 4F 74 65 63 68 32 00 60 00')
							if (Result):
								Result = DL.Check_RXResponse(6, 'E8 ** DF EE 25')
					sResult=DL.Get_RXResponse(6)
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
							TR1maskdata3 = "^1712************"
							TR1maskdata4 = "?*"
							
							TR2maskdata1 = ";6510********"
							TR2maskdata2 = "=1712************"
							TR2maskdata3 = "?*"
							
							TR1plaintextdata1 = "2542363531303030303030303030"
							TR1plaintextdata2 = "5E434152442F494D414745"
							TR1plaintextdata3 = "5E31373132323031"
							
							TR2plaintextdata1 = "3B363531303030303030303030"
							TR2plaintextdata2 = "3D31373132323031"
							
							TagDFEE25 = DL.GetTLV(sResult,"DFEE25")
							Tag9F39 = DL.GetTLV(sResult,"9F39")
							TagFFEE01 = DL.GetTLV(sResult,"FFEE01")
							TagDFEE26 = DL.GetTLV(sResult,"DFEE26")
							TagDFEF4C = DL.GetTLV(sResult,"DFEF4C")
							TagDFEF4D = DL.GetTLV(sResult,"DFEF4D")
							decDFEF4D = DL.DecryptDLL(0,2, strKey, KSN, TagDFEF4D)	

							# Verify Mask (or clear) track data
							if DL.Check_StringAB(Track1_CardData, TR1maskdata1) and DL.Check_StringAB(Track1_CardData, TR1maskdata2) and DL.Check_StringAB(Track1_CardData, TR1maskdata3) and DL.Check_StringAB(Track1_CardData, TR1maskdata4): 
								DL.SetWindowText("Blue", "Track 1 Mask data: PASS")
							else:
								DL.SetWindowText("Red", "Track 1 Mask data: FAIL")
							if DL.Check_StringAB(Track2_CardData, TR2maskdata1) and DL.Check_StringAB(Track2_CardData, TR2maskdata2) and DL.Check_StringAB(Track2_CardData, TR2maskdata3): 
								DL.SetWindowText("Blue", "Track 2 Mask data: PASS")
							else:
								DL.SetWindowText("Red", "Track 2 Mask data: FAIL")
								
							# Verify Encryption track data	
							if DL.Check_StringAB(TRK1DecryptData, TR1plaintextdata1) and DL.Check_StringAB(TRK1DecryptData, TR1plaintextdata2) and DL.Check_StringAB(TRK1DecryptData, TR1plaintextdata3): 
								DL.SetWindowText("Blue", "Track 1 Decryption data: PASS")
							else:
								DL.SetWindowText("Red", "Track 1 Decryption data: FAIL")
							if DL.Check_StringAB(TRK2DecryptData, TR2plaintextdata1) and DL.Check_StringAB(TRK2DecryptData, TR2plaintextdata2): 
								DL.SetWindowText("Blue", "Track 2 Decryption data: PASS")
							else:
								DL.SetWindowText("Red", "Track 2 Decryption data: FAIL")
										
							# Verify specific tags
							if DL.Check_StringAB(CardData, '80 1F 44 28 00 B3 9B') == False:
								DL.SetWindowText("Red", "Tag DFEE23: FAIL")
								
							if TagDFEE25 != "0007": 
								DL.SetWindowText("Red", "Tag DFEE25: FAIL")
							if Tag9F39 != "80": 
								DL.SetWindowText("Red", "Tag 9F39: FAIL")
							if readertype == 1:		     # NEO2 or upward
								if TagFFEE01 != "DFEE30010C": 
									DL.SetWindowText("Red", "Tag FFEE01: FAIL")
								if lcdtype == 1:	
									if TagDFEE26 != "EA01": 
										DL.SetWindowText("Red", "Tag DFEE26: FAIL")
								if lcdtype == 0:	
									if TagDFEE26 != "E800":
										DL.SetWindowText("Red", "Tag DFEE26: FAIL")
							if readertype == 0:     # NEO1
								if TagFFEE01 != "DF30010C": 
									DL.SetWindowText("Red", "Tag FFEE01: FAIL")	
								if TagDFEE26 != "CA": 
									DL.SetWindowText("Red", "Tag DFEE26: FAIL")	
								if TagDFEF4C != "002700000000": 
									DL.SetWindowText("Red", "Tag DFEF4C: FAIL")	
								if DL.Check_StringAB(decDFEF4D, '3B36353130303030') == False:
									DL.SetWindowText("Red", "Tag DFEF4D: FAIL")

if readertype == 1:	     # NEO2 or upward								
	# cmd 60-13
	RetOfStep = DL.SendCommand('60-13 Contact Retrieve Transaction Result')
	if (RetOfStep):
		if lcdtype == 1:
			Result = Result and DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 60 00 ** EA ** 57 00 5A 00 5F 34 00 5F 20 00 5F 24 00 9F 20 00 5F 25 00 5F 2D 00 50 00 4F 00 84 00 DF EE 23 00 9F 39 00")		
		if lcdtype == 0:
			Result = Result and DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 60 00 ** E8 ** 57 00 5A 00 5F 34 00 5F 20 00 5F 24 00 9F 20 00 5F 25 00 5F 2D 00 50 00 4F 00 84 00 DF EE 23 00 9F 39 00")				