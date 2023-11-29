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
lcdtype = DL.ShowMessageBox("", "Is this VP3350?", 0)
if lcdtype == 1:
	DL.SetWindowText("Green", "*** This is VP3350 ***")
	RetOfStep = DL.SendCommand('0105 do not use LCD')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")
else:
	DL.SetWindowText("Green", "*** non-VP3350 reader ***")

# Check data encryption TYPE is AES	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("C7 00 00 06 01 02 00 00 00 00")

# Set/ Get MSR Secure Parameters		
if (Result):
	RetOfStep = DL.SendCommand('Set MSR Secure Parameters (05)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('Get MSR Secure Parameters')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 05 DF EF 04 01 05")
		
# Burst mode OFF		
if (Result):
	RetOfStep = DL.SendCommand('Burst mode Off')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	

# cmd 02-40, swipe card
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
			for i in range (1, 11):
				if j == 1:
					time.sleep(1)
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
				
				if (RetOfStep):		
					if j == 1:
						if i == 1:
							Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EC DF EE 25 02 00 11 DF EE 23 ** 02 ** 83 7F 4F 28 6B 82 AD")
						if i == 2:
							Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EC DF EE 25 02 00 11 DF EE 23 ** 02 ** 80 5F 44 28 00 A3 9B")
						if i == 3:
							Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EC DF EE 25 02 00 11 DF EE 23 ** 02 ** 80 5F 48 28 00 A3 9B")
						if i == 4:
							Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EC DF EE 25 02 00 11 DF EE 23 ** 02 ** 85 57 00 48 00 82 00")
						if i == 5:
							Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EC DF EE 25 02 00 11 DF EE 23 ** 02 ** 81 7F 30 23 52 82 AD")
						if i == 6:
							Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EC DF EE 25 02 00 11 DF EE 23 ** 02 ** 80 5F 3D 26 00 83 9B")
						if i == 7:
							Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EC DF EE 25 02 00 11 DF EE 23 ** 02 ** 83 4F 3B 00 00 80 89")
						if i == 8:
							Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EC DF EE 25 02 00 11 DF EE 23 ** 02 ** 80 4F 3A 00 00 A1 89")
						if i == 9:
							Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EC DF EE 25 02 00 11 DF EE 23 ** 02 ** 83 4F 42 00 00 80 89")
						if i == 10:
							Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** EC DF EE 25 02 00 11 DF EE 23 ** 02 ** 80 7F 4D 27 69 87 BF")
					if j == 2:
						Result = DL.Check_StringAB(DL.Get_RXResponse(1),"56 69 56 4F 74 65 63 68 32 00 03 00")
						if (Result):
							Result = DL.Check_StringAB(DL.Get_RXResponse(1),"EC DF EE 25 02 00 11 DF EE 23")
							if (Result):
								if i == 1:
									Result = DL.Check_StringAB(DL.Get_RXResponse(1),"83 7F 4F 28 6B 82 AD")
								if i == 2:
									Result = DL.Check_StringAB(DL.Get_RXResponse(1),"80 5F 44 28 00 A3 9B")
								if i == 3:
									Result = DL.Check_StringAB(DL.Get_RXResponse(1),"80 5F 48 28 00 A3 9B")
								if i == 4:
									Result = DL.Check_StringAB(DL.Get_RXResponse(1),"85 57 00 48 00 82 00")
								if i == 5:
									Result = DL.Check_StringAB(DL.Get_RXResponse(1),"81 7F 30 23 52 82 AD")
								if i == 6:
									Result = DL.Check_StringAB(DL.Get_RXResponse(1),"80 5F 3D 26 00 83 9B")
								if i == 7:
									Result = DL.Check_StringAB(DL.Get_RXResponse(1),"83 4F 3B 00 00 80 89")
								if i == 8:
									Result = DL.Check_StringAB(DL.Get_RXResponse(1),"80 4F 3A 00 00 A1 89")
								if i == 9:
									Result = DL.Check_StringAB(DL.Get_RXResponse(1),"83 4F 42 00 00 80 89")
								if i == 10:
									Result = DL.Check_StringAB(DL.Get_RXResponse(1),"80 7F 4D 27 69 87 BF")
									
					if j == 1:
						rx = 0
					if j == 2:
						rx = 1
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
									TRK1DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK1)
								if len(TRK2)> 0:
									TRK2DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK2)
								if len(TRK3) > 0:
									TRK3DecryptData = DL.AES_DUPKT_EMVData_Decipher(KSN, strKey, TRK3)
							
								# Verify specific tags
								if DL.Check_RXResponse(rx, "9F39 01 90") == False:
									DL.SetWindowText("red", "Tag9F39: FAIL")							
								if DL.Check_RXResponse(rx, 'FFEE01 ** DFEE30010C') == False:
									DL.SetWindowText("red", "TagFFEE01: FAIL")	
								if DL.Check_RXResponse(rx, 'DFEE26 02 EC01') == False:
									DL.SetWindowText("red", "TagDFEE26: FAIL")	
								
								# IDT
								if i == 1:
									# Transaction result verification
									TR2maskdata = ";2121212121767676070707767676762121212?0"
									TR1plaintextdata = "25545241434B31373637363736303730373037373637363736303730373037373637363736303730373037373637363736303730373037373637363736303730373037373637363736303730373F43"
									TR3plaintextdata = "3B33333333333333333333373637363736303730373037373637363736333333333333333333333736373637363037303730373736373637363333333333333333333337363736373630373037303737363736373633333333333333333333373637363736303730373F32"

									Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR2maskdata: FAIL")
										
									Result = DL.Check_StringAB(TR1plaintextdata, TRK1DecryptData)
									if Result != True:
										DL.SetWindowText("red", "TR1plaintextdata: FAIL")	

									Result = DL.Check_StringAB(TR3plaintextdata, TRK3DecryptData)
									if Result != True:
										DL.SetWindowText("red", "TR3plaintextdata: FAIL")
																											
								# Discover	
								if i == 2:
									# Transaction result verification
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
									
								# JIS 1	
								if i == 3:
									# Transaction result verification
									TR1maskdata = "a900*************************************************************0000"
									TR2maskdata = ";4322********2833=1108****************?*"
									TR1plaintextdata = "613930303030303030323131313131323334353637383930313232323232333333333334343434343535353535363636363637373737373838383838393939393930303030"
									TR2plaintextdata = "3B343332323036313030303837323833333D31313038323031383836343038323531303030303F3B"                                    
									
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

								# JIS 2	
								if i == 4:
									# Transaction result verification
									TR2maskdata = "a90000000211111234567890122222333334444455555666667777788888999990000"
									TR2maskdata2 = "123456789012345678901234567890123456789012345678901234567890123456789"
									
									Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
									if Result != True:
										Result = DL.Check_StringAB(TR2maskdata2, Track2_CardData)
										if Result != True:
											DL.SetWindowText("red", "TR2maskdata: FAIL")
										else:
											DL.SetWindowText("green", "JIS2 final verification result: PASS")

								# AAMVA
								if i == 5:
									# Transaction result verification
									TR2maskdata = ";3555551111111111111=000919770303??"
									TR1plaintextdata = "254E594E455720594F524B5E4C4545244252554345244A525E363535204E2E2042455252592053542E2C20234B5E3F52"
									TR3plaintextdata = "25232339323832312D30303434304141424242424242424242425454545446353037313235425257424C4B303132333435363738392020202020202020202020202020202043434343434353535353533F25"

									Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR2maskdata: FAIL")
										
									Result = DL.Check_StringAB(TR1plaintextdata, TRK1DecryptData)
									if Result != True:
										DL.SetWindowText("red", "TR1plaintextdata: FAIL")

									Result = DL.Check_StringAB(TR3plaintextdata, TRK3DecryptData)
									if Result != True:
										DL.SetWindowText("red", "TR3plaintextdata: FAIL")

								# Gift Card	
								if i == 6:
									# Transaction result verification
									TR1maskdata = "%*6006***********7147^07675009902$00000$        ^8012******?*"
									TR2maskdata = ";6006***********7147=8012***********?*"
									TR1plaintextdata = "2542363030363439313739373537353531373134375E30373637353030393930322430303030302420202020202020205E38303132313130544C363F5F"
									TR2plaintextdata = "3B363030363439313739373537353531373134373D3830313231313031353230383536363F3A"
									
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

								# PAN = 11	
								if i == 7:
									# Transaction result verification
									TR1plaintextdata = "254234303731363632313034365E444F572F4A4F484E205E313731313230313132373837313130303030303030303834393030303030303F203F3F"
									
									Result = DL.Check_StringAB(TR1plaintextdata, TRK1DecryptData)
									if Result != True:
										DL.SetWindowText("red", "TR1plaintextdata: FAIL")

								# PAN = 12	
								if i == 8:
									# Transaction result verification
									TR1maskdata = "%*40******0469^DOW/JOHN ^1711***************************?*"
									TR1plaintextdata = "25423430373136363231303436395E444F572F4A4F484E205E313731313230313132373837313130303030303030303834393030303030303F39"
									
									Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR1maskdata: FAIL")
										
									Result = DL.Check_StringAB(TR1plaintextdata, TRK1DecryptData)
									if Result != True:
										DL.SetWindowText("red", "TR1plaintextdata: FAIL")

								# PAN = 20	
								if i == 9:
									# Transaction result verification
									TR1plaintextdata = "254234303731363632313034363931323334353637385E444F572F4A4F484E205E313731313230313132373837313130303030303030303834393030303030303F31"
									
									Result = DL.Check_StringAB(TR1plaintextdata, TRK1DecryptData)
									if Result != True:
										DL.SetWindowText("red", "TR1plaintextdata: FAIL")

								# ISO 4909 (3T)	
								if i == 10:
									# Transaction result verification
									TR1maskdata = "%*4547********0000^LLIBRE ROBERT-GUILLERMO ^1102***************************?*"
									TR2maskdata = ";4547********0000=1102***************?*"
									TR3maskdata = ";**4547********0000=***********************************************************************************?*"
									TR1plaintextdata = "2542343534373537303030313037303030305E4C4C4942524520524F424552542D4755494C4C45524D4F205E313130323130313030303030303034303030303030303330363030303030303F2E"
									TR2plaintextdata = "3B343534373537303030313037303030303D313130323130313030303030333036303030303F38"
									TR3plaintextdata = "3B3031343534373537303030313037303030303D37393738303030303030303030303030303030333031393031383034303230303031313032343D33303235303030313134313430313035383539383D3D313D30303030303032363030303030303030303030303F35"
									
									Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR1maskdata: FAIL")

									Result = DL.Check_StringAB(TR2maskdata, Track2_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR2maskdata: FAIL")
										
									Result = DL.Check_StringAB(TR3maskdata, Track3_CardData)
									if Result != True:
										DL.SetWindowText("red", "TR3maskdata: FAIL")									
									Result = DL.Check_StringAB(TR1plaintextdata, TRK1DecryptData)
									if Result != True:
										DL.SetWindowText("red", "TR1plaintextdata: FAIL")
										
									Result = DL.Check_StringAB(TR2plaintextdata, TRK2DecryptData)
									if Result != True:
										DL.SetWindowText("red", "TR2plaintextdata: FAIL")
										
									Result = DL.Check_StringAB(TR3plaintextdata, TRK3DecryptData)
									if Result != True:
										DL.SetWindowText("red", "TR3plaintextdata: FAIL")					

							
if lcdtype == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")							
        
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )