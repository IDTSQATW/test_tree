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

# Enable encryption (02)
if (Result):
	RetOfStep = DL.SendCommand('Enable Encryption (02)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 00")

# Encryption Type -- TransArmor TDES
if (Result):
	RetOfStep = DL.SendCommand('C7-A2 TDES DUKPT manage_TransArmor TDES, data key')
	time.sleep(1)
	
# Check data encryption TYPE is TDES	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 06 00 02 00 00 00 00")	
		
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
		DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** A5")
		
		alldata = DL.Get_RXResponse(0)	
		Tag57 = DL.GetTLV(alldata,"57", 0)
		Tag5A = DL.GetTLV(alldata,"5A", 0)
	
		alldata = DL.GetTLV(alldata,"FF8105")	
		Tag57 = DL.GetTLV(alldata,"57", 0)
		Tag5A = DL.GetTLV(alldata,"5A", 0)
		
	# Tag 57
		Result = DL.Check_RXResponse('57 13 47 61 73 90 01 01 00 10 D3 01 21 20 00 12 33 99 00 03 1F')
		if Result == True:
			DL.SetWindowText("blue", "Tag 57_Mask: PASS")
		else:
			DL.SetWindowText("red", "Tag 57_Mask: FAIL")

	# Tag 5A
		Result = DL.Check_RXResponse('5A 08 47 61 73 90 01 01 00 10')
		if Result == True:
			DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
		else:
			DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
						
	# Tags 9F39/ FFEE01/ DFEE26
		if DL.Check_RXResponse("9F39 01 07"): 
			DL.SetWindowText("blue", "Tag 9F39 = 07: PASS")
		else:
			DL.SetWindowText("Red", "Tag 9F39: FAIL")
		
		if DL.Check_RXResponse("FFEE01 ** DFEE300100"): 
			DL.SetWindowText("blue", "Tag FFEE01: PASS")
		else:
			DL.SetWindowText("Red", "Tag FFEE01: FAIL")
		
		if DL.Check_RXResponse("DFEE26 02 A506"): 
			DL.SetWindowText("blue", "Tag DFEE26: PASS")
		else:
			DL.SetWindowText("Red", "Tag DFEE26: FAIL")				
			
if readertype == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")			