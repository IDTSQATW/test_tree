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

# Enable encryption (02)
if (Result):
	RetOfStep = DL.SendCommand('Enable Encryption (02)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 00")

# Encryption Type -- AES
if (Result):
	RetOfStep = DL.SendCommand('Encryption Type -- AES')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 01")		
		
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
		DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** 63")
		alldata = DL.Get_RXResponse(0)
	
		mask5A = DL.GetTLV_Embedded(alldata,"5A", 0)
		mask57 = DL.GetTLV_Embedded(alldata,"57", 0)
		
		Tag9F39 = DL.GetTLV(alldata,"9F39")
		TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
		TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
	
	# Tag 5A
		Result = DL.Check_StringAB(mask5A, '5A085413330089600010000000000000')
		if Result == True:
			DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
		else:
			DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
			
	# Tag 57
		Result = DL.Check_StringAB(mask57, '57115413330089600010D141220101234091720000000000')
		if Result == True:
			DL.SetWindowText("blue", "Tag 57_Mask: PASS")
		else:
			DL.SetWindowText("red", "Tag 57_Mask: FAIL")
			
	# Tags 9F39/ FFEE01/ DFEE26
		if DL.Check_RXResponse("9F39 01 07"): 
			DL.SetWindowText("blue", "Tag 9F39: PASS")
		else:
			DL.SetWindowText("Red", "Tag 9F39: FAIL")
		
		if DL.Check_RXResponse("FEE01 ** DFEE300100"): 
			DL.SetWindowText("blue", "Tag FFEE01: PASS")
		else:
			DL.SetWindowText("Red", "Tag FFEE01: FAIL")
		
		if DL.Check_RXResponse("DFEE26 02 6300"): 
			DL.SetWindowText("blue", "Tag DFEE26: PASS")
		else:
			DL.SetWindowText("Red", "Tag DFEE26: FAIL")