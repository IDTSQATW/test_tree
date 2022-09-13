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
		Result = Result and DL.Check_RXResponse("C7 00 00 06 00 00 00 00 00 00")
		
# Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")

# cmd 02-40, tap card
if (Result):
	if lcdtype == 1:
		RetOfStep = DL.SendCommand('Activate Transaction w/ LCD')
	if lcdtype == 0:
		RetOfStep = DL.SendCommand('Activate Transaction w/o LCD')		
	if (RetOfStep):
		if lcdtype == 1:
			rx = 0
			DL.Check_RXResponse(rx, "56 69 56 4F 74 65 63 68 32 00 02 23 ** E1 ** DF EE 12")
			alldata = DL.Get_RXResponse(rx)
		if lcdtype == 0:
			rx = 4
			DL.Check_RXResponse(rx, "56 69 56 4F 74 65 63 68 32 00 02 23 ** E1 ** DF EE 12")
			alldata = DL.GetTLV(DL.Get_RXResponse(rx),"FF8105")
		
		ksn = DL.GetTLV(DL.Get_RXResponse(rx),"DFEE12")
		
		mask57 = DL.GetTLV(alldata,"57", 0)
		enc57 = DL.GetTLV(alldata,"57", 1)
		dec57 = DL.DecryptDLL(0,1, strKey, ksn, enc57)	
		
		mask5A = DL.GetTLV(alldata,"5A", 0)
		enc5A = DL.GetTLV(alldata,"5A", 1)
		dec5A = DL.DecryptDLL(0,1, strKey, ksn, enc5A)	
		
	# Tag 57
		Result = DL.Check_StringAB(mask57, '47 61 CC CC CC CC 00 10 D')
		if Result == True:
			Result = DL.Check_StringAB(mask57, '01 2C CC CC CC CC CC CC CC CC')
		if Result == True and DL.Check_RXResponse(rx, "57 A1 13"):
			DL.SetWindowText("blue", "Tag 57_Mask: PASS")
		else:
			DL.SetWindowText("red", "Tag 57_Mask: FAIL")
			
		Result = DL.Check_StringAB(dec57, '57 13 47 61 73 90 01 01 00 10 D')
		if Result == True:
			Result = DL.Check_StringAB(dec57, '57 13 47 61 73 90 01 01 00 10 D3 01 21 20 00 12 33 99 00 03 1F')
		if Result == True and DL.Check_RXResponse(rx, "57 C1 18"):
			DL.SetWindowText("blue", "Tag 57_Enc: PASS")
		else:
			DL.SetWindowText("red", "Tag 57_Enc: FAIL")

	# Tag 5A
		Result = DL.Check_StringAB(mask5A, '47 61 CC CC CC CC 00 10')
		if Result == True and DL.Check_RXResponse(rx, "5A A1 08"):
			DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
		else:
			DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
			
		Result = DL.Check_StringAB(dec5A, '5A 08 47 61 73 90 01 01 00 10')
		if Result == True and DL.Check_RXResponse(rx, "5A C1 10"):
			DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
		else:
			DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
			
	# Tags 9F39/ FFEE01/ DFEE26
		if DL.Check_RXResponse(rx, "9F39 01 07") == False: 
			DL.SetWindowText("Red", "Tag 9F39: FAIL")
				
		if DL.Check_RXResponse(rx, "FFEE01 ** DFEE300100") == False: 
			DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
		if DL.Check_RXResponse(rx, "DFEE26 02 E100") == False: 
			DL.SetWindowText("Red", "Tag DFEE26: FAIL")