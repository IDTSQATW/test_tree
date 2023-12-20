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
		
# Auto poll support check
autopollcheck = DL.ShowMessageBox("", "Does the project support Auto-Poll mode?", 0)
if autopollcheck == 1: 
    autopoll = 6
else:
    autopoll = 4
        
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
	RetOfStep = DL.SendCommand('0105 do not use LCD')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")	
else:
	DL.SetWindowText("Green", "*** non-VP3350 reader ***")		

# Check data encryption TYPE is TDES DUKPT manage, TransArmor TDES, PIN key	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("C7 00 00 06 00 02 01 00 00 00")
		if Result == False:
			RetOfStep = DL.SendCommand('C7-A2 TDES DUKPT manage_TransArmor TDES, PIN key')
			if (RetOfStep):
				Result = DL.Check_RXResponse("C7 00 00 00")	
		
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
        
if (Result):
	RetOfStep = DL.SendCommand('DF7D = 02 (NEO2)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")

# cmd 02-40, MSR/ CL/ CT
if (Result):	
	for i in range (1, autopoll):
		if i <= 3:
			if i == 1:
				RetOfStep = DL.SendCommand('Poll on Demand')
				if (RetOfStep):
					Result = DL.Check_RXResponse("01 00 00 00")	
			if (Result):			
				if i == 1:
					RetOfStep = DL.SendCommand('02-40, MSR -- Discover w/ LCD')
				if i == 2:
					time.sleep(1)
					RetOfStep = DL.SendCommand('02-40, CL -- Discover w/ LCD')
				if i == 3:
					time.sleep(1)
					RetOfStep = DL.SendCommand('60-10, CT -- EMV Test Card V2 T=0 w/ LCD')
					rx = 1
		if i >= 4:
			if i == 4:
				RetOfStep = DL.SendCommand('Auto Poll 1rx')
				if (RetOfStep):
					Result = DL.Check_RXResponse("01 00 00 00")	
			if (Result):
				if i == 4:
					RetOfStep = DL.SendCommand('03-40, MSR -- Discover w/ LCD')
					rx = 1
					time.sleep(1)
				if i == 5:
					RetOfStep = DL.SendCommand('03-40, CL -- Discover w/ LCD')
					rx = 1
					time.sleep(1)
				
		if (RetOfStep):
			# MSR transaction
			if i == 1 or i == 4:
				sResult=DL.Get_RXResponse(rx)		
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
								#TRK1DecryptData = TRK1DecryptData[0:((objectMSR[0].msr_track1Length)*2)]
							if len(TRK2)> 0:
								DL.SetWindowText("blue", "Track 2:")
								TRK2DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK2)
								#TRK2DecryptData = TRK2DecryptData[0:((objectMSR[0].msr_track2Length)*2)]
							if len(TRK3) > 0:
								DL.SetWindowText("blue", "Track 3:")
								TRK3DecryptData = DL.DecryptDLL(EncryptType, EncryptMode, Key, KSN, TRK3)
								#TRK3DecryptData = TRK3DecryptData[0:((objectMSR[0].msr_track3Length)*2)]
									
							# Verify specific tags
							if DL.Check_RXResponse(rx, "9F39 ** 90") == False:
								DL.fails=DL.fails+1
								DL.SetWindowText("red", "Tag9F39: FAIL")
							if DL.Check_RXResponse(rx, "FFEE01 ** DFEE30010C") == False:	
								DL.fails=DL.fails+1
								DL.SetWindowText("red", "TagFFEE01: FAIL")	
							if DL.Check_RXResponse(rx, "DFEE26 ** EC06") == False:	
								DL.fails=DL.fails+1
								DL.SetWindowText("red", "TagDFEE26: FAIL")
																						
							# Discover	
							TR1maskdata = "%*6510********0026^CARD/IMAGE 03             ^1712****************?;6510********0026=1712****************?"
							TR1plaintextdata = "2542363531303030303030303030303032365E434152442F494D414745203033202020202020202020202020205E31373132323031313030303032313030303030303F3B363531303030303030303030303032363D31373132323031313030303032313030303030303F"
											
							Result = DL.Check_StringAB(TR1maskdata, Track1_CardData)
							if Result != True:
								DL.fails=DL.fails+1
								DL.SetWindowText("red", "TR1maskdata: FAIL")
							Result = DL.Check_StringAB(TR1plaintextdata, TRK1DecryptData)
							if Result != True:
								DL.fails=DL.fails+1
								DL.SetWindowText("red", "TR1plaintextdata: FAIL")
			# CL transaction
			if i == 2 or i == 5:
				if (RetOfStep):
					if readermodel == 0:
						alldata=DL.Get_RXResponse(rx)		
						DL.Check_RXResponse(rx, 'F5 ** DF EE 12')
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
						r1 = DL.Check_StringAB(maskDFEF17, '2A363531302A2A2A2A2A2A2A2A')
						r2 = DL.Check_StringAB(maskDFEF17, '5E434152442F494D414745')
						r3 = DL.Check_StringAB(maskDFEF17, '5E313731322A2A2A2A2A2A2A2A2A2A2A2A2A')
						if r1 == True and r2 == True and r3 == True and DL.Check_StringAB(alldata, "DF EF 17 A1"):
							DL.SetWindowText("blue", "Tag DFEF17_Mask: PASS")
						else:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "Tag DFEF17_Mask: FAIL")
									
						r2 = DL.Check_StringAB(decDFEF17, '25 42 36 35 31 30 30 30 30 30 30 30 30 30')
						r3 = DL.Check_StringAB(decDFEF17, '5E 43 41 52 44 2F 49 4D 41 47 45')
						r4 = DL.Check_StringAB(decDFEF17, '5E 31 37 31 32 32 30 31')
						if r2 == True and r3 == True and r4 == True and DL.Check_StringAB(alldata, "DF EF 17 C1"):
							DL.SetWindowText("blue", "Tag DFEF17_Enc: PASS")
						else:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "Tag DFEF17_Enc: FAIL")

						# Tag DFEF18
						r1 = DL.Check_StringAB(maskDFEF18, '36 35 31 30 2A 2A 2A 2A 2A 2A 2A 2A')
						r2 = DL.Check_StringAB(maskDFEF18, '3D 31 37 31 32 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A')
						if r1 == True and r2 == True and DL.Check_StringAB(alldata, "DF EF 18 A1"):
							DL.SetWindowText("blue", "Tag DFEF18_Mask: PASS")
						else:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "Tag DFEF18_Mask: FAIL")
									
						r2 = DL.Check_StringAB(decDFEF18, '3B 36 35 31 30 30 30 30 30 30 30 30 30')
						r3 = DL.Check_StringAB(decDFEF18, '3D 31 37 31 32 32 30 31')
						if r2 == True and r3 == True and DL.Check_StringAB(alldata, "DF EF 18 C1"):
							DL.SetWindowText("blue", "Tag DFEF18_Enc: PASS")
						else:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "Tag DFEF18_Enc: FAIL")
									
						# Tag 56
						r1 = DL.Check_StringAB(mask56, '2A 36 35 31 30 2A 2A 2A 2A 2A 2A 2A 2A')
						r2 = DL.Check_StringAB(mask56, '5E 43 41 52 44 2F 49 4D 41 47 45')
						r3 = DL.Check_StringAB(mask56, '5E 31 37 31 32 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A')
						if r1 == True and r2 == True and r3 == True and DL.Check_StringAB(alldata, "56 A1"):
							DL.SetWindowText("blue", "Tag 56_Mask: PASS")
						else:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "Tag 56_Mask: FAIL")
								
						r2 = DL.Check_StringAB(dec56, '25 42 36 35 31 30 30 30 30 30 30 30 30 30')
						r3 = DL.Check_StringAB(dec56, '5E 43 41 52 44 2F 49 4D 41 47 45')
						r4 = DL.Check_StringAB(dec56, '5E 31 37 31 32 32 30 31')
						if r2 == True and r3 == True and r4 == True and DL.Check_StringAB(alldata, "56 C1"):
							DL.SetWindowText("blue", "Tag 56_Enc: PASS")
						else:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "Tag 56_Enc: FAIL")
									
						# Tag 57
						r1 = DL.Check_StringAB(mask57, '65 10 CC CC CC CC')
						r2 = DL.Check_StringAB(mask57, 'D1 71 2C CC CC CC CC CC')
						if r1 == True and r2 == True and DL.Check_StringAB(alldata, "57 A1"):
							DL.SetWindowText("blue", "Tag 57_Mask: PASS")
						else:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "Tag 57_Mask: FAIL")
									
						r2 = DL.Check_StringAB(dec57, '3B363531303030303030303030')
						r3 = DL.Check_StringAB(dec57, '3D31373132323031')
						if r2 == True and r3 == True and DL.Check_StringAB(alldata, "57 C1"):
							DL.SetWindowText("blue", "Tag 57_Enc: PASS")
						else:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "Tag 57_Enc: FAIL")	
									
						# Tags 9F39/ FFEE01/ DFEE26
						if DL.Check_RXResponse(rx, "9F39 ** 91") == False:
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag 9F39: FAIL")
						if DL.Check_RXResponse(rx, "FFEE01 ** DFEE300100") == False:
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag FFEE01: FAIL")
						if DL.Check_RXResponse(rx, "DFEE26 ** F506") == False:
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag DFEE26: FAIL")	
					if readermodel == 1:	
						DL.Check_RXResponse(rx, "E5 ** DF EE 12")
						alldata = DL.GetTLV(DL.Get_RXResponse(rx),"FF8105")
						ksn = DL.GetTLV(DL.Get_RXResponse(rx),"DFEE12")
						
						mask57 = DL.GetTLV(alldata,"57", 0)
						enc57 = DL.GetTLV(alldata,"57", 1)
						dec57 = DL.DecryptDLL(1,1, strKey, ksn, enc57)	
						
					# Tag 57
						r1 = DL.Check_StringAB(mask57, '36 07 CC CC CC C0 00 1D 49 12 CC CC CC CC CC CC CC CC')
						if r1 == True and DL.Check_RXResponse(rx, "57 A1 12"):
							DL.SetWindowText("blue", "Tag 57_Mask: PASS")
						else:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "Tag 57_Mask: FAIL")
							
						Result = DL.Check_StringAB(dec57, '3B3336303730353030303030303030313D34393132313031303030303333323131323330313F')
						if Result == True and DL.Check_RXResponse(rx, "57 C1 28"):
							DL.SetWindowText("blue", "Tag 57_Enc: PASS")
						else:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "Tag 57_Enc: FAIL")
							
					# Tags 9F39/ FFEE01/ DFEE26
						if DL.Check_RXResponse(rx, "9F39 01 07") == False: 
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag 9F39: FAIL")
						if DL.Check_RXResponse(rx, "DFEE26 02 E506") == False: 
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag DFEE26: FAIL")							
			# CT transaction
			if i == 3:						
				Result = Result and DL.Check_RXResponse("60 63 00 00")
				alldata = DL.Get_RXResponse(rx)
				CTresultcode = DL.GetTLV(alldata,"DFEE25")
				if (Result):
					Result = DL.Check_StringAB(DL.Get_RXResponse(rx), '56 69 56 4F 74 65 63 68 32 00 60 00')
					if (Result):
						ksn = DL.GetTLV(alldata,"DFEE12")	
				
						mask57 = DL.GetTLV(alldata,"57", 0)
						enc57 = DL.GetTLV(alldata,"57", 1)
						dec57 = DL.DecryptDLL(1,1, strKey, ksn, enc57)	
				
						mask5A = DL.GetTLV(alldata,"5A", 0)
						enc5A = DL.GetTLV(alldata,"5A", 1)
						dec5A = DL.DecryptDLL(1,1, strKey, ksn, enc5A)	
				
						# Tag 57
						Result = DL.Check_StringAB(mask57, '47 61 CC CC CC CC 00 10 D2 01 2C CC CC CC CC CC CC')
						if Result == True and DL.Check_StringAB(DL.Get_RXResponse(rx), '57 A1 11'):
							DL.SetWindowText("blue", "Tag 57_Mask: PASS")
						else:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "Tag 57_Mask: FAIL")
					
						Result = DL.Check_StringAB(dec57, '34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 32 30 31 32 32 30 31 30 31 32 33 34 35 36 37 38 39')
						if Result == True and DL.Check_StringAB(DL.Get_RXResponse(rx), '57 C1'):
							DL.SetWindowText("blue", "Tag 57_Enc: PASS")
						else:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "Tag 57_Enc: FAIL")

						# Tag 5A
						Result = DL.Check_StringAB(mask5A, '47 61 CC CC CC CC 00 10')
						if Result == True and DL.Check_StringAB(DL.Get_RXResponse(rx), '5A A1 08'):
							DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
						else:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
					
						Result = DL.Check_StringAB(dec5A, '34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30')
						if Result == True and DL.Check_StringAB(DL.Get_RXResponse(rx), '5A C1'):
							DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
						else:
							DL.fails=DL.fails+1
							DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
					
						# Tags 9F39/ FFEE01/ DFEE26				
						if DL.Check_RXResponse(rx, "FFEE01 ** DFEE300101") == False: 
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
						if DL.Check_RXResponse(rx, "DFEE26 ** E406") == False: 
							DL.fails=DL.fails+1
							DL.SetWindowText("Red", "Tag DFEE26: FAIL")
						
						DL.SendCommand('05-01')
						time.sleep(1)
					else:
						DL.fails=DL.fails+1
else:
	DL.fails=DL.fails+1

RetOfStep = DL.SendCommand('Poll on Demand')
time.sleep(1)

if readermodel == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")
        
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )