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

# Get Data Encryption (C7-37)
if (Result):
	RetOfStep = DL.SendCommand('Get Data Encryption (C7-37)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 03")			
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
    for i in range(1, 3):
        if i == 1:
            RetOfStep = DL.SendCommand('02-40 #9987 VAS_AND_PAY')
        if i == 2:
            time.sleep(1)
            RetOfStep = DL.SendCommand('02-40 #9987 VAS_OR_PAY')	
            
        if (RetOfStep):
            Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** DFEE12 0A")
            alldata = DL.Get_RXResponse(0)
            TagFF8105 = DL.GetTLV(alldata,"FF8105")
            ksn = DL.GetTLV(alldata,"DFEE12")	
            
            mask57 = DL.GetTLV(TagFF8105,"57", 0)
            enc57 = DL.GetTLV(TagFF8105,"57", 1)
            dec57 = DL.DecryptDLL(0,1, strKey, ksn, enc57)	
            
            mask5A = DL.GetTLV(TagFF8105,"5A", 0)
            enc5A = DL.GetTLV(TagFF8105,"5A", 1)
            dec5A = DL.DecryptDLL(0,1, strKey, ksn, enc5A)	
            
            if (Result):
                # Tag 57
                Result = DL.Check_RXResponse('57 A1 13 47 61 CC CC CC CC 00 10 D3 01 2C CC CC CC CC CC CC CC CC')
                if Result == True:
                    DL.SetWindowText("blue", "Tag 57_Mask: PASS")
                else:
                    DL.SetWindowText("red", "Tag 57_Mask: FAIL")
                    DL.fails=DL.fails+1
                    
                Result = DL.Check_StringAB(dec57, '57 13 47 61 73 90 01 01 00 10 D3 01 21 20 00 12 33 99 00 03 1F')
                if Result == True and DL.Check_RXResponse("57 C1"):
                    DL.SetWindowText("blue", "Tag 57_Enc: PASS")
                else:
                    DL.SetWindowText("red", "Tag 57_Enc: FAIL")
                    DL.fails=DL.fails+1

                # Tag 5A
                Result = DL.Check_RXResponse('5A A1 08 47 61 CC CC CC CC 00 10')
                if Result == True:
                    DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
                else:
                    DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
                    DL.fails=DL.fails+1
                    
                Result = DL.Check_StringAB(dec5A, '5A 08 47 61 73 90 01 01 00 10')
                if Result == True and DL.Check_RXResponse("5A C1"):
                    DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
                else:
                    DL.SetWindowText("red", "Tag 5A_Enc: FAIL")	
                    DL.fails=DL.fails+1
                    
                # Tags 9F39/ FFEE01/ DFEE26/ DFEF7B
                if (DL.Check_RXResponse("9F 39 01 07")): 
                    DL.SetWindowText("blue", "Tag 9F39: PASS")
                else:
                    DL.SetWindowText("Red", "Tag 9F39: FAIL")
                    DL.fails=DL.fails+1
                
                if DL.Check_RXResponse("DF EE 26 02 **"): 
                    DL.SetWindowText("blue", "Tag DFEE26: PASS")
                else:
                    DL.SetWindowText("Red", "Tag DFEE26: FAIL")
                    DL.fails=DL.fails+1
                    
                if (DL.Check_RXResponse("DF EF 7B 01 00")): 
                    DL.SetWindowText("blue", "Tag DFEF7B: PASS")
                else:
                    DL.SetWindowText("Red", "Tag DFEF7B: FAIL")
                    DL.fails=DL.fails+1
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