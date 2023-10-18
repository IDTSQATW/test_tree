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
		Result = DL.Check_RXResponse("C7 00 00 06 00 01 00 00 00 00")		

# Set group 80 -- DF 81 1B = 40
if (Result):
	RetOfStep = DL.SendCommand('Set group 80 -- DF 81 1B = 40')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")
		
# Auto Poll	
if (Result):
	RetOfStep = DL.SendCommand('Auto Poll')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")

# tap card, cmd 03-40 
if (Result):
	RetOfStep = DL.SendCommand('Get Transaction Result')
	if (RetOfStep):
		alldata = DL.Get_RXResponse(1)
		DL.Check_RXResponse(1, '56 69 56 4F 74 65 63 68 32 00 03 23')
		DL.Check_RXResponse(1, 'F3 ** DF EE 12')
		ksn = DL.GetTLV(alldata,"DFEE12")	
		
		tagFF8106 = DL.GetTLV(alldata,"FF8106")
		encDF812A = DL.GetTLV(tagFF8106,"DF812A", 0)
		decDF812A = DL.DecryptDLL(0,2, strKey, ksn, encDF812A)
		encDF812B = DL.GetTLV(tagFF8106,"DF812B", 0)
		decDF812B = DL.DecryptDLL(0,2, strKey, ksn, encDF812B)		
		
		tagFF8105 = DL.GetTLV(alldata,"FF8105")
		mask56 = DL.GetTLV(tagFF8105,"56", 0)
		enc56 = DL.GetTLV(tagFF8105,"56", 1)
		dec56 = DL.DecryptDLL(0,2, strKey, ksn, enc56)	
		mask9F6B = DL.GetTLV(tagFF8105,"9F6B", 0)
		enc9F6B = DL.GetTLV(tagFF8105,"9F6B", 1)
		dec9F6B = DL.DecryptDLL(0,2, strKey, ksn, enc9F6B)	
			
	# Tag DF812A/ DF812B (only need enc data)
		Result = DL.Check_StringAB(decDF812A, 'DF 81 2A 0D 30 30 30 30 30 30 30 30 30 30 30 30 30')
		if Result == True and DL.Check_StringAB(alldata, "DF 81 2A C1"):
			DL.SetWindowText("blue", "Tag DF812A_Enc: PASS")
		else:
			DL.SetWindowText("red", "Tag DF812A_Enc: FAIL")
			
		Result = DL.Check_StringAB(decDF812B, 'DF 81 2B 07 00 00 00 00 00 00 0F')
		if Result == True and DL.Check_StringAB(alldata, "DF 81 2B C1"):
			DL.SetWindowText("blue", "Tag DF812B_Enc: PASS")
		else:
			DL.SetWindowText("red", "Tag DF812B_Enc: FAIL")
			
	# Tag 56
		R1 = DL.Check_StringAB(mask56, '2A353132382A2A2A2A2A2A2A2A')
		R2 = DL.Check_StringAB(mask56, '5E202F5E313830332A2A2A2A2A2A2A2A2A2A2A2A2A2A2A2A')	
		if R1 == True and R2 == True and DL.Check_StringAB(alldata, "56 A1 29"):
			DL.SetWindowText("blue", "Tag 56_Mask: PASS")
		else:
			DL.SetWindowText("red", "Tag 56_Mask: FAIL")
			
		R1 = DL.Check_StringAB(dec56, '562942353132383537303130303033')
		R2 = DL.Check_StringAB(dec56, '5E202F5E31383033363232')
		if R1 == True and R2 == True and DL.Check_StringAB(alldata, "56 C1"):
			DL.SetWindowText("blue", "Tag 56_Enc: PASS")
		else:
			DL.SetWindowText("red", "Tag 56_Enc: FAIL")
			
	# Tag 9F6B
		R1 = DL.Check_StringAB(mask9F6B, '51 28 CC CC CC CC')
		R2 = DL.Check_StringAB(mask9F6B, 'D1 80 3C CC CC CC CC CC CC CC CC')
		if R1 == True and R2 == True and DL.Check_StringAB(alldata, "9F 6B A1 13"):
			DL.SetWindowText("blue", "Tag 9F6B_Mask: PASS")
		else:
			DL.SetWindowText("red", "Tag 9F6B_Mask: FAIL")
			
		R1 = DL.Check_StringAB(dec9F6B, '9F 6B 13 51 28 57 01 00 03 ')
		R2 = DL.Check_StringAB(dec9F6B, 'D1 80 36 22')
		if R1 == True and R2 == True and DL.Check_StringAB(alldata, "9F 6B C1"):
			DL.SetWindowText("blue", "Tag 9F6B_Enc: PASS")
		else:
			DL.SetWindowText("red", "Tag 9F6B_Enc: FAIL")
			
	# Tags 9F39/ FFEE01/ DFEE26			
		if DL.Check_RXResponse(1, "9F39 01 91") == False: 
			DL.SetWindowText("Red", "Tag 9F39: FAIL")
				
		if DL.Check_RXResponse(1, "FFEE01 ** DFEE300100") == False: 
			DL.SetWindowText("Red", "Tag FFEE01: FAIL")
				
		if DL.Check_RXResponse(1, "DFEE26 02 F300") == False: 
			DL.SetWindowText("Red", "Tag DFEE26: FAIL")			
			
# Reset to default
RetOfStep = DL.SendCommand('Reset to default')
if (RetOfStep):
	DL.Check_RXResponse("04 00 00 00")	
	
if readertype == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")			