#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True
Result2= True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''
strKey = '0123456789ABCDEFFEDCBA9876543210'

# Check reader is VP3350 or not
readermodel = DL.ShowMessageBox("", "Is this VP3350?", 0)
if readermodel == 1:
	DL.SetWindowText("Green", "*** This is VP3350 ***")
	RetOfStep = DL.SendCommand('0105 do not use LCD')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")
	readertype = DL.ShowMessageBox("", "Is this NSRED project?", 0)
else:
	DL.SetWindowText("Green", "*** non-VP3350 reader ***")	

if readertype == 1:
    # Check data encryption TYPE is TDES	
    if (Result):
        RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("C7 00 00 06 00 00 00 00 00 00")

    # Enable encryption (03)
    if (Result):
        RetOfStep = DL.SendCommand('Enable Encryption (03)')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("C7 00 00 00")
            
    # Poll on demand
    if (Result):
        RetOfStep = DL.SendCommand('Poll on Demand')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("01 00 00 00")

    # cmd 02-40, tap card
    if (Result):
        for i in range(1, 4):
            if i == 1 or i == 3:
                RetOfStep = DL.SendCommand('DFEC4A--06 04 2A 0C 31')
            if i == 2:
                RetOfStep = DL.SendCommand('DFEE1D--06 04 2A 0C 31')
            if (RetOfStep):
                Result = Result and DL.Check_RXResponse("C7 00 00 00")	

            if (Result):
                time.sleep(1)
                if i <= 2:
                    RetOfStep = DL.SendCommand('Activate Transaction-D')
                if i == 3:
                    RetOfStep = DL.SendCommand('Activate Transaction-V')
                if (RetOfStep):
                    Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** E1 ** DF EE 12")
                    if (Result):
                        alldata = DL.Get_RXResponse(0)
                        ksn = DL.GetTLV(alldata,"DFEE12")	
                
                        mask57 = DL.GetTLV_Embedded (alldata,"57", 0)
                        enc57 = DL.GetTLV_Embedded (alldata,"57", 1)
                        dec57 = DL.DecryptDLL(0,1, strKey, ksn, enc57)	
                        
                        mask5A = DL.GetTLV_Embedded (alldata,"5A", 0)
                        enc5A = DL.GetTLV_Embedded (alldata,"5A", 1)
                        dec5A = DL.DecryptDLL(0,1, strKey, ksn, enc5A)	
                    
                        # Tag 57
                        if i == 1:
                            Result = DL.Check_RXResponse('36 07 05 CC CC C0 00 1D 49 12 CC CC CC CC CC CC CC CC')
                        if i == 2:
                            Result = DL.Check_RXResponse('36 07 0C CC CC C0 00 1D 49 12 CC CC CC CC CC CC CC CC')
                        if i == 3:
                            Result = DL.Check_RXResponse('47 61 73 CC CC 01 00 D2 01 2C CC CC CC CC CC CC CC CC')
                            
                        if Result == True and DL.Check_RXResponse("57 A1 12"):
                            DL.SetWindowText("blue", "Tag 57_Mask: PASS")
                        else:
                            DL.SetWindowText("red", "Tag 57_Mask: FAIL")
                            DL.fails=DL.fails+1
                                
                        if i <= 2:
                            r1 = DL.Check_StringAB(dec57, '57 12 36 07 05 00 00 00 00 1D 49 12 10 10 00 03 32 11 23 01 00 00 00 00 00 00 00 00 00 00 00 00')
                        if i == 3:
                            r1 = DL.Check_StringAB(dec57, '57 12 47 61 73 90 01 01 00 D2 01 21 20 00 12 33 99 00 03 1F 00 00 00 00')
                        if r1 == True and DL.Check_RXResponse("57 C1 18"):
                            DL.SetWindowText("blue", "Tag 57_Enc: PASS")
                        else:
                            DL.SetWindowText("red", "Tag 57_Enc: FAIL")
                            DL.fails=DL.fails+1
                            
                        # Tag 5A
                        if i == 1:
                            Result = DL.Check_RXResponse('36 07 05 CC CC C0 00 1F')
                        if i == 2:
                            Result = DL.Check_RXResponse('36 07 0C CC CC C0 00 1F')
                        if i == 3:
                            Result = DL.Check_RXResponse('47 61 73 CC CC 01 00')
                            
                        if i <= 2:
                            if Result == True and Result2 == DL.Check_RXResponse("5A A1 08"):
                                DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
                        if i == 3:
                            if Result == True and Result2 == DL.Check_RXResponse("5A A1 07"):
                                DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
                        if Result == False or Result2 == False:
                            DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
                            DL.fails=DL.fails+1
                                
                        if i <= 2:
                            r1 = DL.Check_StringAB(dec5A, '5A 08 36 07 05 00 00 00 00 1F')
                        if i == 3:
                            r1 = DL.Check_StringAB(dec5A, '5A 07 47 61 73 90 01 01 00 00 00 00 00 00 00 00')
                        if r1 == True and DL.Check_RXResponse("5A C1 10"):
                            DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
                        else:
                            DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
                            DL.fails=DL.fails+1
                    else:
                        DL.fails=DL.fails+1
            else:
                DL.fails=DL.fails+1
    else:
        DL.fails=DL.fails+1
        
    # Reset to default
    RetOfStep = DL.SendCommand('Reset to default')
    if (RetOfStep):
        DL.Check_RXResponse("04 00 00 00")
else:
    DL.SetWindowText("red", "Please use NSRED reader to test...")
    DL.fails=DL.fails+1
    
if readermodel == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")								
        
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )