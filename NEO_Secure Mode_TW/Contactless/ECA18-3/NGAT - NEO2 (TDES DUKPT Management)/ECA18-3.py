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

# Check reader is VP3350 or not
readertype = DL.ShowMessageBox("", "Is this VP3350?", 0)
if readertype == 1:
	DL.SetWindowText("Green", "*** This is VP3350 ***")
	RetOfStep = DL.SendCommand('0105 do not use LCD')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")
else:
	DL.SetWindowText("Green", "*** non-VP3350 reader ***")	

# Check data encryption TYPE is TDES	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("C7 00 00 06 00 01 00 00 00 00")		
		
# Burst mode OFF
if (Result):
	RetOfStep = DL.SendCommand('Burst mode Off')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	

# cmd 02-40/ 03-40, tap card
if (Result):
	for i in range(1, 3):
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
					rx = 0
					DL.Check_RXResponse(rx, '56 69 56 4F 74 65 63 68 32 00 02 23 ** E3 ** DF EE 12')
				if i == 2:
					rx = 1
					DL.Check_RXResponse(rx, '56 69 56 4F 74 65 63 68 32 00 03 23 ** E3 ** DF EE 12')
				alldata = DL.Get_RXResponse(rx)
				ksn = DL.GetTLV(alldata,"DFEE12")	
				
				mask57 = DL.GetTLV_Embedded(alldata,"57", 0)
				enc57 = DL.GetTLV_Embedded(alldata,"57", 1)
				dec57 = DL.DecryptDLL(0,2, strKey, ksn, enc57)	
				mask5A = DL.GetTLV_Embedded(alldata,"5A", 0)
				enc5A = DL.GetTLV_Embedded(alldata,"5A", 1)
				dec5A = DL.DecryptDLL(0,2, strKey, ksn, enc5A)
								
			# Tag 57
				Result = DL.Check_StringAB(mask57, '54 13 CC CC CC CC 15 13 D0 51 2C CC CC CC CC CC CC')
				if Result == True and DL.Check_StringAB(alldata, "57 A1 11"):
					DL.SetWindowText("blue", "Tag 57_Mask: PASS")
				else:
					DL.SetWindowText("red", "Tag 57_Mask: FAIL")
					
				Result = DL.Check_StringAB(dec57, '57 11 54 13 33 90 00 00 15 13 D0 51 22 20 01 23 45 67 89')
				if Result == True and DL.Check_StringAB(alldata, "57 C1 20"):
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
				if DL.Check_RXResponse(rx, "9F39 01 07") == False: 
					DL.SetWindowText("Red", "Tag 9F39: FAIL")
				if DL.Check_RXResponse(rx, "FFEE01 ** DFEE300100") == False: 
					DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				if DL.Check_RXResponse(rx, "DFEE26 02 E300") == False: 
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")		
				
				RetOfStep = DL.SendCommand('03-03')
				time.sleep(2)
				
if readertype == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")						