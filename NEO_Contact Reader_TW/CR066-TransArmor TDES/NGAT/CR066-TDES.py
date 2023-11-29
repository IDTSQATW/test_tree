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
lcdtype = DL.ShowMessageBox("", "Does the project has LCD?", 0)
if lcdtype == 1:
	DL.SetWindowText("Green", "*** The project has LCD ***")
else:
	DL.SetWindowText("Green", "*** The project has NO LCD ***")

# Encryption Type -- TransArmor TDES
if (Result):
	RetOfStep = DL.SendCommand('C7-A2 TDES DUKPT manage_TransArmor TDES, data key')
	time.sleep(1)
	
# Check data encryption TYPE is TDES	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 06 00 02 00 00 00 00")		
		
# Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")
		
# cmd 60-10, swipe card
if (Result):
	if lcdtype == 1:
		RetOfStep = DL.SendCommand('Activate Transaction_w/ LCD')
	if lcdtype == 0:
		RetOfStep = DL.SendCommand('Activate Transaction_w/o LCD')	
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 63 00 00")
		if lcdtype == 1:
			rx = 1
		if lcdtype == 0:
			rx = 3
		alldata = DL.Get_RXResponse(rx)
		if alldata!=None and alldata!="":
			alldata=alldata.replace(" ","")
			CardData=DL.GetTLV(alldata,"DFEE23")
			if CardData!=None and CardData!='':
				objectMSR = DL.ParseCardData(CardData,Key)
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

					# Track 1
					TR1maskdata = "%*4547********0000^LLIBRE ROBERT-GUILLERMO ^1102***************************?;4547********0000=1102***************?"	
					TR1plaintextdata = "25 42 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 5E 4C 4C 49 42 52 45 20 52 4F 42 45 52 54 2D 47 55 49 4C 4C 45 52 4D 4F 20 5E 31 31 30 32 31 30 31 30 30 30 30 30 30 30 34 30 30 30 30 30 30 30 33 30 36 30 30 30 30 30 30 3F 3B 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 31 31 30 32 31 30 31 30 30 30 30 30 33 30 36 30 30 30 30 3F"
									
					Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
					if Result != True:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "TR1maskdata: FAIL")
					Result = DL.Check_StringAB(TR1plaintextdata, TRK1DecryptData)
					if Result != True:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "TR1plaintextdata: FAIL")

					TR3maskdata = ";**4547********0000=***********************************************************************************?"
					TR3plaintextdata = "3B 30 31 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 37 39 37 38 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 33 30 31 39 30 31 38 30 34 30 32 30 30 30 31 31 30 32 34 3D 33 30 32 35 30 30 30 31 31 34 31 34 30 31 30 35 38 35 39 38 3D 3D 31 3D 30 30 30 30 30 30 32 36 30 30 30 30 30 30 30 30 30 30 30 30 3F"
					
					Result = DL.Check_StringAB(TR3maskdata, Track3_CardData)
					if Result != True:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "TR3maskdata: FAIL")
					Result = DL.Check_StringAB(TR3plaintextdata, TRK3DecryptData)
					if Result != True:
						DL.fails=DL.fails+1
						DL.SetWindowText("red", "TR3plaintextdata: FAIL")										
					# Tags DFEE25/ 9F39/ FFEE01/ DFEE26
					if DL.Check_RXResponse(rx, "DFEE25 02 0011") == False: 
						DL.fails=DL.fails+1
						DL.SetWindowText("Red", "Tag DFEE25: FAIL")
						
					if DL.Check_RXResponse(rx, "9F39 01 90") == False: 
						DL.fails=DL.fails+1
						DL.SetWindowText("Red", "Tag 9F39: FAIL")
		
					if DL.Check_RXResponse(rx, "FFEE01 ** DFEE30010C") == False: 
						DL.fails=DL.fails+1
						DL.SetWindowText("Red", "Tag FFEE01: FAIL")
					if DL.Check_RXResponse(rx, "DFEE26 02 EC06") == False: 
						DL.fails=DL.fails+1
						DL.SetWindowText("Red", "Tag DFEE26: FAIL")
else:
	DL.fails=DL.fails+1
                        
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )