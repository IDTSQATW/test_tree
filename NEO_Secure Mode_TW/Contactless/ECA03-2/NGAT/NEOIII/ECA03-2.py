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

# Set group 80 (MSD only)
if (Result):
	RetOfStep = DL.SendCommand('Set group 80 (MSD only)')
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
		DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** 73 ** DF EE 12")
		alldata = DL.Get_RXResponse(0)
		ksn = DL.GetTLV(alldata,"DFEE12")	
		
		maskDFEF17 = DL.GetTLV(alldata,"DFEF17", 0)
		encDFEF17 = DL.GetTLV(alldata,"DFEF17", 1)
		decDFEF17 = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, encDFEF17)
		
		maskDFEF18 = DL.GetTLV(alldata,"DFEF18", 0)
		encDFEF18 = DL.GetTLV(alldata,"DFEF18", 1)
		decDFEF18 = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, encDFEF18)
		
		tagFF8106 = DL.GetTLV(alldata,"FF8106")
		encDF812A = DL.GetTLV(tagFF8106,"DF812A", 0)
		decDF812A = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, encDF812A)
        
		encDF812B = DL.GetTLV(tagFF8106,"DF812B", 0)
		decDF812B = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, encDF812B)	
		
		tagFF8105 = DL.GetTLV(alldata,"FF8105")
		mask56 = DL.GetTLV(tagFF8105,"56", 0)
		enc56 = DL.GetTLV(tagFF8105,"56", 1)
		dec56 = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc56)	
		mask9F6B = DL.GetTLV(tagFF8105,"9F6B", 0)
		enc9F6B = DL.GetTLV(tagFF8105,"9F6B", 1)
		dec9F6B = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc9F6B)	
		
	# Tag DFEF17
		Result = DL.Check_StringAB(maskDFEF17, '2A 35 32 35 36 2A 2A 2A 2A 2A 2A 2A 2A 30 30 30 30 5E 53 75 70 70 6C 69 65 64 2F 4E 6F 74 5E 31 32 31 32 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A')
		if Result == True and DL.Check_RXResponse("** DF EF 17 A1 3E **"):
			DL.SetWindowText("blue", "Tag DFEF17_Mask: PASS")
		else:
			DL.SetWindowText("red", "Tag DFEF17_Mask: FAIL")
			
		Result = DL.Check_StringAB(decDFEF17, 'DF EF 17 3E 42 35 32 35 36 38 33 32 30 33 30 30 30 30 30 30 30 5E 53 75 70 70 6C 69 65 64 2F 4E 6F 74 5E 31 32 31 32 35 30 32')
		if Result == True and DL.Check_RXResponse("** DF EF 17 C1 **"):
			DL.SetWindowText("blue", "Tag DFEF17_Enc: PASS")
		else:
			DL.SetWindowText("red", "Tag DFEF17_Enc: FAIL")

	# Tag DFEF18
		Result = DL.Check_StringAB(maskDFEF18, '35 32 35 36 2A 2A 2A 2A 2A 2A 2A 2A 30 30 30 30 3D 31 32 31 32 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A')
		if Result == True and DL.Check_RXResponse("** DF EF 18 A1 25 **"):
			DL.SetWindowText("blue", "Tag DFEF18_Mask: PASS")
		else:
			DL.SetWindowText("red", "Tag DFEF18_Mask: FAIL")
			
		Result = DL.Check_StringAB(decDFEF18, 'DF EF 18 25 35 32 35 36 38 33 32 30 33 30 30 30 30 30 30 30 3D 31 32 31 32 35 30 32')
		if Result == True and DL.Check_RXResponse("** DF EF 18 C1 **"):
			DL.SetWindowText("blue", "Tag DFEF18_Enc: PASS")
		else:
			DL.SetWindowText("red", "Tag DFEF18_Enc: FAIL")
			
	# Tag DF812A/ DF812B (only need enc data)
		Result = DL.Check_StringAB(decDF812A, 'DF 81 2A 18 30 30 30 31 30 30 30 30 30 31 30 30 31 31 31 31 31 31 31 31 31 31 31 32')
		if Result == True and DL.Check_RXResponse("** DF 81 2A C1 **"):
			DL.SetWindowText("blue", "Tag DF812A_Enc: PASS")
		else:
			DL.SetWindowText("red", "Tag DF812A_Enc: FAIL")
			
		Result = DL.Check_StringAB(decDF812B, 'DF 81 2B 07 00 01 00 00 01 00 2F')
		if Result == True and DL.Check_RXResponse("** DF 81 2B C1 **"):
			DL.SetWindowText("blue", "Tag DF812B_Enc: PASS")
		else:
			DL.SetWindowText("red", "Tag DF812B_Enc: FAIL")
	
	# Tag 56
		Result = DL.Check_StringAB(mask56, '2A 35 32 35 36 2A 2A 2A 2A 2A 2A 2A 2A 30 30 30 30 5E 53 75 70 70 6C 69 65 64 2F 4E 6F 74 5E 31 32 31 32 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A')
		if Result == True and DL.Check_RXResponse("** 56 A1 3E **"):
			DL.SetWindowText("blue", "Tag 56_Mask: PASS")
		else:
			DL.SetWindowText("red", "Tag 56_Mask: FAIL")
			
		Result = DL.Check_StringAB(dec56, '56 3E 42 35 32 35 36 38 33 32 30 33 30 30 30 30 30 30 30 5E 53 75 70 70 6C 69 65 64 2F 4E 6F 74 5E 31 32 31 32 35 30 32')
		if Result == True and DL.Check_RXResponse("** 56 C1 **"):
			DL.SetWindowText("blue", "Tag 56_Enc: PASS")
		else:
			DL.SetWindowText("red", "Tag 56_Enc: FAIL")
			
	# Tag 9F6B
		Result = DL.Check_StringAB(mask9F6B, '52 56 CC CC CC CC 00 00 D1 21 2C CC CC CC CC CC CC CC CC')
		if Result == True and DL.Check_RXResponse("** 9F 6B A1 13 **"):
			DL.SetWindowText("blue", "Tag 9F6B_Mask: PASS")
		else:
			DL.SetWindowText("red", "Tag 9F6B_Mask: FAIL")
			
		Result = DL.Check_StringAB(dec9F6B, '9F 6B 13 52 56 83 20 30 00 00 00 D1 21 25 02')
		if Result == True and DL.Check_RXResponse("** 9F 6B C1 **"):
			DL.SetWindowText("blue", "Tag 9F6B_Enc: PASS")
		else:
			DL.SetWindowText("red", "Tag 9F6B_Enc: FAIL")
			
	# Tags 9F39/ FFEE01/ DFEE26
		if DL.Check_RXResponse("9F39 01 91"): 
			DL.SetWindowText("blue", "Tag 9F39: PASS")
		else:
			DL.SetWindowText("Red", "Tag 9F39: FAIL")
		
		if DL.Check_RXResponse("FFEE01 ** DFEE300100"): 
			DL.SetWindowText("blue", "Tag FFEE01: PASS")
		else:
			DL.SetWindowText("Red", "Tag FFEE01: FAIL")
		
		if DL.Check_RXResponse("DFEE26 02 7301"): 
			DL.SetWindowText("blue", "Tag DFEE26: PASS")
		else:
			DL.SetWindowText("Red", "Tag DFEE26: FAIL")
			
if readertype == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")					