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
		Result = Result and DL.Check_RXResponse("C7 00 00 01 02")
		if Result != True:
			DL.SetWindowText("red", "Please load data key (AES) and set cmd C7-36 = 02 first!")

# Encryption Type -- AES
if (Result):
	RetOfStep = DL.SendCommand('Encryption Type -- AES')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 01")		
		if Result == False:
			DL.SetWindowText("red", "Set encryption Type = AES first...")
		
# Burst mode OFF	
if (Result):
	RetOfStep = DL.SendCommand('Burst mode Off')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	
		
# Tag 9F66	
if (Result):
	RetOfStep = DL.SendCommand('Tag 9F66')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	

if (Result):
	# Poll on demand
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")

		# cmd 02-40, tap card
		if (Result):
			RetOfStep = DL.SendCommand('Activate Transaction')
			if (RetOfStep):
				DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** 43")
				alldata = DL.Get_RXResponse(0)
				
				Tag57 = DL.GetTLV(alldata,"57")
				
				Tag9F39 = DL.GetTLV(alldata,"9F39")
				TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
				TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
				
			# Tag 57					
				Result = DL.Check_RXResponse(0, '5713')
				if Result == True:
					DL.SetWindowText("blue", "Tag 57: PASS")
				else:
					DL.SetWindowText("red", "Tag 57: FAIL")
					
			# Tags 9F39/ FFEE01/ DFEE26
				if Tag9F39 == "07": 
					DL.SetWindowText("blue", "Tag 9F39: PASS")
				else:
					DL.SetWindowText("Red", "Tag 9F39: FAIL")
				
				if (DL.Check_StringAB(TagFFEE01, "DF300100")): 
					DL.SetWindowText("blue", "Tag FFEE01: PASS")
				else:
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
				if TagDFEE26 == "43": 
					DL.SetWindowText("blue", "Tag DFEE26: PASS")
				else:
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")
			
	# Auto Poll
	RetOfStep = DL.SendCommand('Auto Poll')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")
	
	# cmd 03-40
		if (Result):
			RetOfStep = DL.SendCommand('Get Transaction result')
			if (RetOfStep):
				alldata = DL.Get_RXResponse(1)
				DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 03 23')
				DL.Check_StringAB(DL.Get_RXResponse(1), '43')
					
				Tag57 = DL.GetTLV(alldata,"57")
				
				Tag9F39 = DL.GetTLV(alldata,"9F39")
				TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
				TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
				
			# Tag 57					
				Result = DL.Check_RXResponse(1, '5713')
				if Result == True:
					DL.SetWindowText("blue", "Tag 57: PASS")
				else:
					DL.SetWindowText("red", "Tag 57: FAIL")
		
			# Tags 9F39/ FFEE01/ DFEE26
				if Tag9F39 == "07": 
					DL.SetWindowText("blue", "Tag 9F39: PASS")
				else:
					DL.SetWindowText("Red", "Tag 9F39: FAIL")
				
				if (DL.Check_StringAB(TagFFEE01, "DF300100")): 
					DL.SetWindowText("blue", "Tag FFEE01: PASS")
				else:
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
				if TagDFEE26 == "43": 
					DL.SetWindowText("blue", "Tag DFEE26: PASS")
				else:
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")