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

# Check project has LCD or not
lcdtype = DL.ShowMessageBox("", "Does the project has LCD?", 0)
if lcdtype == 1:
	DL.SetWindowText("Green", "*** The project has LCD ***")
else:
	DL.SetWindowText("Green", "*** The project has NO LCD ***")

# Check data encryption TYPE is TDES	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("C7 00 00 06 00 01 00 00 00 00")
		
# Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")

# Set group 80 -- DF 81 1B = 80
if (Result):
	RetOfStep = DL.SendCommand('Set group 80 -- DF 81 1B = 80')
	if (RetOfStep):
		Result = DL.Check_RXResponse("04 00 00 00")		
		
# cmd 02-40, tap card
if (Result):
	if lcdtype == 1:
		RetOfStep = DL.SendCommand('Activate Transaction w/ LCD')
		rx = 0
	if lcdtype == 0:
		RetOfStep = DL.SendCommand('Activate Transaction w/o LCD')	
		rx = 4
	if (RetOfStep):
		DL.Check_RXResponse(rx, "56 69 56 4F 74 65 63 68 32 00 02 23 ** E1 ** DF EE 12")
		alldata = DL.Get_RXResponse(rx)
		ksn = DL.GetTLV(DL.Get_RXResponse(rx),"DFEE12")	

		tagFF8105 = DL.GetTLV(alldata,"FF8105", 0)
		mask5A = DL.GetTLV(tagFF8105,"5A", 0)
		enc5A = DL.GetTLV(tagFF8105,"5A", 1)
		dec5A = DL.DecryptDLL(0,2, strKey, ksn, enc5A)	
		
		mask57 = DL.GetTLV(tagFF8105,"57", 0)
		enc57 = DL.GetTLV(tagFF8105,"57", 1)
		dec57 = DL.DecryptDLL(0,2, strKey, ksn, enc57)	

		if lcdtype == 1:		
		# Tag 5A
			Result = DL.Check_StringAB(mask5A, '51 28 CC CC CC CC')
			if Result == True and DL.Check_RXResponse(rx, "5A A1 08"):
				DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
			else:
				DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
				
			Result = DL.Check_StringAB(dec5A, '5A 08 51 28 57 01 00 03')
			if Result == True and DL.Check_RXResponse(rx, "5A C1 10"):
				DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
			else:
				DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
				
		# Tag 57
			Result = DL.Check_StringAB(mask57, '51 28 CC CC CC CC')
			if (Result):
				Result = DL.Check_StringAB(mask57, 'D1 80 3C CC CC CC CC CC')
			if Result == True and DL.Check_RXResponse(rx, "57 A1 10"):
				DL.SetWindowText("blue", "Tag 57_Mask: PASS")
			else:
				DL.SetWindowText("red", "Tag 57_Mask: FAIL")
				
			Result = DL.Check_StringAB(dec57, '57 10 51 28 57 01 00 03')
			if (Result):
				Result = DL.Check_StringAB(dec57, 'D1 80 36 22')
			if Result == True and DL.Check_RXResponse(rx, "57 C1 20"):
				DL.SetWindowText("blue", "Tag 57_Enc: PASS")
			else:
				DL.SetWindowText("red", "Tag 57_Enc: FAIL")

		if lcdtype == 0:
		# Tag 5A
			Result = DL.Check_StringAB(mask5A, '5413CCCCCCCC0010')
			if Result == True and DL.Check_RXResponse(rx, "5A A1 08"):
				DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
			else:
				DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
				
			Result = DL.Check_StringAB(dec5A, '5A085413330089600010000000000000')
			if Result == True and DL.Check_RXResponse(rx, "5A C1 10"):
				DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
			else:
				DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
				
		# Tag 57
			Result = DL.Check_StringAB(mask57, '5413CCCCCCCC0010D1412CCCCCCCCCCCCC')
			if Result == True and DL.Check_RXResponse(rx, "57A111"):
				DL.SetWindowText("blue", "Tag 57_Mask: PASS")
			else:
				DL.SetWindowText("red", "Tag 57_Mask: FAIL")
				
			Result = DL.Check_StringAB(dec57, '57115413330089600010D141220101234091720000000000')
			if Result == True and DL.Check_RXResponse(rx, "57 C1 20"):
				DL.SetWindowText("blue", "Tag 57_Enc: PASS")
			else:
				DL.SetWindowText("red", "Tag 57_Enc: FAIL")	
				
	# Tags 9F39/ FFEE01/ DFEE26
		if DL.Check_RXResponse(rx, "9F39 01 07") == False: 
			DL.SetWindowText("Red", "Tag 9F39: FAIL")
				
		if DL.Check_RXResponse(rx, "FFEE01 ** DFEE300100") == False: 
			DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
		if DL.Check_RXResponse(rx, "DFEE26 02 E100") == False: 
			DL.SetWindowText("Red", "Tag DFEE26: FAIL")
			
# Reset to default
RetOfStep = DL.SendCommand('Reset to default')
if (RetOfStep):
	DL.Check_RXResponse("04 00 00 00")	