#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''
strKey = '33333333333333333333333333333333'

# Set Param to Default (04-09)
if (Result):
	RetOfStep = DL.SendCommand('Set Param to Default (04-09)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("00")

# Check data key slot 03
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT KSN (81-0B)_0203')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("62 99 49 01 30 00 00 00")
		
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
	RetOfStep = DL.SendCommand('ACT (02-05) - CT only')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 00 ** C2 ")
		alldata = DL.Get_RXResponse(0)
		ksn = DL.GetTLV(alldata,"DFEE12")	
		
		mask5A = DL.GetTLV(alldata,"5A", 0)
		enc5A = DL.GetTLV(alldata,"5A", 1)
		dec5A = DL.DecryptDLL(0,2, strKey, ksn, enc5A)	
		
		#mask57 = DL.GetTLV(alldata,"57", 0)
		enc57 = DL.GetTLV(alldata,"57", 0)
		dec57 = DL.DecryptDLL(0,2, strKey, ksn, enc57)	
		
		Tag9F39 = DL.GetTLV(alldata,"9F39")
		TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
		TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
		
	# Tag 5A
		Result = DL.Check_StringAB(mask5A, '5A A1 08 54 13 CC CC CC CC 00 45')
		if Result == True and DL.Check_RXResponse("5A A1 08"):
			DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
		else:
			DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
			
		Result = DL.Check_StringAB(dec5A, '5A 08 54 13 33 00 89 02 00 45')
		if Result == True and DL.Check_RXResponse("5A C1 10"):
			DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
		else:
			DL.SetWindowText("red", "Tag 5A_Enc: FAIL")

	# Tag 57
		#Result = DL.Check_StringAB(57A1, '')
		#if Result == True and DL.Check_RXResponse("57 A1"):
			#DL.SetWindowText("blue", "Tag 57_Mask: PASS")
		#else:
			#DL.SetWindowText("red", "Tag 57_Mask: FAIL")
			
		Result = DL.Check_StringAB(dec57, '57 11 54 13 33 00 89 02 00 45 D2 51 22 01 01 94 60 02 7F')
		if Result == True and DL.Check_RXResponse("57 C1 20"):
			DL.SetWindowText("blue", "Tag 57_Enc: PASS")
		else:
			DL.SetWindowText("red", "Tag 57_Enc: FAIL")
			
	# Tags 9F39/ FFEE01/ DFEE26
		if Tag9F39 == "05": 
			DL.SetWindowText("blue", "Tag 9F39: PASS")
		else:
			DL.SetWindowText("Red", "Tag 9F39: FAIL")
		
		if (DL.Check_StringAB(TagFFEE01, "DFEE300101")): 
			DL.SetWindowText("blue", "Tag FFEE01: PASS")
		else:
			DL.SetWindowText("Red", "Tag FFEE01: FAIL")
		
		if TagDFEE26 == "C2": 
			DL.SetWindowText("blue", "Tag DFEE26: PASS")
		else:
			DL.SetWindowText("Red", "Tag DFEE26: FAIL")

