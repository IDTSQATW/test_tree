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
		Result = DL.Check_RXResponse("C7 00 00 06 00 00 00 00 00 00")	
		
# Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")
		
# set FFFC 02 in G1		
if (Result):
	RetOfStep = DL.SendCommand('set FFFC 02 in G1')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")			

# cmd 02-40, tap card
if (Result):
	RetOfStep = DL.SendCommand('Activate Transaction')
	if (RetOfStep):
		DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 0A")
		alldata = DL.Get_RXResponse(0)
		tagDFEE02 = DL.GetTLV(alldata,"DFEE02")
			
	# Tag FFEE1F
		Result = DL.Check_StringAB(tagDFEE02, 'DF EE 02 04 20 90 00 03')
		if Result == True:
			DL.SetWindowText("blue", "Tag DFEE02: PASS")
		else:
			DL.SetWindowText("red", "Tag DFEE02: FAIL")
			
	# # Tags 9F39/ FFEE01/ DFEE26
		# if DL.Check_RXResponse(1, "9F39 01 91") == False: 
			# DL.SetWindowText("Red", "Tag 9F39: FAIL")
				
		# if DL.Check_RXResponse(1, "FFEE01 ** DFEE300100") == False: 
			# DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
		# if DL.Check_RXResponse(1, "DFEE26 02 F100") == False: 
			# DL.SetWindowText("Red", "Tag DFEE26: FAIL")			
			
if readertype == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")	