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
	
else:
	DL.SetWindowText("Green", "*** non-VP3350 reader ***")	
    
readertype = DL.ShowMessageBox("", "Is this SRED project?", 0)

if readertype == 1:
    # Set DFec60, mask/ truncate mode selection = 3	
    if (Result):
        RetOfStep = DL.SendCommand('Set DFec60, mask/ truncate mode selection = 3')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("C7 00")
    
    # Check data encryption TYPE is TDES	
    if (Result):
        RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("C7 00 00 06 00 00 00 00 00 00")

    # Poll on demand
    if (Result):
        RetOfStep = DL.SendCommand('Poll on Demand')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("01 00 00 00")
            
    # JUST write data in DFEE1D/ DFEC4A both.
    if (Result):
        RetOfStep = DL.SendCommand('DFEE1D--06 04 2A 0C 31')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("C7 00 00 00")	

    # cmd 02-40, tap card
    if (Result):
        for i in range(1, 7):     #6 card brand transaction: Discover-16PAN/ JCB/ MC/ VISA/ AMEX/ Discover-14PAN; ***UnionPay should add when it support.
            if (Result):
                if i == 1: 
                    RetOfStep = DL.SendCommand('Activate Transaction-D16')
                if i == 2: 
                    RetOfStep = DL.SendCommand('Activate Transaction-JCB')
                if i == 3: 
                    RetOfStep = DL.SendCommand('Activate Transaction-MasterCard')
                if i == 4: 
                    RetOfStep = DL.SendCommand('Activate Transaction-Visa')
                if i == 5: 
                    RetOfStep = DL.SendCommand('Activate Transaction-AMEX')
                if i == 6: 
                    RetOfStep = DL.SendCommand('Activate Transaction-D14')
                if (RetOfStep):
                    Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 ** DF EE 12")
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
                            Result = DL.Check_RXResponse('36 07 05 00 CC CC 00 14 D4 91 2C CC CC CC CC CC CC CC CC')
                        if i == 2: 
                            Result = DL.Check_RXResponse('35 40 82 99 CC CC 10 12 D4 91 2C CC CC CC CC CC CC CC CC')
                        if i == 3:
                            Result = DL.Check_RXResponse('54 13 33 00 CC CC 00 10 D1 41 2C CC CC CC CC CC CC')
                        if i == 4:
                            Result = DL.Check_RXResponse('47 61 73 90 CC CC 00 10 D2 01 2C CC CC CC CC CC CC CC CC')
                        if i == 5:
                            Result = DL.Check_RXResponse('37 42 45 CC CC C0 00 1D 14 10 CC CC CC CC CC CC CC CC CC')
                        if i == 6:
                            Result = DL.Check_RXResponse('36 07 05 CC CC 00 14 D4 91 2C CC CC CC CC CC CC CC')
                            
                        if i <= 2 or i == 4 or i == 5:
                            if Result == True and Result2 == DL.Check_RXResponse("57 A1 13"):
                                DL.SetWindowText("blue", "Tag 57_Mask: PASS")
                        if i == 3 or i == 6:
                            if Result == True and Result2 == DL.Check_RXResponse("57 A1 11"):
                                DL.SetWindowText("blue", "Tag 57_Mask: PASS")
                        if Result == False or Result2 == False:
                            DL.SetWindowText("red", "Tag 57_Mask: FAIL")
                            DL.fails=DL.fails+1
                                
                        if i == 1:
                            Result = DL.Check_StringAB(dec57, '')
                        if i == 2:
                            Result = DL.Check_StringAB(dec57, '')
                        if i == 3:
                            Result = DL.Check_StringAB(dec57, '')
                        if i == 4:
                            Result = DL.Check_StringAB(dec57, '')
                        if i == 5:
                            Result = DL.Check_StringAB(dec57, '')
                        if i == 6:
                            Result = DL.Check_StringAB(dec57, '')
                            
                        if Result == True and DL.Check_RXResponse("57 C1 18"):
                            DL.SetWindowText("blue", "Tag 57_Enc: PASS")
                        else:
                            DL.SetWindowText("red", "Tag 57_Enc: FAIL")
                            DL.fails=DL.fails+1
                            
                        # Tag 5A
                        if i == 1:
                            Result = DL.Check_RXResponse('36 07 05 00 CC CC 00 14')
                        if i == 2:
                            Result = DL.Check_RXResponse('35 40 82 99 CC CC 10 12')
                        if i == 3:
                            Result = DL.Check_RXResponse('54 13 33 00 CC CC 00 10')
                        if i == 4:
                            Result = DL.Check_RXResponse('47 61 73 90 CC CC 00 10')
                        if i == 5:
                            Result = DL.Check_RXResponse('37 42 45 CC CC C0 00 1F')
                        if i == 6:
                            Result = DL.Check_RXResponse('36 07 05 CC CC 00 14')
                            
                        if i <= 5:
                            if Result == True and Result2 == DL.Check_RXResponse("5A A1 08"):
                                DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
                        if i == 6:
                            if Result == True and Result2 == DL.Check_RXResponse("5A A1 07"):
                                DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
                        if Result == False or Result2 == False:
                            DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
                            DL.fails=DL.fails+1
                                
                        if i == 1:
                            Result = DL.Check_StringAB(dec5A, '')
                        if i == 2:
                            Result = DL.Check_StringAB(dec5A, '')
                        if i == 3:
                            Result = DL.Check_StringAB(dec5A, '')
                        if i == 4:
                            Result = DL.Check_StringAB(dec5A, '')
                        if i == 5:
                            Result = DL.Check_StringAB(dec5A, '')
                        if i == 6:
                            Result = DL.Check_StringAB(dec5A, '')
                            
                        if Result == True and DL.Check_RXResponse("5A C1 10"):
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
        
    # Set DFec60, mask/ truncate mode selection = default
    if (Result):
        RetOfStep = DL.SendCommand('Set DFec60, mask/ truncate mode selection = default')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("C7 00 00 00")
        
else:
    # Set DFec60, mask/ truncate mode selection = 3, only support on SRED project
    if (Result):
        RetOfStep = DL.SendCommand('Set DFec60, mask/ truncate mode selection = 3')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("C7 0A")
    
if readermodel == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")								
        
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )