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
		
# Encryption Type -- TransArmor TDES
if (Result):
	RetOfStep = DL.SendCommand('2-use TransArmor TDES to encrypt (C7-32)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 00")
		if Result != True:
			Result = DL.SendCommand('0-use TDES to encrypt (C7-32)')
			if (Result):
				Result = DL.SendCommand('2-use TransArmor TDES to encrypt (C7-32)')
if (Result):
	RetOfStep = DL.SendCommand('Encryption Type -- TransArmor TDES')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 02")	
		
# Burst mode OFF & Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Burst mode Off')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")

# cmd 02-40, tap card
if (Result):
	RetOfStep = DL.SendCommand('Activate Transaction')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** E5 DF EE 12")
		alldata = DL.Get_RXResponse(0)
		ksn = DL.GetTLV(alldata,"DFEE12")	
		
		mask57 = DL.GetTLV(alldata,"57", 0)
		enc57 = DL.GetTLV(alldata,"57", 1)
		dec57 = DL.DecryptDLL(0,1, strKey, ksn, enc57)	
		
		mask5A = DL.GetTLV(alldata,"5A", 0)
		enc5A = DL.GetTLV(alldata,"5A", 1)
		dec5A = DL.DecryptDLL(0,1, strKey, ksn, enc5A)	
		
		Tag9F39 = DL.GetTLV(alldata,"9F39")
		TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
		TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
		
	# Tag 57
		Result = DL.Check_StringAB(mask57, '47 61 CC CC CC CC 00 10 D3 01 2C CC CC CC CC CC CC CC CC')
		if Result == True and DL.Check_RXResponse("57 A1 13"):
			DL.SetWindowText("blue", "Tag 57_Mask: PASS")
		else:
			DL.SetWindowText("red", "Tag 57_Mask: FAIL")
			
		Result = DL.Check_StringAB(dec57, '3B 34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30 3D 33 30 31 32 31 32 30 30 30 31 32 33 33 39 39 30 30 30 33 31 3F')
		if Result == True and DL.Check_RXResponse("57 C1 28"):
			DL.SetWindowText("blue", "Tag 57_Enc: PASS")
		else:
			DL.SetWindowText("red", "Tag 57_Enc: FAIL")

	# Tag 5A
		Result = DL.Check_StringAB(mask5A, '47 61 CC CC CC CC 00 10')
		if Result == True and DL.Check_RXResponse("5A A1 08"):
			DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
		else:
			DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
			
		Result = DL.Check_StringAB(dec5A, '34 37 36 31 37 33 39 30 30 31 30 31 30 30 31 30')
		if Result == True and DL.Check_RXResponse("5A C1 10"):
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
		
		if TagDFEE26 == "E506": 
			DL.SetWindowText("blue", "Tag DFEE26: PASS")
		else:
			DL.SetWindowText("Red", "Tag DFEE26: FAIL")