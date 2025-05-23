#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''
strKey ='FEDCBA9876543210F1F1F1F1F1F1F1F1'

# Check reader is VP3350 or not
if (Result):
	RetOfStep = DL.SendCommand('0105 do not use LCD')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")

# Check data encryption TYPE is TDES	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 06 01 02 00 00 00 00")
		
# Tag DFEE1D = 04 04 2A 0C 30
if (Result):
	RetOfStep = DL.SendCommand('Tag DFEE1D = 04 04 2A 0C 30')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 00")

# # Set/ Get MSR Secure Parameters		
# if (Result):
	# RetOfStep = DL.SendCommand('Set MSR Secure Parameters (10)')
	# if (RetOfStep):
		# Result = Result and DL.Check_RXResponse("C7 00 00 00")	
# if (Result):
	# RetOfStep = DL.SendCommand('Get MSR Secure Parameters')
	# if (RetOfStep):
		# Result = Result and DL.Check_RXResponse("C7 00 00 05 DF EF 04 01 10")
		
# Burst mode OFF		
if (Result):
	RetOfStep = DL.SendCommand('Burst mode Off')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	

# cmd 02-40, swipe Discover card
if (Result):
	for j in range (1, 2):
		if j == 1:
			RetOfStep = DL.SendCommand('Poll on Demand')
			if (RetOfStep):
				Result = DL.Check_RXResponse("01 00 00 00")
		if j == 2:
			RetOfStep = DL.SendCommand('Auto Poll')
			if (RetOfStep):
				Result = DL.Check_RXResponse("01 00 00 00")		
		if (Result):
			for i in range (2, 3):
				if j == 1:
					# if i == 1:
						# RetOfStep = DL.SendCommand('Activate Transaction -- IDT')
					if i == 2:
						RetOfStep = DL.SendCommand('Activate Transaction -- Discover')
					# if i == 3:
						# RetOfStep = DL.SendCommand('Activate Transaction -- JIS 1')
					# if i == 4:
						# RetOfStep = DL.SendCommand('Activate Transaction -- JIS 2')
					# if i == 5:
						# RetOfStep = DL.SendCommand('Activate Transaction -- AAMVA')
					# if i == 6:
						# RetOfStep = DL.SendCommand('Activate Transaction -- Gift card')
					# if i == 7:
						# RetOfStep = DL.SendCommand('Activate Transaction -- PAN = 11')
					# if i == 8:
						# RetOfStep = DL.SendCommand('Activate Transaction -- PAN = 12')
					# if i == 9:
						# RetOfStep = DL.SendCommand('Activate Transaction -- PAN = 20')
					# if i == 10:
						# RetOfStep = DL.SendCommand('Activate Transaction -- ISO4909 (3T)')
				if j == 2:
					# if i == 1:
						# RetOfStep = DL.SendCommand('Get Transaction Result -- IDT')
					if i == 2:
						RetOfStep = DL.SendCommand('Get Transaction Result -- Discover')
					# if i == 3:
						# RetOfStep = DL.SendCommand('Get Transaction Result -- JIS 1')
					# if i == 4:
						# RetOfStep = DL.SendCommand('Get Transaction Result -- JIS 2')
					# if i == 5:
						# RetOfStep = DL.SendCommand('Get Transaction Result -- AAMVA')
					# if i == 6:
						# RetOfStep = DL.SendCommand('Get Transaction Result -- Gift card')
					# if i == 7:
						# RetOfStep = DL.SendCommand('Get Transaction Result -- PAN = 11')
					# if i == 8:
						# RetOfStep = DL.SendCommand('Get Transaction Result -- PAN = 12')
					# if i == 9:
						# RetOfStep = DL.SendCommand('Get Transaction Result -- PAN = 20')
					# if i == 10:
						# RetOfStep = DL.SendCommand('Get Transaction Result -- ISO4909 (3T)')
				
				if (RetOfStep):		
					if j == 1:
						# if i == 1:
							# Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EA DF EE 25 02 00 11 DF EE 23 ** 02 ** 83 3F 4F 28 6B 97 00")
						if i == 2:
							Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EC DF EE 25 02 00 11 DF EE 23 ** 02 ** 80 5F 44 28 00 A3 9B")
						# if i == 3:
							# Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EA DF EE 25 02 00 11 DF EE 23 ** 02 ** 86 1F 48 28 00 93 00")
						# if i == 4:
							# Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EA DF EE 25 02 00 11 DF EE 23 ** 02 ** 85 17 00 48 00 92 00")
						# if i == 5:
							# Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EA DF EE 25 02 00 11 DF EE 23 ** 02 ** 81 3F 30 23 52 97 00")
						# if i == 6:
							# Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EA DF EE 25 02 00 11 DF EE 23 ** 02 ** 80 1F 3D 26 00 93 83")
						# if i == 7:
							# Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EA DF EE 25 02 00 11 DF EE 23 ** 02 ** 83 0F 3B 00 00 91 00")
						# if i == 8:
							# Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EA DF EE 25 02 00 11 DF EE 23 ** 02 ** 80 0F 3A 00 00 B1 81")
						# if i == 9:
							# Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EA DF EE 25 02 00 11 DF EE 23 ** 02 ** 83 0F 42 00 00 91 00")
						# if i == 10:
							# Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EA DF EE 25 02 00 11 DF EE 23 ** 02 ** 80 3F 4D 27 69 93 87")
					if j == 2:
						Result = DL.Check_RXResponse(1,"56 69 56 4F 74 65 63 68 32 00 03 00")
						if (Result):
							Result = DL.Check_RXResponse(1,"EC ** DF EE 25 02 00 11 DF EE 23")
							if (Result):
								# if i == 1:
									# Result = DL.Check_StringAB(DL.Get_RXResponse(1),"83 3F 4F 28 6B 97 00")
								if i == 2:
									Result = DL.Check_StringAB(DL.Get_RXResponse(1),"80 5F 44 28 00 A3 9B")
								# if i == 3:
									# Result = DL.Check_StringAB(DL.Get_RXResponse(1),"86 1F 48 28 00 93 00")
								# if i == 4:
									# Result = DL.Check_StringAB(DL.Get_RXResponse(1),"85 17 00 48 00 92 00")
								# if i == 5:
									# Result = DL.Check_StringAB(DL.Get_RXResponse(1),"81 3F 30 23 52 97 00")
								# if i == 6:
									# Result = DL.Check_StringAB(DL.Get_RXResponse(1),"80 1F 3D 26 00 93 83")
								# if i == 7:
									# Result = DL.Check_StringAB(DL.Get_RXResponse(1),"83 0F 3B 00 00 91 00")
								# if i == 8:
									# Result = DL.Check_StringAB(DL.Get_RXResponse(1),"80 0F 3A 00 00 B1 81")
								# if i == 9:
									# Result = DL.Check_StringAB(DL.Get_RXResponse(1),"83 0F 42 00 00 91 00")
								# if i == 10:
									# Result = DL.Check_StringAB(DL.Get_RXResponse(1),"80 3F 4D 27 69 93 87")
									
					if j == 1:
						sResult=DL.Get_RXResponse(0)
					if j == 2:
						sResult=DL.Get_RXResponse(1)
						
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
									TRK1DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK1)
								if len(TRK2)> 0:
									TRK2DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK2)
								if len(TRK3) > 0:
									TRK3DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK3)
							
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
								Result = DL.Check_StringAB(TagDFEE26, 'EC01')
								if Result != True:
									DL.fails=DL.fails+1
									DL.SetWindowText("red", "TagDFEE26: FAIL")	

								# Discover	
								if i == 2:
									# Transaction result verification
									TR1maskdata = "%*6510********0026^CARD/IMAGE 03             ^********************?*"
									TR2maskdata = ";6510********0026=********************?*"
									TR1plaintextdata = "2542363531303030303030303030303032365E434152442F494D414745203033202020202020202020202020205E31373132323031313030303032313030303030303F25"
									TR2plaintextdata = "3B363531303030303030303030303032363D31373132323031313030303032313030303030303F3B"
									
									Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
									if Result != True:
										DL.fails=DL.fails+1
										DL.SetWindowText("red", "TR1maskdata: FAIL")

									Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
									if Result != True:
										DL.fails=DL.fails+1
										DL.SetWindowText("red", "TR2maskdata: FAIL")

									Result = DL.Check_StringAB(TR1plaintextdata, TRK1DecryptData)
									if Result != True:
										DL.fails=DL.fails+1
										DL.SetWindowText("red", "TR1plaintextdata: FAIL")
										
									Result = DL.Check_StringAB(TR2plaintextdata, TRK2DecryptData)
									if Result != True:
										DL.fails=DL.fails+1
										DL.SetWindowText("red", "TR2plaintextdata: FAIL")
					else:
						DL.fails=DL.fails+1
else:
	DL.fails=DL.fails+1
							
RetOfStep = DL.SendCommand('0105 default (VP3350)')
if (RetOfStep):
	Result = DL.Check_RXResponse("01 00 00 00")
        
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )