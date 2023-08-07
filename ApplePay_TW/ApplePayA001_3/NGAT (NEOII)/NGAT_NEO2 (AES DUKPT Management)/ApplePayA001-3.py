#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''
strKey = 'FEDCBA9876543210F1F1F1F1F1F1F1F1'

# Check reader is VP3350 or not
lcdtype = DL.ShowMessageBox("", "Is this VP3350?", 0)
if lcdtype == 1:
	DL.SetWindowText("Green", "*** This is VP3350 ***")
	RetOfStep = DL.SendCommand('0105 do not use LCD')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")
else:
	DL.SetWindowText("Green", "*** non-VP3350 reader ***")

# Get Data Encryption (C7-37)
if (Result):
	RetOfStep = DL.SendCommand('Get Data Encryption (C7-37)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 03")

# Check data encryption TYPE is AES	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("C7 00 00 06 01 02 00 00 00 00")
		if Result == False:
			DL.SetWindowText("red", "Please load AES key first.....")			
		
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
				DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** E5 ** DF EE 12")
				alldata = DL.Get_RXResponse(0)
				ksn = DL.GetTLV(alldata,"DFEE12")	
				
				mask57 = DL.GetTLV_Embedded(alldata,"57", 0)
				enc57 = DL.GetTLV_Embedded(alldata,"57", 1)
				dec57 = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc57)
				
				Tag9F39 = DL.GetTLV_Embedded(alldata,"9F39")
				TagFFEE01 = DL.GetTLV_Embedded(alldata,"FFEE01")
				TagDFEE26 = DL.GetTLV_Embedded(alldata,"DFEE26")
				
			# Tag 57
				if DL.Check_RXResponse("57 A1 13"):
					DL.SetWindowText("blue", "Tag 57_Mask: PASS")
				else:
					DL.SetWindowText("red", "Tag 57_Mask: FAIL")
					
				Result = DL.Check_StringAB(dec57, '5713')
				if Result == True and DL.Check_RXResponse("57 C1 20"):
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
				
				if TagDFEE26 == "E501": 
					DL.SetWindowText("blue", "Tag DFEE26: PASS")
				else:
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")
			
	if lcdtype == 0:
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
					DL.Check_StringAB(DL.Get_RXResponse(1), 'E3 ** DF EE 12')
					ksn = DL.GetTLV(alldata,"DFEE12")	
					
					mask57 = DL.GetTLV_Embedded(alldata,"57", 0)
					enc57 = DL.GetTLV_Embedded(alldata,"57", 1)
					dec57 = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc57)
					
					Tag9F39 = DL.GetTLV_Embedded(alldata,"9F39")
					TagFFEE01 = DL.GetTLV_Embedded(alldata,"FFEE01")
					TagDFEE26 = DL.GetTLV_Embedded(alldata,"DFEE26")
					
				# Tag 57
					if DL.Check_StringAB(alldata, "57 A1 13"):
						DL.SetWindowText("blue", "Tag 57_Mask: PASS")
					else:
						DL.SetWindowText("red", "Tag 57_Mask: FAIL")
						
					Result = DL.Check_StringAB(dec57, '5713')
					if Result == True and DL.Check_StringAB(alldata, "57 C1 20"):
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
						
					if TagDFEE26 == "E301": 
						DL.SetWindowText("blue", "Tag DFEE26: PASS")
					else:
						DL.SetWindowText("Red", "Tag DFEE26: FAIL")
					
if lcdtype == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")	