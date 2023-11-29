#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''
strKey = 'FEDCBA9876543210F1F1F1F1F1F1F1F1'

# Check project has LCD or not
readertype = DL.ShowMessageBox("", "Does the project has LCD?", 0)
if readertype == 1:
	DL.SetWindowText("Green", "*** The project has LCD ***")
else:
	DL.SetWindowText("Green", "*** The project has NO LCD ***")

# Get DUKPT DEK Attribution based on KeySlot (C7-A3)
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 06 01 02 00 00 00 00")

# Set MSR Secure Parameters (C7-38)
if (Result):
	RetOfStep = DL.SendCommand('Set MSR Secure Parameters (C7-38)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 00")		

# First Response Control (0x63) = enable
if (Result):
	RetOfStep = DL.SendCommand('First Response Control (0x63) = enable')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")			
		
# Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")

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
	RetOfStep = DL.SendCommand('60-06 Contact Set Terminal Data')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('60-0A Contact Set CA Public Key')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")
if (Result):
	RetOfStep = DL.SendCommand('DF7D = 02 (NEO2)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")
		
# cmd 60-10, fallback to MSR, swipe card
if (Result):
	if readertype == 1:
		RetOfStep = DL.SendCommand('Activate Transaction_w LCD')
	if readertype == 0:
		RetOfStep = DL.SendCommand('Activate Transaction_w/o LCD')
	if (RetOfStep):
		Result = DL.Check_RXResponse("60 63 00 00")
		if (Result):
			if readertype == 1:
				Result = DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 60 00')
				if (Result):
					Result = DL.Check_StringAB(DL.Get_RXResponse(1), 'E8 DF EE 25')
					sResult=DL.Get_RXResponse(1)
			if readertype == 0:   
				rx = 3
				Result = DL.Check_StringAB(DL.Get_RXResponse(rx), '56 69 56 4F 74 65 63 68 32 00 60 00')
				if (Result):
					Result = DL.Check_StringAB(DL.Get_RXResponse(rx), 'EC DF EE 25')
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
								TRK1DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK1)
							if len(TRK2)> 0:
								TRK2DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK2)
							if len(TRK3) > 0:
								TRK3DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK3)

						TR1cleardata = "%TRACK17676760707077676760707077676760707077676760707077676760707077676760707?C"
						TR2cleardata = ";2121212121767676070707767676762121212?0"
						TR3cleardata = ";33333333337676760707077676763333333333767676070707767676333333333376767607070776767633333333337676760707?2"
						TagDFEE25 = DL.GetTLV(sResult,"DFEE25")
						Tag9F39 = DL.GetTLV(sResult,"9F39")
						TagFFEE01 = DL.GetTLV(sResult,"FFEE01")
						TagDFEE26 = DL.GetTLV(sResult,"DFEE26")

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
						Result = DL.Check_StringAB(CardData, '83 7F 4F 28 6B 87 00')
						if Result == False:
							DL.SetWindowText("Red", "Tag DFEE23: FAIL")
							
						if TagDFEE25 != "0011": 
							DL.SetWindowText("Red", "Tag DFEE25: FAIL")
						if Tag9F39 != "90": 
							DL.SetWindowText("Red", "Tag 9F39: FAIL")
						if TagFFEE01 != "DFEE30010C": 
							DL.SetWindowText("Red", "Tag FFEE01: FAIL")
						if TagDFEE26 != "EC01": 
							DL.SetWindowText("Red", "Tag DFEE26: FAIL")
				else:
					DL.SetWindowText("RED", "Parse Card Data Fail")							
					
# cmd 60-13
RetOfStep = DL.SendCommand('60-13 Contact Retrieve Transaction Result')
if (RetOfStep):
	DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 60 00 ** EC ** 57 00 5A 00 5F 34 00 5F 20 00 5F 24 00 9F 20 00 5F 25 00 5F 2D 00 50 00 4F 00 84 00 DF EE 23 00 9F 39 00")