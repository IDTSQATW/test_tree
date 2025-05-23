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

# Get Data Encryption (C7-37)
if (Result):
	RetOfStep = DL.SendCommand('Get Data Encryption (C7-37)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 02")
        
# Check data encryption TYPE is AES	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 06 01 02 00 00 00 00")

# group 80, support MSD only
if (Result):
	RetOfStep = DL.SendCommand('group 80, support MSD only')
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
        Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** 75 ** DF EE 12")
        if (Result):
            alldata = DL.Get_RXResponse(0)
            ksn = DL.GetTLV(alldata,"DFEE12")	
            
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
                
        # Tag DF812A/ DF812B (only need enc data)
            Result = DL.Check_StringAB(decDF812A, 'DF 81 2A 0D 30 30 30 30 30 30 30 30 30 30 30 30 30')
            if Result == True and DL.Check_RXResponse("** DF 81 2A C1 **"):
                DL.SetWindowText("blue", "Tag DF812A_Enc: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag DF812A_Enc: FAIL")
                
            Result = DL.Check_StringAB(decDF812B, 'DF 81 2B 07 00 00 00 00 00 00 0F')
            if Result == True and DL.Check_RXResponse("** DF 81 2B C1 **"):
                DL.SetWindowText("blue", "Tag DF812B_Enc: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag DF812B_Enc: FAIL")
        
        # Tag 56
            r1 = DL.Check_StringAB(mask56, '2A 35 31 32 38 2A 2A 2A 2A 2A 2A 2A 2A ')
            r2 = DL.Check_StringAB(mask56, '5E 20 2F 5E 31 38 30 33 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A')
            if r1 == True and r2 == True and DL.Check_RXResponse("** 56 A1 29 **"):
                DL.SetWindowText("blue", "Tag 56_Mask: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag 56_Mask: FAIL")
                
            r1 = DL.Check_StringAB(dec56, '56 29 42 35 31 32 38 35 37 30 31 30 30 30 33')
            r2 = DL.Check_StringAB(dec56, '5E 20 2F 5E 31 38 30 33 36 32 32')
            if r1 == True and r2 == True and DL.Check_RXResponse("** 56 C1 **"):
                DL.SetWindowText("blue", "Tag 56_Enc: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag 56_Enc: FAIL")
                
        # Tag 9F6B
            r1 = DL.Check_StringAB(mask9F6B, '51 28 CC CC CC CC')
            r2 = DL.Check_StringAB(mask9F6B, 'D1 80 3C CC CC CC CC CC CC CC CC')
            if r1 == True and r2 == True and DL.Check_RXResponse("** 9F 6B A1 13 **"):
                DL.SetWindowText("blue", "Tag 9F6B_Mask: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag 9F6B_Mask: FAIL")
                
            r1 = DL.Check_StringAB(dec9F6B, '9F 6B 13 51 28 57 01 00 03')
            r2 = DL.Check_StringAB(dec9F6B, 'D1 80 36 22')
            if r1 == True and r2 == True and DL.Check_RXResponse("** 9F 6B C1 **"):
                DL.SetWindowText("blue", "Tag 9F6B_Enc: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag 9F6B_Enc: FAIL")
                
        # Tags 9F39/ FFEE01/ DFEE26
            if DL.Check_RXResponse("9F39 01 91"): 
                DL.SetWindowText("blue", "Tag 9F39: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("Red", "Tag 9F39: FAIL")
            
            if DL.Check_RXResponse("FFEE01 ** DFEE300100"): 
                DL.SetWindowText("blue", "Tag FFEE01: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("Red", "Tag FFEE01: FAIL")
            
            if DL.Check_RXResponse("DFEE26 02 7501"): 
                DL.SetWindowText("blue", "Tag DFEE26: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("Red", "Tag DFEE26: FAIL")			
        else:
            DL.fails=DL.fails+1
else:
    DL.fails=DL.fails+1

if readertype == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")			
        
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )