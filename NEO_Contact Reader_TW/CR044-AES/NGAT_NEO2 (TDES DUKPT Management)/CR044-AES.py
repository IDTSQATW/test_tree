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

# Check reader is VP3350 or not
lcdtype = DL.ShowMessageBox("", "Is this VP3350?", 0)
if lcdtype == 1:
	DL.SetWindowText("Green", "*** This is VP3350 ***")
	RetOfStep = DL.SendCommand('0105 do not use LCD')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")
else:
	DL.SetWindowText("Green", "*** non-VP3350 reader ***")

# Check data encryption TYPE is TDES	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 06 00 01 00 00 00 00")

# First Response Control (0x63) = enable
if (Result):
	RetOfStep = DL.SendCommand('First Response Control (0x63) = enable')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")			
		
# Burst mode OFF & Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Burst mode Off')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")
		
# cmd 60-10, fallback to MSR, swipe card
if (Result):
	RetOfStep = DL.SendCommand('Activate Transaction')
	if (RetOfStep):
		Result = DL.Check_RXResponse("60 63 00 00")
		if (Result):
			Result = DL.Check_RXResponse(1, '56 69 56 4F 74 65 63 68 32 00 60 00')
			if (Result):	
				sResult=DL.Get_RXResponse(1)
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
								# TRK1DecryptData = TRK1DecryptData[0:((objectMSR[0].msr_track1Length)*2)]
							if len(TRK2)> 0:
								DL.SetWindowText("blue", "Track 2:")
								TRK2DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK2)
								# TRK2DecryptData = TRK2DecryptData[0:((objectMSR[0].msr_track2Length)*2)]
							if len(TRK3) > 0:
								DL.SetWindowText("blue", "Track 3:")
								TRK3DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK3)
								# TRK3DecryptData = TRK3DecryptData[0:((objectMSR[0].msr_track3Length)*2)]

							TR1cleardata = "%TRACK17676760707077676760707077676760707077676760707077676760707077676760707?C"
							TR2cleardata = ";2121212121767676070707767676762121212?0"
							TR3cleardata = ";33333333337676760707077676763333333333767676070707767676333333333376767607070776767633333333337676760707?2"

							# Verify Mask (or clear) track data
							if TR1cleardata == Track1_CardData: 
								DL.SetWindowText("Blue", "Track 1 Clear data: PASS")
							else:
								DL.SetWindowText("Red", "Track 1 Clear data: FAIL")
							if TR2cleardata == Track2_CardData: 
								DL.SetWindowText("Blue", "Track 2 Clear data: PASS")
							else:
								DL.SetWindowText("Red", "Track 2 Clear data: FAIL")
							if TR3cleardata == Track3_CardData: 
								DL.SetWindowText("Blue", "Track 3 Clear data: PASS")
							else:
								DL.SetWindowText("Red", "Track 3 Clear data: FAIL")
										
							# Verify specific tags
							Result = DL.Check_StringAB(CardData, '83 3F 4F 28 6B 97 00')
							if Result == False:
								DL.SetWindowText("Red", "Tag DFEE23: FAIL")
								
							if DL.Check_RXResponse(1, " DFEE25 02 0011") == False: 
								DL.SetWindowText("Red", "Tag DFEE25: FAIL")
							if DL.Check_RXResponse(1, "9F39 01 90") == False: 
								DL.SetWindowText("Red", "Tag 9F39: FAIL")
							if DL.Check_RXResponse(1, "FFEE01 ** DFEE30010C") == False: 
								DL.SetWindowText("Red", "Tag FFEE01: FAIL")
							if DL.Check_RXResponse(1, "DFEE26 02 EA00") == False: 
								DL.SetWindowText("Red", "Tag DFEE26: FAIL")
					
# cmd 60-13
RetOfStep = DL.SendCommand('60-13 Contact Retrieve Transaction Result')
if (RetOfStep):
	DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 60 00 ** EA ** 57 00 5A 00 5F 34 00 5F 20 00 5F 24 00 9F 20 00 5F 25 00 5F 2D 00 50 00 4F 00 84 00 DF EE 23 00 9F 39 00")
	
if lcdtype == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")			