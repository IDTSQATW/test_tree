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
lcdtype = DL.ShowMessageBox("", "Is this VP3350?", 0)
if lcdtype == 1:
	DL.SetWindowText("Green", "*** This is VP3350 ***")
	RetOfStep = DL.SendCommand('0105 do not use LCD')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")
else:
	DL.SetWindowText("Green", "*** non-VP3350 reader ***")

if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 06 00 00 00 00 00 00")	
		
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
				DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** E1 ** DF EE 12")
				alldata = DL.Get_RXResponse(0)
				ksn = DL.GetTLV(alldata,"DFEE12")	
				
				mask57 = DL.GetTLV_Embedded(alldata,"57", 0)
				enc57 = DL.GetTLV_Embedded(alldata,"57", 1)
				dec57 = DL.DecryptDLL(0,1, strKey, ksn, enc57)	
				
			# Tag 57
				if DL.Check_RXResponse("57 A1 13"):
					DL.SetWindowText("blue", "Tag 57_Mask: PASS")
				else:
					DL.SetWindowText("red", "Tag 57_Mask: FAIL")
					
				Result = DL.Check_StringAB(dec57, '5713')
				if Result == True and DL.Check_RXResponse("57 C1"):
					DL.SetWindowText("blue", "Tag 57_Enc: PASS")
				else:
					DL.SetWindowText("red", "Tag 57_Enc: FAIL")
					
			# Tags 9F39/ FFEE01/ DFEE26
				if DL.Check_RXResponse('9F39 01 07'): 
					DL.SetWindowText("blue", "Tag 9F39: PASS")
				else:
					DL.SetWindowText("Red", "Tag 9F39: FAIL")
				
				# if DL.Check_RXResponse('FFEE01 ** DFEE300100'): 
					# DL.SetWindowText("blue", "Tag FFEE01: PASS")
				# else:
					# DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
				if DL.Check_RXResponse('DFEE26 02 E100'): 
					DL.SetWindowText("blue", "Tag DFEE26: PASS")
				else:
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")
			
	# Auto Poll
	time.sleep(1)
	RetOfStep = DL.SendCommand('Auto Poll')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")
	
	# cmd 03-40
		if (Result):
			RetOfStep = DL.SendCommand('Get Transaction result')
			if (RetOfStep):
				alldata = DL.Get_RXResponse(1)
				DL.Check_RXResponse(1, '56 69 56 4F 74 65 63 68 32 00 03 23 ** E1 ** DF EE 12')
				ksn = DL.GetTLV(alldata,"DFEE12")	
					
				mask57 = DL.GetTLV_Embedded(alldata,"57", 0)
				enc57 = DL.GetTLV_Embedded(alldata,"57", 1)
				dec57 = DL.DecryptDLL(0,1, strKey, ksn, enc57)	
				
			# Tag 57
				if DL.Check_StringAB(alldata, "57 A1 13"):
					DL.SetWindowText("blue", "Tag 57_Mask: PASS")
				else:
					DL.SetWindowText("red", "Tag 57_Mask: FAIL")
					
				Result = DL.Check_StringAB(dec57, '5713')
				if Result == True and DL.Check_StringAB(alldata, "57 C1"):
					DL.SetWindowText("blue", "Tag 57_Enc: PASS")
				else:
					DL.SetWindowText("red", "Tag 57_Enc: FAIL")
		
			# Tags 9F39/ FFEE01/ DFEE26
				if DL.Check_RXResponse(1, '9F39 01 07'): 
					DL.SetWindowText("blue", "Tag 9F39: PASS")
				else:
					DL.SetWindowText("Red", "Tag 9F39: FAIL")
				
				# if DL.Check_RXResponse('FFEE01 ** DFEE300100'): 
					# DL.SetWindowText("blue", "Tag FFEE01: PASS")
				# else:
					# DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
				if DL.Check_RXResponse(1, 'DFEE26 02 E100'): 
					DL.SetWindowText("blue", "Tag DFEE26: PASS")
				else:
					DL.SetWindowText("Red", "Tag DFEE26: FAIL")
					
if lcdtype == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")	