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

# Encryption Type -- AES
if (Result):
	RetOfStep = DL.SendCommand('Encryption Type -- AES')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 01")		
		
# Burst mode OFF	
if (Result):
	RetOfStep = DL.SendCommand('Burst mode Off')
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
				DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** E3 DF EE 12")
				alldata = DL.Get_RXResponse(0)
				ksn = DL.GetTLV(alldata,"DFEE12")	
				
				mask57 = DL.GetTLV(alldata,"57", 0)
				enc57 = DL.GetTLV(alldata,"57", 1)
				dec57 = DL.DecryptDLL(0,2, strKey, ksn, enc57)	
				
				Tag9F39 = DL.GetTLV(alldata,"9F39")
				TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
				TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
				
			# Tag 57
				Result = DL.Check_RXResponse("57 A1 13")
				if Result == True:
					DL.SetWindowText("blue", "Tag 57_Mask: PASS")
				else:
					DL.SetWindowText("red", "Tag 57_Mask: FAIL")
					
				Result = DL.Check_RXResponse("57 C1")
				if Result == True:
					DL.SetWindowText("blue", "Tag 57_Enc: PASS")
				else:
					DL.SetWindowText("red", "Tag 57_Enc: FAIL")
					
			# Tags 9F39/ FFEE01/ DFEE26
				if Tag9F39 == "07": 
					DL.SetWindowText("blue", "Tag 9F39: PASS")
				else:
					DL.SetWindowText("Red", "Tag 9F39: FAIL")
				
				if (DL.Check_StringAB(TagFFEE01, "DFEE300100")): 
					DL.SetWindowText("blue", "Tag FFEE01: PASS")
				else:
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
				if TagDFEE26 == "E300": 
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
				DL.Check_StringAB(DL.Get_RXResponse(1), 'E3 DF EE 12')
				ksn = DL.GetTLV(alldata,"DFEE12")	
					
				mask57 = DL.GetTLV(alldata,"57", 0)
				enc57 = DL.GetTLV(alldata,"57", 1)
				dec57 = DL.DecryptDLL(0,2, strKey, ksn, enc57)	
					
				Tag9F39 = DL.GetTLV(alldata,"9F39")
				TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
				TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
				
			# Tag 57
				Result = DL.Check_RXResponse(1, "57 A1 13")
				if Result == True:
					DL.SetWindowText("blue", "Tag 57_Mask: PASS")
				else:
					DL.SetWindowText("red", "Tag 57_Mask: FAIL")
					
				Result = DL.Check_RXResponse(1, "57 C1")
				if Result == True:
					DL.SetWindowText("blue", "Tag 57_Enc: PASS")
				else:
					DL.SetWindowText("red", "Tag 57_Enc: FAIL")
		
			# Tags 9F39/ FFEE01/ DFEE26
				if Tag9F39 == "07": 
					DL.SetWindowText("blue", "Tag 9F39: PASS")
				else:
					DL.SetWindowText("Red", "Tag 9F39: FAIL")
				
				if (DL.Check_StringAB(TagFFEE01, "DFEE300100")): 
					DL.SetWindowText("blue", "Tag FFEE01: PASS")
				else:
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
				if TagDFEE26 == "E300": 
					DL.SetWindowText("blue", "Tag DFEE26: PASS")
				else:
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")