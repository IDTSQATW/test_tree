#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''
strKey = '99999999999999999999999999999999'

# Check data key slot 00
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT KSN (81-0B)_0209')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("62 99 49 01 90 00 00 00")
		
# Set IIN
if (Result):
	RetOfStep = DL.SendCommand('Set IIN')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("00")

# Get IIN
if (Result):
	RetOfStep = DL.SendCommand('Get IIN')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("37 09 03 47 61 73 01 00 03 44 62 72 01 01 03 54 13 33 01 03 03 54 57 21 01 04 03 67 99 99 01 05 03 35 40 82 01 06 03 36 07 05 01 07 03 37 42 45 01 08 03 65 10 00 01 09")

# cmd 02-05, insert card
if (Result):
	RetOfStep = DL.SendCommand('ACT (02-05) - MSR only')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** CA DF EE 23 ** 02 ** 80 1F 44 28 00 B3 9B")
		alldata = DL.Get_RXResponse(0)
		
		if Result == True and alldata!=None and alldata!="":
						alldata=alldata.replace(" ","")
						CardData=DL.GetTLV(alldata,"DFEE23")
						bresult = False
						if CardData!=None and CardData!='':
							objectMSR = DL.ParseCardData(CardData ,bresult,strKey,MacKey)
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
									TRK1DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, strKey, KSN, TRK1)
									TRK1DecryptData = TRK1DecryptData[0:((objectMSR[0].msr_track1Length)*2)]
								if len(TRK2)> 0:
									DL.SetWindowText("blue", "Track 2:")
									TRK2DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, strKey, KSN, TRK2)
									TRK2DecryptData = TRK2DecryptData[0:((objectMSR[0].msr_track2Length)*2)]
								if len(TRK3) > 0:
									DL.SetWindowText("blue", "Track 3:")
									TRK3DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, strKey, KSN, TRK3)
									TRK3DecryptData = TRK3DecryptData[0:((objectMSR[0].msr_track3Length)*2)]
							
								Tag9F39 = DL.GetTLV(alldata,"9F39")
								TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
								TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
								
								# Verify specific tags
								Result = DL.Check_StringAB(Tag9F39, '90')
								if Result != True:
									DL.SetWindowText("red", "Tag9F39: FAIL")							
								Result = DL.Check_StringAB(TagFFEE01, 'DFEE30010C')
								if Result != True:
									DL.SetWindowText("red", "TagFFEE01: FAIL")	
								Result = DL.Check_StringAB(TagDFEE26, 'CA')
								if Result != True:
									DL.SetWindowText("red", "TagDFEE26: FAIL")
																											
								# Discover	
									TR1maskdata = "%*6510********0026^CARD/IMAGE 03             ^1712****************?*"
									TR2maskdata = ";6510********0026=1712****************?*"
									TR1plaintextdata = "2542363531303030303030303030303032365E434152442F494D414745203033202020202020202020202020205E31373132323031313030303032313030303030303F25"
									TR2plaintextdata = "3B363531303030303030303030303032363D31373132323031313030303032313030303030303F3B"
									
									Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR1maskdata: FAIL")

									Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR2maskdata: FAIL")

									Result = DL.Check_StringAB(TR1plaintextdata, TRK1DecryptData)
									if Result != True:
										DL.SetWindowText("red", "TR1plaintextdata: FAIL")
										
									Result = DL.Check_StringAB(TR2plaintextdata, TRK2DecryptData)
									if Result != True:
										DL.SetWindowText("red", "TR2plaintextdata: FAIL")						
						else:
							DL.SetWindowText("RED", "Parse Card Data Fail")
								
		