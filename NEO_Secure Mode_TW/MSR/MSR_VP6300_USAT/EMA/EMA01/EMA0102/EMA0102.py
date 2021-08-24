#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''

# Enable encryption (00)
if (Result):
	RetOfStep = DL.SendCommand('Enable Encryption (00)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 00")
		
# Encryption type -- AES
if (Result):
	RetOfStep = DL.SendCommand('Encryption type -- AES')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 01")

# Set/ Get MSR Secure Parameters		
if (Result):
	RetOfStep = DL.SendCommand('Set MSR Secure Parameters (10)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('Get MSR Secure Parameters')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 05 DF EF 04 01 10")
		
# cmd 02-40, swipe card
if (Result):
	for j in range (1, 4):
		if j == 1:
			# Poll on Demand
			RetOfStep = DL.SendCommand('Poll on Demand')
			if (RetOfStep):
				Result = DL.Check_RXResponse("01 00 00 00")
				# Burst mode OFF		
				if (Result):
					RetOfStep = DL.SendCommand('Burst mode Off')
					if (RetOfStep):
						Result = DL.Check_RXResponse("04 00 00 00")	
		if j == 2:
			# Auto Poll
			RetOfStep = DL.SendCommand('Auto Poll')
			if (RetOfStep):
				Result = DL.Check_RXResponse("01 00 00 00")		
		if j == 3:
			# Burst mode ON		
			RetOfStep = DL.SendCommand('Burst mode ON')
			if (RetOfStep):
				Result = DL.Check_RXResponse("04 00 00 00")
					
		if (Result):
			for i in range (1, 11):
				if j == 1:
					if i == 1:
						RetOfStep = DL.SendCommand('Activate Transaction -- IDT')
					if i == 2:
						RetOfStep = DL.SendCommand('Activate Transaction -- Discover')
					if i == 3:
						RetOfStep = DL.SendCommand('Activate Transaction -- JIS 1')
					if i == 4:
						RetOfStep = DL.SendCommand('Activate Transaction -- JIS 2')
					if i == 5:
						RetOfStep = DL.SendCommand('Activate Transaction -- AAMVA')
					if i == 6:
						RetOfStep = DL.SendCommand('Activate Transaction -- Gift card')
					if i == 7:
						RetOfStep = DL.SendCommand('Activate Transaction -- PAN = 11')
					if i == 8:
						RetOfStep = DL.SendCommand('Activate Transaction -- PAN = 12')
					if i == 9:
						RetOfStep = DL.SendCommand('Activate Transaction -- PAN = 20')
					if i == 10:
						RetOfStep = DL.SendCommand('Activate Transaction -- ISO4909 (3T)')
				if j == 2:
					if i == 1:
						RetOfStep = DL.SendCommand('Get Transaction Result -- IDT')
					if i == 2:
						RetOfStep = DL.SendCommand('Get Transaction Result -- Discover')
					if i == 3:
						RetOfStep = DL.SendCommand('Get Transaction Result -- JIS 1')
					if i == 4:
						RetOfStep = DL.SendCommand('Get Transaction Result -- JIS 2')
					if i == 5:
						RetOfStep = DL.SendCommand('Get Transaction Result -- AAMVA')
					if i == 6:
						RetOfStep = DL.SendCommand('Get Transaction Result -- Gift card')
					if i == 7:
						RetOfStep = DL.SendCommand('Get Transaction Result -- PAN = 11')
					if i == 8:
						RetOfStep = DL.SendCommand('Get Transaction Result -- PAN = 12')
					if i == 9:
						RetOfStep = DL.SendCommand('Get Transaction Result -- PAN = 20')
					if i == 10:
						RetOfStep = DL.SendCommand('Get Transaction Result -- ISO4909 (3T)')
				if j == 3:
					if i == 1:
						RetOfStep = DL.SendCommand('Burst mode data -- IDT')
					if i == 2:
						RetOfStep = DL.SendCommand('Burst mode data -- Discover')
					if i == 3:
						RetOfStep = DL.SendCommand('Burst mode data -- JIS 1')
					if i == 4:
						RetOfStep = DL.SendCommand('Burst mode data -- JIS 2')
					if i == 5:
						RetOfStep = DL.SendCommand('Burst mode data -- AAMVA')
					if i == 6:
						RetOfStep = DL.SendCommand('Burst mode data -- Gift card')
					if i == 7:
						RetOfStep = DL.SendCommand('Burst mode data -- PAN = 11')
					if i == 8:
						RetOfStep = DL.SendCommand('Burst mode data -- PAN = 12')
					if i == 9:
						RetOfStep = DL.SendCommand('Burst mode data -- PAN = 20')
					if i == 10:
						RetOfStep = DL.SendCommand('Burst mode data -- ISO4909 (3T)')
				
				if (RetOfStep):		
					if j == 1:
						if i == 1:
							Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** 2A DF EE 25 02 00 11 DF EE 23 ** 02 ** 83 3F 4F 28 6B 97 00")
						if i == 2:
							Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** 2A DF EE 25 02 00 11 DF EE 23 ** 02 ** 80 1F 44 28 00 B3 00")
						if i == 3:
							Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** 2A DF EE 25 02 00 11 DF EE 23 ** 02 ** 80 1F 48 28 00 B3 00")
						if i == 4:
							Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** 2A DF EE 25 02 00 11 DF EE 23 ** 02 ** 85 17 00 48 00 92 00")
						if i == 5:
							Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** 2A DF EE 25 02 00 11 DF EE 23 ** 02 ** 81 3F 30 23 52 97 00")
						if i == 6:
							Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** 2A DF EE 25 02 00 11 DF EE 23 ** 02 ** 80 1F 3D 26 00 93 00")
						if i == 7:
							Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** 2A DF EE 25 02 00 11 DF EE 23 ** 02 ** 83 0F 3B 00 00 91 00")
						if i == 8:
							Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** 2A DF EE 25 02 00 11 DF EE 23 ** 02 ** 80 0F 3A 00 00 B1 00")
						if i == 9:
							Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** 2A DF EE 25 02 00 11 DF EE 23 ** 02 ** 83 0F 42 00 00 91 00")
						if i == 10:
							Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** 2A DF EE 25 02 00 11 DF EE 23 ** 02 ** 80 3F 4D 27 69 97 00")
					if j == 2:
						Result = DL.Check_StringAB(DL.Get_RXResponse(1),"56 69 56 4F 74 65 63 68 32 00 03 00")
						if (Result):
							Result = DL.Check_StringAB(DL.Get_RXResponse(1),"2A DF EE 25 02 00 11 DF EE 23")
							if (Result):
								if i == 1:
									Result = DL.Check_StringAB(DL.Get_RXResponse(1),"83 3F 4F 28 6B 97 00")
								if i == 2:
									Result = DL.Check_StringAB(DL.Get_RXResponse(1),"80 1F 44 28 00 B3 00")
								if i == 3:
									Result = DL.Check_StringAB(DL.Get_RXResponse(1),"80 1F 48 28 00 B3 00")
								if i == 4:
									Result = DL.Check_StringAB(DL.Get_RXResponse(1),"85 17 00 48 00 92 00")
								if i == 5:
									Result = DL.Check_StringAB(DL.Get_RXResponse(1),"81 3F 30 23 52 97 00")
								if i == 6:
									Result = DL.Check_StringAB(DL.Get_RXResponse(1),"80 1F 3D 26 00 93 00")
								if i == 7:
									Result = DL.Check_StringAB(DL.Get_RXResponse(1),"83 0F 3B 00 00 91 00")
								if i == 8:
									Result = DL.Check_StringAB(DL.Get_RXResponse(1),"80 0F 3A 00 00 B1 00")
								if i == 9:
									Result = DL.Check_StringAB(DL.Get_RXResponse(1),"83 0F 42 00 00 91 00")
								if i == 10:
									Result = DL.Check_StringAB(DL.Get_RXResponse(1),"80 3F 4D 27 69 97 00")
					if j == 3:
						if i == 1:
							Result = DL.Check_RXResponse("01 00 0C 25 54 52 41 43 4B 31 37 36 37 36 37 36 30 37 30 37 30 37 37 36 37 36 37 36 30 37 30 37 30 37 37 36 37 36 37 36 30 37 30 37 30 37 37 36 37 36 37 36 30 37 30 37 30 37 37 36 37 36 37 36 30 37 30 37 30 37 37 36 37 36 37 36 30 37 30 37 3F 3B 32 31 32 31 32 31 32 31 32 31 37 36 37 36 37 36 30 37 30 37 30 37 37 36 37 36 37 36 37 36 32 31 32 31 32 31 32 3F 3B 33 33 33 33 33 33 33 33 33 33 37 36 37 36 37 36 30 37 30 37 30 37 37 36 37 36 37 36 33 33 33 33 33 33 33 33 33 33 37 36 37 36 37 36 30 37 30 37 30 37 37 36 37 36 37 36 33 33 33 33 33 33 33 33 33 33 37 36 37 36 37 36 30 37 30 37 30 37 37 36 37 36 37 36 33 33 33 33 33 33 33 33 33 33 37 36 37 36 37 36 30 37 30 37 3F 81 14")
						if i == 2:
							Result = DL.Check_RXResponse("01 00 0C 25 42 36 35 31 30 30 30 30 30 30 30 30 30 30 30 32 36 5E 43 41 52 44 2F 49 4D 41 47 45 20 30 33 20 20 20 20 20 20 20 20 20 20 20 20 20 5E 31 37 31 32 32 30 31 31 30 30 30 30 32 31 30 30 30 30 30 30 3F 3B 36 35 31 30 30 30 30 30 30 30 30 30 30 30 32 36 3D 31 37 31 32 32 30 31 31 30 30 30 30 32 31 30 30 30 30 30 30 3F 31 A6")
						if i == 3:
							Result = DL.Check_RXResponse("01 00 0C 7F 61 39 30 30 30 30 30 30 30 32 31 31 31 31 31 32 33 34 35 36 37 38 39 30 31 32 32 32 32 32 33 33 33 33 33 34 34 34 34 34 35 35 35 35 35 36 36 36 36 36 37 37 37 37 37 38 38 38 38 38 39 39 39 39 39 30 30 30 30 7F 3B 34 33 32 32 30 36 31 30 30 30 38 37 32 38 33 33 3D 31 31 30 38 32 30 31 38 38 36 34 30 38 32 35 31 30 30 30 30 3F 50 DB")
						if i == 4:
							Result = DL.Check_RXResponse("01 00 0C 7F 61 39 30 30 30 30 30 30 30 32 31 31 31 31 31 32 33 34 35 36 37 38 39 30 31 32 32 32 32 32 33 33 33 33 33 34 34 34 34 34 35 35 35 35 35 36 36 36 36 36 37 37 37 37 37 38 38 38 38 38 39 39 39 39 39 30 30 30 30 7F 8E 2C")
						if i == 5:
							Result = DL.Check_RXResponse("01 00 0C 25 4E 59 4E 45 57 20 59 4F 52 4B 5E 4C 45 45 24 42 52 55 43 45 24 4A 52 5E 36 35 35 20 4E 2E 20 42 45 52 52 59 20 53 54 2E 2C 20 23 4B 5E 3F 3B 33 35 35 35 35 35 31 31 31 31 31 31 31 31 31 31 31 31 31 3D 30 30 30 39 31 39 37 37 30 33 30 33 3F 25 23 23 39 32 38 32 31 2D 30 30 34 34 30 41 41 42 42 42 42 42 42 42 42 42 42 54 54 54 54 46 35 30 37 31 32 35 42 52 57 42 4C 4B 30 31 32 33 34 35 36 37 38 39 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 43 43 43 43 43 43 53 53 53 53 53 3F 73 BE")
						if i == 6:
							Result = DL.Check_RXResponse("01 00 0C 25 42 36 30 30 36 34 39 31 37 39 37 35 37 35 35 31 37 31 34 37 5E 30 37 36 37 35 30 30 39 39 30 32 24 30 30 30 30 30 24 20 20 20 20 20 20 20 20 5E 38 30 31 32 31 31 30 54 4C 36 3F 3B 36 30 30 36 34 39 31 37 39 37 35 37 35 35 31 37 31 34 37 3D 38 30 31 32 31 31 30 31 35 32 30 38 35 36 36 3F 45 58")
						if i == 7:
							Result = DL.Check_RXResponse("01 00 0C 25 42 34 30 37 31 36 36 32 31 30 34 36 5E 44 4F 57 2F 4A 4F 48 4E 20 5E 31 37 31 31 32 30 31 31 32 37 38 37 31 31 30 30 30 30 30 30 30 30 38 34 39 30 30 30 30 30 30 3F 20 3F D5 EA")
						if i == 8:
							Result = DL.Check_RXResponse("01 00 0C 25 42 34 30 37 31 36 36 32 31 30 34 36 39 5E 44 4F 57 2F 4A 4F 48 4E 20 5E 31 37 31 31 32 30 31 31 32 37 38 37 31 31 30 30 30 30 30 30 30 30 38 34 39 30 30 30 30 30 30 3F 2A D2")
						if i == 9:
							Result = DL.Check_RXResponse("01 00 0C 25 42 34 30 37 31 36 36 32 31 30 34 36 39 31 32 33 34 35 36 37 38 5E 44 4F 57 2F 4A 4F 48 4E 20 5E 31 37 31 31 32 30 31 31 32 37 38 37 31 31 30 30 30 30 30 30 30 30 38 34 39 30 30 30 30 30 30 3F 64 9D")
						if i == 10:
							Result = DL.Check_RXResponse("01 00 0C 25 42 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 5E 4C 4C 49 42 52 45 20 52 4F 42 45 52 54 2D 47 55 49 4C 4C 45 52 4D 4F 20 5E 31 31 30 32 31 30 31 30 30 30 30 30 30 30 34 30 30 30 30 30 30 30 33 30 36 30 30 30 30 30 30 3F 3B 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 31 31 30 32 31 30 31 30 30 30 30 30 33 30 36 30 30 30 30 3F 3B 30 31 34 35 34 37 35 37 30 30 30 31 30 37 30 30 30 30 3D 37 39 37 38 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 33 30 31 39 30 31 38 30 34 30 32 30 30 30 31 31 30 32 34 3D 33 30 32 35 30 30 30 31 31 34 31 34 30 31 30 35 38 35 39 38 3D 3D 31 3D 30 30 30 30 30 30 32 36 30 30 30 30 30 30 30 30 30 30 30 30 3F BE 68")
									
					if j == 1:
						sResult=DL.Get_RXResponse(0)
					if j == 2:
						sResult=DL.Get_RXResponse(1)
					if j == 3:
						sResult=""
						
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
								Result = DL.Check_StringAB(TagDFEE26, '2A01')
								if Result != True:
									DL.SetWindowText("red", "TagDFEE26: FAIL")	
								
								# IDT
								if i == 1:
									# Transaction result verification
									TR1maskdata = "%TRACK17676760707077676760707077676760707077676760707077676760707077676760707?C"
									TR2maskdata = ";2121212121767676070707767676762121212?0"
									TR3maskdata = ";33333333337676760707077676763333333333767676070707767676333333333376767607070776767633333333337676760707?2"
									
									Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR1maskdata: FAIL")

									Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR2maskdata: FAIL")

									Result = DL.Check_StringAB(TR3maskdata, Track3_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR3maskdata: FAIL")
																											
								# Discover	
								if i == 2:
									# Transaction result verification
									TR1maskdata = "%B6510000000000026^CARD/IMAGE 03             ^17122011000021000000?%"
									TR2maskdata = ";6510000000000026=17122011000021000000?;"
									
									Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR1maskdata: FAIL")

									Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR2maskdata: FAIL")
									
								# JIS 1	
								if i == 3:
									# Transaction result verification
									TR1maskdata = "a90000000211111234567890122222333334444455555666667777788888999990000"
									TR2maskdata = ";4322061000872833=11082018864082510000?;"
									
									Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR1maskdata: FAIL")

									Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR2maskdata: FAIL")

								# JIS 2	
								if i == 4:
									# Transaction result verification
									TR2maskdata = "a90000000211111234567890122222333334444455555666667777788888999990000"
									
									Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR2maskdata: FAIL")

								# AAMVA
								if i == 5:
									# Transaction result verification
									TR1maskdata = "%NYNEW YORK^LEE$BRUCE$JR^655 N. BERRY ST., #K^?R"
									TR2maskdata = ";3555551111111111111=000919770303??"
									TR3maskdata = "%##92821-00440AABBBBBBBBBBTTTTF507125BRWBLK0123456789                CCCCCCSSSSS?%"
									
									Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR1maskdata: FAIL")

									Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR2maskdata: FAIL")

									Result = DL.Check_StringAB(TR3maskdata, Track3_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR3maskdata: FAIL")

								# Gift Card	
								if i == 6:
									# Transaction result verification
									TR1maskdata = "%B6006491797575517147^07675009902$00000$        ^8012110TL6?_"
									TR2maskdata = ";6006491797575517147=801211015208566?:"
									
									Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR1maskdata: FAIL")

									Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR2maskdata: FAIL")

								# PAN = 11	
								if i == 7:
									# Transaction result verification
									TR1maskdata = "%B40716621046^DOW/JOHN ^1711201127871100000000849000000? ??"
									
									Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR1maskdata: FAIL")

								# PAN = 12	
								if i == 8:
									# Transaction result verification
									TR1maskdata = "%B407166210469^DOW/JOHN ^1711201127871100000000849000000?9"
									
									Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR1maskdata: FAIL")

								# PAN = 20	
								if i == 9:
									# Transaction result verification
									TR1maskdata = "%B40716621046912345678^DOW/JOHN ^1711201127871100000000849000000?1"
									
									Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR1maskdata: FAIL")

								# ISO 4909 (3T)	
								if i == 10:
									# Transaction result verification
									TR1maskdata = "%B4547570001070000^LLIBRE ROBERT-GUILLERMO ^1102101000000040000000306000000?."
									TR2maskdata = ";4547570001070000=1102101000003060000?8"
									TR3maskdata = ";014547570001070000=79780000000000000003019018040200011024=30250001141401058598==1=00000026000000000000?5"
									
									Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR1maskdata: FAIL")

									Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR2maskdata: FAIL")
										
									Result = DL.Check_StringAB(TR3maskdata, Track3_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR3maskdata: FAIL")
						else:
							DL.SetWindowText("RED", "Parse Card Data Fail")