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

# Get Encryption status (03)
if (Result):
	RetOfStep = DL.SendCommand('Get Encryption status (03)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 03")

# Encryption Type -- TDES
if (Result):
	RetOfStep = DL.SendCommand('Encryption Type -- TDES')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 00")

# Set group 80 -- DF 81 1B = 80
if (Result):
	RetOfStep = DL.SendCommand('Set group 80 -- DF 81 1B = 80')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")		
		
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
		DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** E1 DF EE 12")
		alldata = DL.Get_RXResponse(0)
		ksn = DL.GetTLV(alldata,"DFEE12")
		
		tagFF8105 = DL.GetTLV(alldata,"FF8105")
		mask5A = DL.GetTLV(tagFF8105,"5A", 0)
		enc5A = DL.GetTLV(tagFF8105,"5A", 1)
		dec5A = DL.DecryptDLL(0,1, strKey, ksn, enc5A)	
		mask57 = DL.GetTLV(tagFF8105,"57", 0)
		enc57 = DL.GetTLV(tagFF8105,"57", 1)
		dec57 = DL.DecryptDLL(0,1, strKey, ksn, enc57)	
		
		Tag9F39 = DL.GetTLV(alldata,"9F39")
		TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
		TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
	
	# Tag 5A
		Result = DL.Check_StringAB(mask5A, '51 28 CC CC CC CC')
		if Result == True and DL.Check_RXResponse("** 5A A1 08 **"):
			DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
		else:
			DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
			
		Result = DL.Check_StringAB(dec5A, '5A 08 51 28 57 01 00 03')
		if Result == True and DL.Check_RXResponse("** 5A C1 10**"):
			DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
		else:
			DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
			
	# Tag 57
		Result = DL.Check_StringAB(mask57, '51 28 CC CC CC CC')
		if (Result):
			Result = DL.Check_StringAB(mask57, 'D1 80 3C CC CC CC CC CC')
		if Result == True and DL.Check_RXResponse("** 57 A1 10 **"):
			DL.SetWindowText("blue", "Tag 57_Mask: PASS")
		else:
			DL.SetWindowText("red", "Tag 57_Mask: FAIL")
			
		Result = DL.Check_StringAB(dec57, '57 10 51 28 57 01 00 03')
		if (Result):
			Result = DL.Check_StringAB(dec57, 'D1 80 36 22')
		if Result == True and DL.Check_RXResponse("** 57 C1 18 **"):
			DL.SetWindowText("blue", "Tag 57_Enc: PASS")
		else:
			DL.SetWindowText("red", "Tag 57_Enc: FAIL")
			
	# Tags 9F39/ FFEE01/ DFEE26
		if Tag9F39 == "07": 
			DL.SetWindowText("blue", "Tag 9F39: PASS")
		else:
			DL.SetWindowText("Red", "Tag 9F39: FAIL")
		
		if TagFFEE01 == "DFEE300100": 
			DL.SetWindowText("blue", "Tag FFEE01: PASS")
		else:
			DL.SetWindowText("Red", "Tag FFEE01: FAIL")
		
		if TagDFEE26 == "E100": 
			DL.SetWindowText("blue", "Tag DFEE26: PASS")
		else:
			DL.SetWindowText("Red", "Tag DFEE26: FAIL")