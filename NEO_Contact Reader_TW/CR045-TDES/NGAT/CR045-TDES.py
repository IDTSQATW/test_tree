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
		Result = Result and DL.Check_RXResponse("C7 00 00 06 00 00 00 00 00 00")	
		
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
				rx = 4
				Result = DL.Check_StringAB(DL.Get_RXResponse(rx), '56 69 56 4F 74 65 63 68 32 00 60 00')
				if (Result):
					Result = DL.Check_StringAB(DL.Get_RXResponse(rx), 'E8 DF EE 25')		
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

						TR2maskdata = ";4761********0010=2012****************?*"
						TR2plaintextdata = "3B343736313733393030313031303031303D32303132313230303031323333393930303033313F32"
						TagDFEE25 = DL.GetTLV(sResult,"DFEE25")
						Tag9F39 = DL.GetTLV(sResult,"9F39")
						TagFFEE01 = DL.GetTLV(sResult,"FFEE01")
						TagDFEE26 = DL.GetTLV(sResult,"DFEE26")

						# Verify Mask (or clear) track data
						if TR2maskdata == Track2_CardData: 
							DL.SetWindowText("Blue", "Track 2 Mask data: PASS")
						else:
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Track 2 Mask data: FAIL")
							
						# Verify Encryption track data	
						if TR2plaintextdata == TRK2DecryptData: 
							DL.SetWindowText("Blue", "Track 2 Decryption data: PASS")
						else:
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Track 2 Decryption data: FAIL")
									
						# Verify specific tags
						Result = DL.Check_StringAB(CardData, '80 17 00 28 00 82 92')
						if Result == False:
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag DFEE23: FAIL")
							
						if TagDFEE25 != "0011": 
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag DFEE25: FAIL")
						if Tag9F39 != "90": 
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag 9F39: FAIL")
						if TagFFEE01 != "DFEE30010C": 
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag FFEE01: FAIL")
						if TagDFEE26 != "E800": 
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag DFEE26: FAIL")
			else:
				DL.fails=DL.fails+1
# cmd 60-13
RetOfStep = DL.SendCommand('60-13 Contact Retrieve Transaction Result')
if (RetOfStep):
	Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 60 00 ** E8 ** 57 00 5A 00 5F 34 00 5F 20 00 5F 24 00 9F 20 00 5F 25 00 5F 2D 00 50 00 4F 00 84 00 DF EE 23 00 9F 39 00")
	if Result == False:
		DL.fails=DL.fails+1	    
    
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )