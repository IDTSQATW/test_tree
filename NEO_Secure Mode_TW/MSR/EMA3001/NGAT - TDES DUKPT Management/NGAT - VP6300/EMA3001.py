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
		
# Get Encryption Type -- AES(C7-33)
if (Result):
	RetOfStep = DL.SendCommand('Get Encryption Type -- AES(C7-33)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 01")	
		
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
		Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EA ** DF EE 25 02 00 11 DF EE 23 ** 02 ** 80 37 00 28 6B B6 B6")
		sResult=DL.Get_RXResponse(0)
			
		if Result == True and sResult!=None and sResult!="":
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
							
					Tag9F39 = DL.GetTLV(sResult,"9F39")
					TagFFEE01 = DL.GetTLV(sResult,"FFEE01")
					TagDFEE26 = DL.GetTLV(sResult,"DFEE26")
								
					# Verify specific tags
					Result = DL.Check_StringAB(Tag9F39, '90')
					if Result != True:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "Tag9F39: FAIL")	
						
					Result = DL.Check_StringAB(TagFFEE01, 'DFEE30010C')
					if Result != True:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "TagFFEE01: FAIL")	
						
					Result = DL.Check_StringAB(TagDFEE26, 'EA01')
					if Result != True:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "TagDFEE26: FAIL")	
																								
					# Transaction result verification
					TR2maskdata = ";6725***********0066=1812*************?*"
					TR2plaintextdata = "3B 36 37 32 35 32 30 30 31 31 33 35 32 39 30 38 30 30 36 36 3D 31 38 31 32 32 30 31 32 35 32 37 37 37 30 30 30 30 3F 33"
									
					Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
					if Result != True:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "TR2maskdata: FAIL")

					Result = DL.Check_StringAB(TR2plaintextdata, TRK2DecryptData)
					if Result != True:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "TR2plaintextdata: FAIL")

					# Transaction result verification
					TR3maskdata = ";**5920**0550=*******************************************************************************************?*"
					TR3plaintextdata = "3B 30 31 35 39 32 30 30 35 30 35 35 30 3D 31 33 35 32 39 30 38 30 30 36 39 3D 32 38 30 39 35 34 30 30 35 30 30 30 30 30 30 34 32 37 31 30 31 33 30 32 34 33 34 35 30 32 30 30 30 30 30 31 38 31 32 37 30 30 30 30 30 30 30 30 30 3D 3D 31 3D 30 30 30 30 34 31 35 39 39 37 33 36 35 32 32 36 30 30 30 30 30 30 30 30 30 30 3F 36"
									
					Result = DL.Check_StringAB(TR3maskdata, Track3_CardData)
					if Result != True:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "TR3maskdata: FAIL")

					Result = DL.Check_StringAB(TR3plaintextdata, TRK3DecryptData)
					if Result != True:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "TR3plaintextdata: FAIL")
else:
	DL.fails=DL.fails+1

if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )