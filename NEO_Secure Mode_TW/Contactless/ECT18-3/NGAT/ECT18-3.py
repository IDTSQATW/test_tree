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

# Get Data Encryption (C7-37)
if (Result):
	RetOfStep = DL.SendCommand('Get Data Encryption (C7-37)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 03")

# Encryption Type -- TDES
if (Result):
	RetOfStep = DL.SendCommand('Encryption Type -- TDES')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 00")		
		
# Burst mode OFF
if (Result):
	RetOfStep = DL.SendCommand('Burst mode Off')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	

# cmd 02-40/ 03-40, tap card
if (Result):
	for i in range(1, 2):
		if i == 1:
			RetOfStep = DL.SendCommand('Poll on Demand')
			if (RetOfStep):
				Result = DL.Check_RXResponse("01 00 00 00")
		if i == 2:
			RetOfStep = DL.SendCommand('Auto Poll')
			if (RetOfStep):
				Result = DL.Check_RXResponse("01 00 00 00")
		
		if (Result):
			if i == 1:
				RetOfStep = DL.SendCommand('AT Transaction')
			if i == 2:
				RetOfStep = DL.SendCommand('Get Transaction Result')
			
			if (RetOfStep):
				if i == 1:
					alldata = DL.Get_RXResponse(0)
					DL.Check_StringAB(alldata, '56 69 56 4F 74 65 63 68 32 00 02 23')
				if i == 2:
					alldata = DL.Get_RXResponse(1)	
					DL.Check_StringAB(alldata, '56 69 56 4F 74 65 63 68 32 00 03 23')
				
				DL.Check_StringAB(alldata, 'E1 DF EE 12')
				ksn = DL.GetTLV(alldata,"DFEE12")	
				
				maskDFEF18 = DL.GetTLV(alldata,"DFEF18", 0)
				encDFEF18 = DL.GetTLV(alldata,"DFEF18", 1)
				decDFEF18 = DL.DecryptDLL(0,1, strKey, ksn, encDFEF18)	
				
				mask57 = DL.GetTLV(alldata,"57", 0)
				enc57 = DL.GetTLV(alldata,"57", 1)
				dec57 = DL.DecryptDLL(0,1, strKey, ksn, enc57)	
				
				mask5A = DL.GetTLV(alldata,"5A", 0)
				enc5A = DL.GetTLV(alldata,"5A", 1)
				dec5A = DL.DecryptDLL(0,1, strKey, ksn, enc5A)					
				
				Tag9F39 = DL.GetTLV(alldata,"9F39")
				TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
				TagDFEE26 = DL.GetTLV(alldata,"DFEE26")

			# Tag DFEF18
				Result = DL.Check_StringAB(maskDFEF18, '35 34 31 33 2A 2A 2A 2A 2A 2A 2A 2A 31 35 31 33 3D 30 35 31 32 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A')
				if Result == True and DL.Check_StringAB(alldata, "DF EF 18 A1 22"):
					DL.SetWindowText("blue", "Tag DFEF18_Mask: PASS")
				else:
					DL.SetWindowText("red", "Tag DFEF18_Mask: FAIL")
					
				Result = DL.Check_StringAB(decDFEF18, 'DF EF 18 22 35 34 31 33 33 33 39 30 30 30 30 30 31 35 31 33 3D 30 35 31 32 32 32 30 30 31 32 33 34 35 36 37 38 39')
				if Result == True and DL.Check_StringAB(alldata, "DF EF 18 C1 28"):
					DL.SetWindowText("blue", "Tag DFEF18_Enc: PASS")
				else:
					DL.SetWindowText("red", "Tag DFEF18_Enc: FAIL")
									
			# Tag 57
				Result = DL.Check_StringAB(mask57, '54 13 CC CC CC CC 15 13 D0 51 2C CC CC CC CC CC CC')
				if Result == True and DL.Check_StringAB(alldata, "57 A1 11"):
					DL.SetWindowText("blue", "Tag 57_Mask: PASS")
				else:
					DL.SetWindowText("red", "Tag 57_Mask: FAIL")
					
				Result = DL.Check_StringAB(dec57, '57 11 54 13 33 90 00 00 15 13 D0 51 22 20 01 23 45 67 89')
				if Result == True and DL.Check_StringAB(alldata, "57 C1 18"):
					DL.SetWindowText("blue", "Tag 57_Enc: PASS")
				else:
					DL.SetWindowText("red", "Tag 57_Enc: FAIL")
					
			# Tag 5A
				Result = DL.Check_StringAB(mask5A, '54 13 CC CC CC CC 15 13')
				if Result == True and DL.Check_StringAB(alldata, "5A A1 08"):
					DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
				else:
					DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
					
				Result = DL.Check_StringAB(dec5A, '5A 08 54 13 33 90 00 00 15 13')
				if Result == True and DL.Check_StringAB(alldata, "5A C1 10"):
					DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
				else:
					DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
					
			# Tags 9F39/ FFEE01/ DFEE26
				if Tag9F39 == "07": 
					DL.SetWindowText("blue", "Tag 9F39: PASS")
				else:
					DL.SetWindowText("Red", "Tag 9F39: FAIL")
				
				if (DL.Check_StringAB(TagFFEE01, "DFEE300100")): 
					DL.SetWindowText("blue", "Tag FFEE01: PASS")
				else:
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
				if TagDFEE26 == "E100": 
					DL.SetWindowText("blue", "Tag DFEE26: PASS")
				else:
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")
		
				RetOfStep = DL.SendCommand('03-03')
				time.sleep(4)