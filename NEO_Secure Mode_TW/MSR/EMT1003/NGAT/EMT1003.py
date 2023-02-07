#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''

# Objective: to verify MSR w/ specific card (T2 + T3 data only)

# Check project has LCD or not
lcdtype = DL.ShowMessageBox("", "Does the project has LCD?", 0)
if lcdtype == 1:
	DL.SetWindowText("Green", "*** The project has LCD ***")
else:
	DL.SetWindowText("Green", "*** The project has NO LCD ***")

# Check data encryption TYPE is TDES	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 06 00 00 00 00 00 00")
		
# Poll on Demand		
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00")	

# Activate Transaction -- ISO4909 (3T)
if (Result):
	if lcdtype == 1:
		Result = DL.SendCommand('Activate Transaction -- ISO4909 (3T) w/ LCD')
	if lcdtype == 0:
		Result = DL.SendCommand('Activate Transaction -- ISO4909 (3T) w/o LCD')		
	if (Result):
		if lcdtype == 1:
			rx = 0
		if lcdtype == 0:
			rx = 1			
		Result = DL.Check_RXResponse(rx, "56 69 56 4F 74 65 63 68 32 00 02 00 ** E8 ** DF EE 25 02 00 11 DF EE 23 ** 02 ** 80 37 00 28 69 86 B6")
		sResult=DL.Get_RXResponse(rx)
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
						
					Result = DL.Check_StringAB(TagDFEE26, 'E800')
					if Result != True:
						DL.SetWindowText("red", "TagDFEE26: FAIL")	
																								
					# Transaction result verification
					TR2maskdata = ";6225********2330=4912****************?*"
					TR3maskdata = ";**6225********2330=***********************************************************************************?*"
					TR2plaintextdata = "3B363232353838373331353337323333303D34393132313230303737373037373630383737373F3F"
					TR3plaintextdata = "33B3939363232353838373331353337323333303D313536313536303530303035303030303030313031353630383737373231343030303034393132303D373331353337323333303D3030303030303030303D3038303030303030373331303030303030303030303F3F00000000000000"
									
					Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
					if Result != True:
						DL.SetWindowText("red", "TR2maskdata: FAIL")
					Result = DL.Check_StringAB(TR2plaintextdata, TRK2DecryptData)
					if Result != True:
						DL.SetWindowText("red", "TR2plaintextdata: FAIL")
					
					Result = DL.Check_StringAB(TR3maskdata, Track3_CardData)
					if Result != True:
						DL.SetWindowText("red", "TR3maskdata: FAIL")
					Result = DL.Check_StringAB(TR3plaintextdata, TRK3DecryptData)
					if Result != True:
						DL.SetWindowText("red", "TR3plaintextdata: FAIL")					
									
			else:
				DL.SetWindowText("RED", "Parse Card Data Fail")