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

# Enable encryption (02)
if (Result):
	RetOfStep = DL.SendCommand('Enable Encryption (02)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 00")

# Encryption Type -- AES
if (Result):
	RetOfStep = DL.SendCommand('Encryption Type -- AES')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 01")

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
        Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** 73 DF EE 12")
        if (Result):
            alldata = DL.Get_RXResponse(0)
            ksn = DL.GetTLV(alldata,"DFEE12")	
            
            encDF812A = DL.GetTLV_Embedded(alldata,"DF812A", 0)
            decDF812A = DL.DecryptDLL(0,2, strKey, ksn, encDF812A)
            encDF812B = DL.GetTLV_Embedded(alldata,"DF812B", 0)
            decDF812B = DL.DecryptDLL(0,2, strKey, ksn, encDF812B)		
            
            mask56 = DL.GetTLV_Embedded(alldata,"56", 0)
            enc56 = DL.GetTLV_Embedded(alldata,"56", 1)
            dec56 = DL.DecryptDLL(0,2, strKey, ksn, enc56)	
            mask9F6B = DL.GetTLV_Embedded(alldata,"9F6B", 0)
            enc9F6B = DL.GetTLV_Embedded(alldata,"9F6B", 1)
            dec9F6B = DL.DecryptDLL(0,2, strKey, ksn, enc9F6B)	
            
            Tag9F39 = DL.GetTLV(alldata,"9F39")
            TagFFEE01 = DL.GetTLV(alldata,"FFEE01")
            TagDFEE26 = DL.GetTLV(alldata,"DFEE26")
                
        # Tag DF812A/ DF812B (only need enc data)
            Result = DL.Check_StringAB(decDF812A, 'DF 81 2A 18 30 30 30 31 30 30 30 30 30 31 30 30 31 31 31 31 31 31 31 31 31 31 31 32')
            if Result == True and DL.Check_RXResponse("** DF 81 2A C1 **"):
                DL.SetWindowText("blue", "Tag DF812A_Enc: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag DF812A_Enc: FAIL")
                
            Result = DL.Check_StringAB(decDF812B, 'DF 81 2B 07 00 01 00 00 01 00 2F')
            if Result == True and DL.Check_RXResponse("** DF 81 2B C1 **"):
                DL.SetWindowText("blue", "Tag DF812B_Enc: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag DF812B_Enc: FAIL")
        
        # Tag 56
            Result = DL.Check_StringAB(mask56, '2A 35 32 35 36 2A 2A 2A 2A 2A 2A 2A 2A 30 30 30 30 5E 53 75 70 70 6C 69 65 64 2F 4E 6F 74 5E 31 32 31 32 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A 2A')
            if Result == True and DL.Check_RXResponse("** 56 A1 3E **"):
                DL.SetWindowText("blue", "Tag 56_Mask: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag 56_Mask: FAIL")
                
            Result = DL.Check_StringAB(dec56, '56 3E 42 35 32 35 36 38 33 32 30 33 30 30 30 30 30 30 30 5E 53 75 70 70 6C 69 65 64 2F 4E 6F 74 5E 31 32 31 32 35 30 32')
            if Result == True and DL.Check_RXResponse("** 56 C1 **"):
                DL.SetWindowText("blue", "Tag 56_Enc: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag 56_Enc: FAIL")
                
        # Tag 9F6B
            Result = DL.Check_StringAB(mask9F6B, '52 56 CC CC CC CC 00 00 D1 21 2C CC CC CC CC CC CC CC CC')
            if Result == True and DL.Check_RXResponse("** 9F 6B A1 13 **"):
                DL.SetWindowText("blue", "Tag 9F6B_Mask: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag 9F6B_Mask: FAIL")
                
            Result = DL.Check_StringAB(dec9F6B, '9F 6B 13 52 56 83 20 30 00 00 00 D1 21 25 02')
            if Result == True and DL.Check_RXResponse("** 9F 6B C1 **"):
                DL.SetWindowText("blue", "Tag 9F6B_Enc: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag 9F6B_Enc: FAIL")
                
        # Tags 9F39/ FFEE01/ DFEE26
            if Tag9F39 == "91": 
                DL.SetWindowText("blue", "Tag 9F39: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("Red", "Tag 9F39: FAIL")
            
            if (DL.Check_RXResponse("FFEE01 ** DFEE300100")): 
                DL.SetWindowText("blue", "Tag FFEE01: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("Red", "Tag FFEE01: FAIL")
            
            if TagDFEE26 == "7300": 
                DL.SetWindowText("blue", "Tag DFEE26: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("Red", "Tag DFEE26: FAIL")
        else:
            DL.fails=DL.fails+1
else:
    DL.fails=DL.fails+1
            
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )