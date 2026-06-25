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
            
    # JUST write data in DFEE1D.
    if (Result):
        RetOfStep = DL.SendCommand('DFEE1D--02 04 2A 0C 31')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("C7 00 00 00")	

    # cmd 02-40, tap card
    if (Result):
        for i in range(1, 7):     #6 card brand transaction, those cards did not meet New_Truncate table.
            if (Result):
                time.sleep(0.3)
                if i == 1: 
                    RetOfStep = DL.SendCommand('Activate Transaction-D15')
                if i == 2: 
                    RetOfStep = DL.SendCommand('Activate Transaction-JCB')
                if i == 3: 
                    RetOfStep = DL.SendCommand('Activate Transaction-MasterCard')
                if i == 4: 
                    RetOfStep = DL.SendCommand('Activate Transaction-Visa')
                if i == 5: 
                    RetOfStep = DL.SendCommand('Activate Transaction-AMEX')
                if i == 6: 
                    RetOfStep = DL.SendCommand('Activate Transaction-interac')
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
                            Result = DL.Check_RXResponse('57 A1 12 36 CC CC CC CC C0 00 1D 49 12 CC CC CC CC CC CC CC CC')
                        if i == 2: 
                            Result = DL.Check_RXResponse('57 A1 12 35 CC CC CC CC 10 12 D4 91 2C CC CC CC CC CC CC CC CC')
                        if i == 3:
                            Result = DL.Check_RXResponse('57 A1 10 54 CC CC CC CC 60 00 D1 41 2C CC CC CC CC CC CC')
                        if i == 4:
                            Result = DL.Check_RXResponse('57 A1 12 47 CC CC CC CC 01 00 D2 01 2C CC CC CC CC CC CC CC CC')
                        if i == 5:
                            Result = DL.Check_RXResponse('57 A1 12 37 CC CC CC CC 10 14 D1 41 0C CC CC CC CC CC CC CC CC')
                        if i == 6:
                            Result = DL.Check_RXResponse('57 A1 11 54 CC CC CC CC CC 15 13 D0 51 2C CC CC CC CC CC CC')
                            
                        if Result == False:
                            DL.SetWindowText("red", "Tag 57_Mask: FAIL")
                            DL.fails=DL.fails+1
                        else:
                            DL.SetWindowText("blue", "Tag 57_Mask: PASS")
                                
                        if i == 1:
                            Result = DL.Check_StringAB(dec57, '57 12 36 07 05 00 00 00 00 1D 49 12 10 10 00 03 32 11 23 01')
                        if i == 2:
                            Result = DL.Check_StringAB(dec57, '57 12 35 40 82 99 42 10 12 D4 91 22 01 55 55 55 55 55 55 2F')
                        if i == 3:
                            Result = DL.Check_StringAB(dec57, '57 10 54 13 33 00 89 60 00 D1 41 22 01 01 23 40 91 72')
                        if i == 4:
                            Result = DL.Check_StringAB(dec57, '57 12 47 61 73 90 01 01 00 D2 01 21 20 00 12 33 99 00 03 1F')
                        if i == 5:
                            Result = DL.Check_StringAB(dec57, '57 12 37 42 45 45 54 10 14 D1 41 07 02 10 10 00 00 00 00 00')
                        if i == 6:
                            Result = DL.Check_StringAB(dec57, '57 11 54 13 33 90 00 00 15 13 D0 51 22 20 01 23 45 67 89')
                            
                        if Result == True and DL.Check_RXResponse("57 C1 18"):
                            DL.SetWindowText("blue", "Tag 57_Enc: PASS")
                        else:
                            DL.SetWindowText("red", "Tag 57_Enc: FAIL")
                            DL.fails=DL.fails+1
                            
                        # Tag 5A
                        if i == 1:
                            Result = DL.Check_RXResponse('5A A1 08 36 CC CC CC CC C0 00 1F')
                        if i == 2:
                            Result = DL.Check_RXResponse('5A A1 07 35 CC CC CC CC 10 12')
                        if i == 3:
                            Result = DL.Check_RXResponse('5A A1 07 54 CC CC CC CC 60 00')
                        if i == 4:
                            Result = DL.Check_RXResponse('5A A1 07 47 CC CC CC CC 01 00')
                        if i == 5:
                            Result = DL.Check_RXResponse('5A A1 07 37 CC CC CC CC 10 14')
                        if i == 6:
                            Result = DL.Check_RXResponse('5A A1 08 54 CC CC CC CC CC 15 13')

                        if Result == False:
                            DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
                            DL.fails=DL.fails+1
                        else:
                            DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
                                
                        if i == 1:
                            Result = DL.Check_StringAB(dec5A, '5A 08 36 07 05 00 00 00 00 1F')
                        if i == 2:
                            Result = DL.Check_StringAB(dec5A, '5A 07 35 40 82 99 42 10 12')
                        if i == 3:
                            Result = DL.Check_StringAB(dec5A, '5A 07 54 13 33 00 89 60 00')
                        if i == 4:
                            Result = DL.Check_StringAB(dec5A, '5A 07 47 61 73 90 01 01 00')
                        if i == 5:
                            Result = DL.Check_StringAB(dec5A, '5A 07 37 42 45 45 54 10 14')
                        if i == 6:
                            Result = DL.Check_StringAB(dec5A, '5A 08 54 13 33 90 00 00 15 13')
                            
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
    RetOfStep = DL.SendCommand('Set DFec60, mask/ truncate mode selection = default')
    if (RetOfStep):
        DL.Check_RXResponse("C7 00 00 00")
        
else:
    # Set DFec60, mask/ truncate mode selection = 3, only support on SRED project
    if (Result):
        RetOfStep = DL.SendCommand('Set DFec60, mask/ truncate mode selection = 3')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("C7 05")
    
if readermodel == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")								
        
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )