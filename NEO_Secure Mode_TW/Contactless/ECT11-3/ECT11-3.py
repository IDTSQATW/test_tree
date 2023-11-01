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

# Check platform
platform = DL.ShowMessageBox("", "Is the project NEOII and upward?", 0)
if platform == 1:
	DL.SetWindowText("Green", "*** The project is NEOII and upward ***")
else:
	DL.SetWindowText("Green", "*** The project is NEOI ***")

# Check project has LCD or not
lcdtype = DL.ShowMessageBox("", "Does the project has LCD?", 0)
if lcdtype == 1:
	DL.SetWindowText("Green", "*** The project has LCD ***")
else:
	DL.SetWindowText("Green", "*** The project has NO LCD ***")
	
# Check reader is VP3350 or not
lcdtype = DL.ShowMessageBox("", "Is this VP3350?", 0)
if lcdtype == 1:
	DL.SetWindowText("Green", "*** This is VP3350 ***")
	RetOfStep = DL.SendCommand('0105 do not use LCD')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")
else:
	DL.SetWindowText("Green", "*** non-VP3350 reader ***")	

# Check data encryption TYPE	
if platform == 1: #NEOII and upward
    if (Result):
        RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
        if (RetOfStep):
            Result = DL.Check_RXResponse("C7 00 00 06 00 00 00 00 00 00")
if platform == 0: #NEOI
    if (Result):
        RetOfStep = DL.SendCommand('0-use TDES to encrypt (C7-32)')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("C7 00 00 00")	
            
# Get Data Encryption (C7-37)
if (Result):
	RetOfStep = DL.SendCommand('Get Data Encryption (C7-37)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 03")
        
# group 80, support MSD only
if platform == 1:
    if (Result):
        RetOfStep = DL.SendCommand('group 80, support MSD only')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("04 00 00 00")		
		
# Auto Poll	
if (Result):
	RetOfStep = DL.SendCommand('Auto Poll')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")
		
# cmd 03-40, tap card
if (Result):
	RetOfStep = DL.SendCommand('Get Transaction Result')
	alldata = DL.Get_RXResponse(1)
	if (RetOfStep):
		if platform == 1: #NEOII and upward
			Result = DL.Check_RXResponse(1, '56 69 56 4F 74 65 63 68 32 00 03 23 ** F1 ** DF EE 12')
			ksn = DL.GetTLV(alldata,"DFEE12")	
		if platform == 0: #NEOI
			Result = DL.Check_RXResponse(1, "56 69 56 4F 74 65 63 68 32 00 03 23 ** D1 ** FFEE12")
			ksn = DL.GetTLV(alldata,"FFEE12")
        
		if (Result):
			tagFF8106 = DL.GetTLV(alldata,"FF8106")
			encDF812A = DL.GetTLV(tagFF8106,"DF812A", 0)
			decDF812A = DL.DecryptDLL(0,1, strKey, ksn, encDF812A)
			encDF812B = DL.GetTLV(tagFF8106,"DF812B", 0)
			decDF812B = DL.DecryptDLL(0,1, strKey, ksn, encDF812B)		
            
			tagFF8105 = DL.GetTLV(alldata,"FF8105")
			mask56 = DL.GetTLV(tagFF8105,"56", 0)
			enc56 = DL.GetTLV(tagFF8105,"56", 1)
			dec56 = DL.DecryptDLL(0,1, strKey, ksn, enc56)	
			mask9F6B = DL.GetTLV(tagFF8105,"9F6B", 0)
			enc9F6B = DL.GetTLV(tagFF8105,"9F6B", 1)
			dec9F6B = DL.DecryptDLL(0,1, strKey, ksn, enc9F6B)	
			
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
			if platform == 0: #NEOI
				Result = DL.Check_RXResponse(1, '56 A1 29 2A 35 31 32 38 2A 2A 2A 2A 2A 2A 2A 2A ** 5E 20 2F 5E 31 38 30 33 363232 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A')
			else: #NEOII and upward
				Result = DL.Check_RXResponse(1, '56 A1 29 2A 35 31 32 38 2A 2A 2A 2A 2A 2A 2A 2A ** 5E 20 2F 5E 31 38 30 33 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A')
			if Result == True:
				DL.SetWindowText("blue", "Tag 56_Mask: PASS")
			else:
				DL.fails=DL.fails+1
				DL.SetWindowText("red", "Tag 56_Mask: FAIL")
                
			Result = DL.Check_StringAB(dec56, '56 29 42 35 31 32 38 35 37 30 31')
			if Result == True:
				Result = DL.Check_StringAB(dec56, '5E 20 2F 5E 31 38 30 33 36 32 32 30 30')
			if Result == True and DL.Check_RXResponse(1, "** 56 C1 **"):
				DL.SetWindowText("blue", "Tag 56_Enc: PASS")
			else:
				DL.fails=DL.fails+1
				DL.SetWindowText("red", "Tag 56_Enc: FAIL")
                
            # Tag 9F6B
			if platform == 0: #NEOI
				Result = DL.Check_RXResponse(1, '9F 6B A1 13 51 28 CC CC CC CC ** D1 80 3 622 CC CC CC CC CC CC CC')
			else: #NEOII and upward
				Result = DL.Check_RXResponse(1, '9F 6B A1 13 51 28 CC CC CC CC ** D1 80 3C CC CC CC CC CC CC CC CC')
			if Result == True:
				DL.SetWindowText("blue", "Tag 9F6B_Mask: PASS")
			else:
				DL.fails=DL.fails+1
				DL.SetWindowText("red", "Tag 9F6B_Mask: FAIL")
                
			Result = DL.Check_StringAB(dec9F6B, '9F 6B 13 51 28 57 01')
			if Result == True:
				Result = DL.Check_StringAB(dec9F6B, 'D1 80 36 22 00')
			if Result == True and DL.Check_RXResponse(1, "** 9F 6B C1 **"):
				DL.SetWindowText("blue", "Tag 9F6B_Enc: PASS")
			else:
				DL.fails=DL.fails+1
				DL.SetWindowText("red", "Tag 9F6B_Enc: FAIL")
			
            # Tags 9F39/ FFEE01/ DFEE26
			if DL.Check_RXResponse(1, "9F39 01 91") == False: 
				DL.fails=DL.fails+1
				DL.SetWindowText("Red", "Tag 9F39: FAIL")

			if platform == 1: #NEOII and upward
				Result = DL.Check_RXResponse(1, "FFEE01 ** DFEE300100")
			if platform == 0: #NEOI
				Result = DL.Check_RXResponse(1, "FFEE01 ** DF300100")
			if Result == False:
				DL.fails=DL.fails+1
				DL.SetWindowText("Red", "Tag DF**30: FAIL")			
                
			if platform == 1: #NEOII and upward
				Result = DL.Check_RXResponse(1, "DFEE26 02 F100")
			if platform == 0: #NEOI
				Result = DL.Check_RXResponse(1, "DFEE26 01 D1")
			if Result == False:
				DL.fails=DL.fails+1
				DL.SetWindowText("Red", "Tag DFEE26: FAIL")			
		else:
			DL.fails=DL.fails+1
else:
	DL.fails=DL.fails+1
			
if lcdtype == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")	
        
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )