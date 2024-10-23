#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True
platformtype = 0

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''
strKey = '0123456789ABCDEFFEDCBA9876543210'

# Check project type (NEOI or NEOII)
platformtype = DL.ShowMessageBox("", "Is this NEOII project?", 0)
if platformtype == 1:
	DL.SetWindowText("Green", "*** NEOII project ***")
else:
	DL.SetWindowText("Green", "*** NEOI project ***")
	
# Check project has LCD or not
lcdtype = DL.ShowMessageBox("", "Does the project has LCD?", 0)
if lcdtype == 1:
	DL.SetWindowText("Green", "*** The project has LCD ***")
else:
	DL.SetWindowText("Green", "*** The project has NO LCD ***")	
	
# Check reader is VP3350 or not
readertype = DL.ShowMessageBox("", "Is this VP3350?", 0)
if readertype == 1:
	DL.SetWindowText("Green", "*** This is VP3350 ***")
else:
	DL.SetWindowText("Green", "*** non-VP3350 reader ***")	

if platformtype == 1:
	# Encryption Type -- TransArmor TDES
	if (Result):
		RetOfStep = DL.SendCommand('C7-A2 TDES DUKPT manage_TransArmor TDES, data key')
		time.sleep(1)
		
	# Check data encryption TYPE is TDES	
	if (Result):
		RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
		if (RetOfStep):
			Result = Result and DL.Check_RXResponse("C7 00 00 06 00 02 00 00 00 00")		

if platformtype == 0:
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
		
# Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")

if platformtype == 1:	
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
	if platformtype == 1:
		if lcdtype == 1:
			RetOfStep = DL.SendCommand('Activate Transaction_NEOII_w/ LCD')
		if lcdtype == 0:
			RetOfStep = DL.SendCommand('Activate Transaction_NEOII_w/o LCD')
	else:
		RetOfStep = DL.SendCommand('Activate Transaction_NEOI')
	if (RetOfStep):
		Result = DL.Check_RXResponse("60 63 00 00")
		if (Result):
			if platformtype == 0:
				Result = DL.Check_RXResponse(3, '56 69 56 4F 74 65 63 68 32 00 61 01 00 10 03 00 00 02 00 45 4E 03 00 81 13 1C 02 00 00 00 23 0F')
			if platformtype == 1:
				if lcdtype == 0:
					Result = DL.Check_RXResponse(4, '56 69 56 4F 74 65 63 68 32 00 61 01 00 10 03 00 00 02 00 ** 03 00 ** 13 1C 02 **')	
			if (Result):	
				if platformtype == 0:
					rx = 5
				if platformtype == 1:
					if lcdtype == 1:
						rx = 3
					if lcdtype == 0:
						rx = 8
				Result = DL.Check_RXResponse(rx, '56 69 56 4F 74 65 63 68 32 00 60 00')
				sResult=DL.Get_RXResponse(rx)
				if (Result):	
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

								TagDFEF4C = DL.GetTLV(sResult,"DFEF4C")
								TagDFEF4D = DL.GetTLV(sResult,"DFEF4D")
								decDFEF4D = DL.DecryptDLL(0,1, strKey, KSN, TagDFEF4D)	

								# Verify Mask (or clear) track data
								if DL.Check_StringAB(Track1_CardData, TR1maskdata1) and DL.Check_StringAB(Track1_CardData, TR1maskdata2) and DL.Check_StringAB(Track1_CardData, TR1maskdata3) and DL.Check_StringAB(Track1_CardData, TR1maskdata4) and DL.Check_StringAB(Track1_CardData, TR1maskdata5): 
									DL.SetWindowText("Blue", "Track 1 Mask data: PASS")
								else:
									DL.fails=DL.fails+1
									DL.SetWindowText("Red", "Track 1 Mask data: FAIL")
									
								if TRK2 == None or TRK2 == "": 
									DL.SetWindowText("Blue", "Track 2 Mask data: NONE")
								else:
									DL.fails=DL.fails+1
									DL.SetWindowText("Red", "Track 2 Mask data: FAIL")
									
								# Verify Encryption track data	
								if DL.Check_StringAB(TRK1DecryptData, TR1plaintextdata1) and DL.Check_StringAB(TRK1DecryptData, TR1plaintextdata2) and DL.Check_StringAB(TRK1DecryptData, TR1plaintextdata3) and DL.Check_StringAB(TRK1DecryptData, TR1plaintextdata4) and DL.Check_StringAB(TRK1DecryptData, TR1plaintextdata5):
									DL.SetWindowText("Blue", "Track 1 Decryption data: PASS")
								else:
									DL.fails=DL.fails+1
									DL.SetWindowText("Red", "Track 1 Decryption data: FAIL")
									
								if TRK2 == None or TRK2 == "":
									DL.SetWindowText("Blue", "Track 2 Decryption data: NONE")
								else:
									DL.fails=DL.fails+1
									DL.SetWindowText("Red", "Track 2 Decryption data: FAIL")
										
							# Verify specific tags
							if DL.Check_RXResponse(rx, '80 4F 6A 00 00 A1 89 01 12') == False:
								DL.fails=DL.fails+1
								DL.SetWindowText("Red", "Tag DFEE23: FAIL")
								
							if DL.Check_RXResponse(rx, "DFEE25 02 0007") == False: 
								DL.fails=DL.fails+1
								DL.SetWindowText("Red", "Tag DFEE25: FAIL")
								
							if DL.Check_RXResponse(rx, "9F39 01 80") == False: 
								DL.fails=DL.fails+1
								DL.SetWindowText("Red", "Tag 9F39: FAIL")
								
							if platformtype == 1:
								if DL.Check_RXResponse(rx, "FFEE01 ** DFEE30010C") == False: 
									DL.fails=DL.fails+1
									DL.SetWindowText("Red", "Tag FFEE01: FAIL")
							if platformtype == 0:
								if DL.Check_RXResponse(rx, "FFEE01 ** DF30010C") == False: 
									DL.fails=DL.fails+1
									DL.SetWindowText("Red", "Tag FFEE01: FAIL")	
									
							if DL.Check_RXResponse(rx, "DFEE26 02 EC06") == False: 
								DL.fails=DL.fails+1
								DL.SetWindowText("Red", "Tag DFEE26: FAIL")
								
							if platformtype == 0:	
								if DL.Check_RXResponse(rx, "DFEF4C 06 6A0000000000") == False: 
									DL.fails=DL.fails+1
									DL.SetWindowText("Red", "Tag DFEF4C: FAIL")	
								r1 = DL.Check_StringAB(decDFEF4D, '2542363531303030303030303030')
								r2 = DL.Check_StringAB(decDFEF4D, '5E434152442F494D414745')
								r3 = DL.Check_StringAB(decDFEF4D, '5E31373132323031')
								r4 = DL.Check_StringAB(decDFEF4D, '3F3B363531303030303030303030')
								r5 = DL.Check_StringAB(decDFEF4D, '3D31373132323031')
								if r1 == False or r2 == False or r3 == False or r4 == False or r5 == False:
									DL.fails=DL.fails+1
									DL.SetWindowText("Red", "Tag DFEF4D: FAIL")		
				else:
					DL.fails=DL.fails+1
else:
	DL.fails=DL.fails+1
                
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )