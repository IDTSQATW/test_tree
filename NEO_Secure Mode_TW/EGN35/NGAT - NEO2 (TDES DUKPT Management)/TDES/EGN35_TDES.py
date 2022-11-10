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
rx = 0
		
# Check project has LCD or not
lcdtype = DL.ShowMessageBox("", "Does the project has LCD?", 0)
if lcdtype == 1:
	DL.SetWindowText("Green", "*** The project has LCD ***")
else:
	DL.SetWindowText("Green", "*** The project has NO LCD ***")
	
# Check reader is VP3350 or not
readermodel = DL.ShowMessageBox("", "Is this VP3350?", 0)
if readermodel == 1:
	DL.SetWindowText("Green", "*** This is VP3350 ***")
else:
	DL.SetWindowText("Green", "*** non-VP3350 reader ***")		

# Check data encryption TYPE is TDES DUKPT Management/ TDES/ PIN Key	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 06 00 00 01 00 00 00")
		if Result == False:
			DL.SetWindowText("red", "Data key should be: TDES DUKPT Management/ TDES/ PIN Key, please check setting first...")
			
# First Response Control (0x63) = enable
if (Result):
	RetOfStep = DL.SendCommand('First Response Control (0x63) = enable')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	
		
# Set group B0
if (Result):
	RetOfStep = DL.SendCommand('Set group B0')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	

# cmd 02-40, MSR/ CL/ CT				
if (Result):	
	for i in range (1, 6):
		if i <= 3:
			if i == 1:
				RetOfStep = DL.SendCommand('Poll on Demand')
				if (RetOfStep):
					Result = DL.Check_RXResponse("01 00 00 00")	
			if (Result):			
				if i == 1:
					if lcdtype == 1:
						RetOfStep = DL.SendCommand('02-40, MSR -- Discover w/ LCD')
						rx = 0
					if lcdtype == 0:
						time.sleep(1)
						RetOfStep = DL.SendCommand('02-40, MSR -- Discover w/o LCD')
						rx = 1
				if i == 2:
					if lcdtype == 1:
						RetOfStep = DL.SendCommand('02-40, CL -- Discover w/ LCD')
						rx = 0
					if lcdtype == 0:
						if readermodel == 0:
							RetOfStep = DL.SendCommand('02-40, CL -- Discover w/o LCD')	
						if readermodel == 1:
							time.sleep(2)
							RetOfStep = DL.SendCommand('02-40, CL -- VISA w/o LCD')
						rx = 4
				if i == 3:
					if lcdtype == 1:
						RetOfStep = DL.SendCommand('60-10, CT -- EMV Test Card V2 T=0 w/ LCD')	
						rx = 1
					if lcdtype == 0:
						time.sleep(1)
						RetOfStep = DL.SendCommand('60-10, CT -- EMV Test Card V2 T=0 w/o LCD')	
						rx = 7
		if i >= 4:
			if i == 4:
				if lcdtype == 1:
					RetOfStep = DL.SendCommand('Auto Poll 1rx')
				if lcdtype == 0:
					RetOfStep = DL.SendCommand('Auto Poll 2rx')
				if (RetOfStep):
					Result = DL.Check_RXResponse("01 00 00 00")		
			if (Result):
				if i == 4:
					if lcdtype == 1:
						RetOfStep = DL.SendCommand('03-40, MSR -- Discover w/ LCD')
						rx = 1
					if lcdtype == 0:
						RetOfStep = DL.SendCommand('03-40, MSR -- Discover w/o LCD')
						rx = 3
					time.sleep(1)
				if i == 5:
					if lcdtype == 1:
						RetOfStep = DL.SendCommand('03-40, CL -- Discover w/ LCD')
						rx = 1
					if lcdtype == 0:
						if readermodel == 0:
							RetOfStep = DL.SendCommand('03-40, CL -- Discover w/o LCD')
						if readermodel == 1:
							RetOfStep = DL.SendCommand('03-40, CL -- VISA w/o LCD')	
						rx = 5	
					time.sleep(1)
				
		if (RetOfStep):
			# MSR transaction
			if i == 1 or i == 4:
				sResult=DL.Get_RXResponse(rx)	
				if sResult!=None and sResult!="":
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
										
							# Verify specific tags
							if DL.Check_RXResponse(rx, "9F39 ** 90") == False:
								DL.SetWindowText("red", "Tag9F39: FAIL")							
							if DL.Check_RXResponse(rx, "FFEE01 ** DFEE30010C") == False:	
								DL.SetWindowText("red", "TagFFEE01: FAIL")	
							if DL.Check_RXResponse(rx, "DFEE26 ** E800") == False:	
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
			# CL transaction
			if i == 2 or i == 5:
				if (RetOfStep):
					if readermodel == 0:
						alldata=DL.Get_RXResponse(rx)	
						DL.Check_RXResponse(rx, 'F1 ** DF EE 12')
						ksn = DL.GetTLV(alldata,"DFEE12")	
								
						maskDFEF17 = DL.GetTLV(alldata,"DFEF17", 0)
						encDFEF17 = DL.GetTLV(alldata,"DFEF17", 1)
						decDFEF17 = DL.DecryptDLL(1,1, strKey, ksn, encDFEF17)	
								
						maskDFEF18 = DL.GetTLV(alldata,"DFEF18", 0)
						encDFEF18 = DL.GetTLV(alldata,"DFEF18", 1)
						decDFEF18 = DL.DecryptDLL(1,1, strKey, ksn, encDFEF18)	

						tagFF8105 = DL.GetTLV(alldata,"FF8105", 0)		
						mask56 = DL.GetTLV(tagFF8105,"56", 0)
						enc56 = DL.GetTLV(tagFF8105,"56", 1)
						dec56 = DL.DecryptDLL(1,1, strKey, ksn, enc56)	
								
						mask57 = DL.GetTLV(tagFF8105,"57", 0)
						enc57 = DL.GetTLV(tagFF8105,"57", 1)
						dec57 = DL.DecryptDLL(1,1, strKey, ksn, enc57)	
								
						# Tag DFEF17
						r1 = DL.Check_RXResponse(rx, '2A363531302A2A2A2A2A2A2A2A')
						r2 = DL.Check_RXResponse(rx, '5E434152442F494D414745')
						r3 = DL.Check_RXResponse(rx, '5E313731322A2A2A2A2A2A2A2A2A2A2A2A2A')
						if r1 == True and r2 == True and r3 == True and DL.Check_RXResponse(rx, "DF EF 17 A1"):
							DL.SetWindowText("blue", "Tag DFEF17_Mask: PASS")
						else:
							DL.SetWindowText("red", "Tag DFEF17_Mask: FAIL")
									
						r1 = DL.Check_StringAB(decDFEF17, 'DF EF 17')
						r2 = DL.Check_StringAB(decDFEF17, '42 36 35 31 30 30 30 30 30 30 30 30 30')
						r3 = DL.Check_StringAB(decDFEF17, '5E 43 41 52 44 2F 49 4D 41 47 45')
						r4 = DL.Check_StringAB(decDFEF17, '5E 31 37 31 32 32 30 31')
						if r1 == True and r2 == True and r3 == True and r4 == True and DL.Check_StringAB(alldata, "DF EF 17 C1"):
							DL.SetWindowText("blue", "Tag DFEF17_Enc: PASS")
						else:
							DL.SetWindowText("red", "Tag DFEF17_Enc: FAIL")

						# Tag DFEF18
						r1 = DL.Check_RXResponse(rx, '36 35 31 30 2A 2A 2A 2A 2A 2A 2A 2A')
						r2 = DL.Check_RXResponse(rx, '3D 31 37 31 32 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A')
						if r1 == True and r2 == True and DL.Check_RXResponse(rx, "DF EF 18 A1"):
							DL.SetWindowText("blue", "Tag DFEF18_Mask: PASS")
						else:
							DL.SetWindowText("red", "Tag DFEF18_Mask: FAIL")
									
						r1 = DL.Check_StringAB(decDFEF18, 'DF EF 18')
						r2 = DL.Check_StringAB(decDFEF18, '36 35 31 30 30 30 30 30 30 30 30 30')
						r3 = DL.Check_StringAB(decDFEF18, '3D 31 37 31 32 32 30 31')
						if r1 == True and r2 == True and r3 == True and DL.Check_StringAB(alldata, "DF EF 18 C1"):
							DL.SetWindowText("blue", "Tag DFEF18_Enc: PASS")
						else:
							DL.SetWindowText("red", "Tag DFEF18_Enc: FAIL")
									
						# Tag 56
						r1 = DL.Check_RXResponse(rx, '2A 36 35 31 30 2A 2A 2A 2A 2A 2A 2A 2A')
						r2 = DL.Check_RXResponse(rx, '5E 43 41 52 44 2F 49 4D 41 47 45')
						r3 = DL.Check_RXResponse(rx, '5E 31 37 31 32 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A')
						if r1 == True and r2 == True and r3 == True and DL.Check_RXResponse(rx, "56 A1"):
							DL.SetWindowText("blue", "Tag 56_Mask: PASS")
						else:
							DL.SetWindowText("red", "Tag 56_Mask: FAIL")
								
						r1 = DL.Check_StringAB(dec56, '56')
						r2 = DL.Check_StringAB(dec56, '42 36 35 31 30 30 30 30 30 30 30 30 30')
						r3 = DL.Check_StringAB(dec56, '5E 43 41 52 44 2F 49 4D 41 47 45')
						r4 = DL.Check_StringAB(dec56, '5E 31 37 31 32 32 30 31')
						if r1 == True and r2 == True and r3 == True and r4 == True and DL.Check_StringAB(alldata, "56 C1"):
							DL.SetWindowText("blue", "Tag 56_Enc: PASS")
						else:
							DL.SetWindowText("red", "Tag 56_Enc: FAIL")
									
						# Tag 57
						r1 = DL.Check_RXResponse(rx, '57 A1 65 10 CC CC CC CC')
						r2 = DL.Check_RXResponse(rx, 'D1 71 2C CC CC CC CC CC')
						if r1 == True and r2 == True:
							DL.SetWindowText("blue", "Tag 57_Mask: PASS")
						else:
							DL.SetWindowText("red", "Tag 57_Mask: FAIL")
									
						r1 = DL.Check_StringAB(dec57, '57')
						r2 = DL.Check_StringAB(dec57, '65 10 00 00 00 00')
						r3 = DL.Check_StringAB(dec57, 'D1 71 22 01')
						if r1 == True and r2 == True and r3 == True and DL.Check_StringAB(alldata, "57 C1"):
							DL.SetWindowText("blue", "Tag 57_Enc: PASS")
						else:
							DL.SetWindowText("red", "Tag 57_Enc: FAIL")	
									
						# Tags 9F39/ FFEE01/ DFEE26
						if DL.Check_RXResponse(rx, "9F39 ** 91") == False:
							DL.SetWindowText("Red", "Tag 9F39: FAIL")
								
						if DL.Check_RXResponse(rx, "FFEE01 ** DFEE300100") == False:
							DL.SetWindowText("Red", "Tag FFEE01: FAIL")
								
						if DL.Check_RXResponse(rx, "DFEE26 ** F100") == False:
							DL.SetWindowText("Red", "Tag DFEE26: FAIL")	
					if readermodel == 1:	
						DL.Check_RXResponse(rx, "E1 ** DF EE 12")
						alldata = DL.GetTLV(DL.Get_RXResponse(rx),"FF8105")
						ksn = DL.GetTLV(DL.Get_RXResponse(rx),"DFEE12")
						
						mask57 = DL.GetTLV(alldata,"57", 0)
						enc57 = DL.GetTLV(alldata,"57", 1)
						dec57 = DL.DecryptDLL(1,1, strKey, ksn, enc57)	
						
						mask5A = DL.GetTLV(alldata,"5A", 0)
						enc5A = DL.GetTLV(alldata,"5A", 1)
						dec5A = DL.DecryptDLL(1,1, strKey, ksn, enc5A)
					# Tag 57
						Result = DL.Check_StringAB(mask57, '47 61 CC CC CC CC 00 10 D')
						if Result == True:
							Result = DL.Check_StringAB(mask57, '01 2C CC CC CC CC CC CC CC CC')
						if Result == True and DL.Check_RXResponse(rx, "57 A1 13"):
							DL.SetWindowText("blue", "Tag 57_Mask: PASS")
						else:
							DL.SetWindowText("red", "Tag 57_Mask: FAIL")
							
						Result = DL.Check_StringAB(dec57, '57 13 47 61 73 90 01 01 00 10 D')
						if Result == True:
							Result = DL.Check_StringAB(dec57, '57 13 47 61 73 90 01 01 00 10 D3 01 21 20 00 12 33 99 00 03 1F')
						if Result == True and DL.Check_RXResponse(rx, "57 C1 18"):
							DL.SetWindowText("blue", "Tag 57_Enc: PASS")
						else:
							DL.SetWindowText("red", "Tag 57_Enc: FAIL")

					# Tag 5A
						Result = DL.Check_StringAB(mask5A, '47 61 CC CC CC CC 00 10')
						if Result == True and DL.Check_RXResponse(rx, "5A A1 08"):
							DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
						else:
							DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
							
						Result = DL.Check_StringAB(dec5A, '5A 08 47 61 73 90 01 01 00 10')
						if Result == True and DL.Check_RXResponse(rx, "5A C1 10"):
							DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
						else:
							DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
							
					# Tags 9F39/ FFEE01/ DFEE26
						if DL.Check_RXResponse(rx, "9F39 01 07") == False: 
							DL.SetWindowText("Red", "Tag 9F39: FAIL")
						if DL.Check_RXResponse(rx, "DFEE26 02 E100") == False: 
							DL.SetWindowText("Red", "Tag DFEE26: FAIL")
							
			# CT transaction
			if i == 3:				
				Result = Result and DL.Check_RXResponse("60 63 00 00")
				alldata = DL.Get_RXResponse(rx)
				CTresultcode = DL.GetTLV(alldata,"DFEE25")
				if (Result):
					Result = DL.Check_RXResponse(rx, '56 69 56 4F 74 65 63 68 32 00 60 00')
					if (Result):
						ksn = DL.GetTLV(alldata,"DFEE12")	
				
						mask57 = DL.GetTLV(alldata,"57", 0)
						enc57 = DL.GetTLV(alldata,"57", 1)
						dec57 = DL.DecryptDLL(1,1, strKey, ksn, enc57)	
				
						mask5A = DL.GetTLV(alldata,"5A", 0)
						enc5A = DL.GetTLV(alldata,"5A", 1)
						dec5A = DL.DecryptDLL(1,1, strKey, ksn, enc5A)	
					
						# Tag 57
						Result = DL.Check_RXResponse(rx, '57 A1 11 47 61 CC CC CC CC 00 10 D2 01 2C CC CC CC CC CC CC')
						if Result == True:
							DL.SetWindowText("blue", "Tag 57_Mask: PASS")
						else:
							DL.SetWindowText("red", "Tag 57_Mask: FAIL")
					
						Result = DL.Check_StringAB(dec57, '57 11 47 61 73 90 01 01 00 10 D2 01 22 01 01 23 45 67 89')
						if Result == True and DL.Check_RXResponse(rx, '57 C1'):
							DL.SetWindowText("blue", "Tag 57_Enc: PASS")
						else:
							DL.SetWindowText("red", "Tag 57_Enc: FAIL")

						# Tag 5A
						Result = DL.Check_RXResponse(rx, '5A A1 08 47 61 CC CC CC CC 00 10')
						if Result == True:
							DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
						else:
							DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
					
						Result = DL.Check_StringAB(dec5A, '5A 08 47 61 73 90 01 01 00 10')
						if Result == True and DL.Check_RXResponse(rx, '5A C1'):
							DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
						else:
							DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
					
						# Tags 9F39/ FFEE01/ DFEE26				
						if DL.Check_RXResponse(rx, "FFEE01 ** DFEE300101") == False: 
							DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
						if DL.Check_RXResponse(rx, "DFEE26 ** E000") == False: 
							DL.SetWindowText("Red", "Tag DFEE26: FAIL")
						
						DL.SendCommand('05-01')
						
# # Reset to default
# RetOfStep = DL.SendCommand('Reset to default')
# time.sleep(2)

RetOfStep = DL.SendCommand('Poll on Demand')
time.sleep(2)