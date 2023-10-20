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
        
# Check data encryption TYPE is AES	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 06 01 02 00 00 00 00")

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
		DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** 65")
		alldata = DL.Get_RXResponse(0)

		mask5A = DL.GetTLV_Embedded(alldata,"5A", 0)
		mask57 = DL.GetTLV_Embedded(alldata,"57", 0)

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
		if DL.Check_RXResponse("9F39 01 07") == False: 
			DL.SetWindowText("Red", "Tag 9F39: FAIL")
		if DL.Check_RXResponse("DFEE26 02 6501") == False: 
			DL.SetWindowText("Red", "Tag DFEE26: FAIL")			
			
if readertype == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")			