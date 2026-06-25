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

# Objective: Tag FFEE1D can work if had been changed before

# Check data encryption TYPE is TDES	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 06 00 00 00 00 00 00")	
		
# Check reader is VP3350 or not
lcdtype = DL.ShowMessageBox("", "Is this VP3350?", 0)
if lcdtype == 1:
	readermodel = 1
	DL.SetWindowText("Green", "*** This is VP3350 ***")
	RetOfStep = DL.SendCommand('0105 do not use LCD')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")
else:
	readermodel = DL.ShowMessageBox("", "Is this NEO3 and upward project?", 0)
		
readertype = DL.ShowMessageBox("", "Is this NSRED project?", 0)
        
# Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")

if readertype == 1:
    if (Result):
        for i in range(1, 3):
            if readermodel == 1: #NEO3 and upward project
                # Set DFec60, mask/ truncate mode selection = 2	
                if (Result):
                    RetOfStep = DL.SendCommand('Set DFec60, mask/ truncate mode selection = 2')
                    if (RetOfStep):
                        Result = Result and DL.Check_RXResponse("C7 00")
                        
                if i == 1:
                    RetOfStep = DL.SendCommand('DFEC4A--08 04 2A 0C 31')
                if i == 2:
                    RetOfStep = DL.SendCommand('DFEE1D--06 04 2A 0C 31')
                Result = DL.Check_RXResponse("C7 00 00 00")	
            if readermodel == 0: #non-NEO3 and upward project
                if i == 1:
                    RetOfStep = DL.SendCommand('')
                    if (RetOfStep):
                        Result = DL.Check_RXResponse("C7 00 00 00")	
                if i == 2:
                    RetOfStep = DL.SendCommand('')
                    if (RetOfStep):
                        Result = DL.Check_RXResponse("C7 00 00 00")	
                    
            # cmd 60-10, insert card		
            if (Result):
                RetOfStep = DL.SendCommand('Activate Transaction')
                if (RetOfStep):
                    Result = DL.Check_RXResponse("60 63 00 00")
                    alldata = DL.Get_RXResponse(1)
                    CTresultcode = DL.GetTLV(alldata,"DFEE25")
                    if (Result):
                        Result = DL.Check_StringAB(DL.Get_RXResponse(1), '56 69 56 4F 74 65 63 68 32 00 60 00')
                        if (Result):
                            ksn = DL.GetTLV(alldata,"DFEE12")	
                            mask57 = DL.GetTLV(alldata,"57", 0)
                            enc57 = DL.GetTLV(alldata,"57", 1)
                            dec57 = DL.DecryptDLL(0,1, strKey, ksn, enc57)	
                            mask5A = DL.GetTLV(alldata,"5A", 0)
                            enc5A = DL.GetTLV(alldata,"5A", 1)
                            dec5A = DL.DecryptDLL(0,1, strKey, ksn, enc5A)	
                        
                            # Tag 57
                            if i == 1:
                                Result = DL.Check_StringAB(mask57, '57 A1 10 47 61 73 CC CC 01 01 D2 21 2C CC CC CC CC CC CC')
                            if i == 2:
                                Result = DL.Check_StringAB(mask57, '57 A1 10 47 61 CC CC CC 01 01 D2 21 2C CC CC CC CC CC CC')
                            if Result == True:
                                DL.SetWindowText("blue", "Tag 57_Mask: PASS")
                            else:
                                DL.fails=DL.fails+1
                                DL.SetWindowText("red", "Tag 57_Mask: FAIL")
                            
                            Result = DL.Check_StringAB(dec57, '57 10 47 61 73 90 01 01 01 D2 21 22 01 17 58 92 88 89 00 00 00 00 00 00')
                            if Result == True and DL.Check_RXResponse(1, '57 C1 18'):
                                DL.SetWindowText("blue", "Tag 57_Enc: PASS")
                            else:
                                DL.fails=DL.fails+1
                                DL.SetWindowText("red", "Tag 57_Enc: FAIL")

                            # Tag 5A
                            if i == 1:
                                Result = DL.Check_StringAB(mask5A, '5A A1 07 47 61 73 CC CC 01 01')
                            if i == 2:
                                Result = DL.Check_StringAB(mask5A, '5A A1 07 47 61 CC CC CC 01 01')
                            if Result == True:
                                DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
                            else:
                                DL.fails=DL.fails+1
                                DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
                            
                            Result = DL.Check_StringAB(dec5A, '5A 07 47 61 73 90 01 01 01 00 00 00 00 00 00 00')
                            if Result == True and DL.Check_RXResponse(1, '5A C1 10'):
                                DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
                            else:
                                DL.fails=DL.fails+1
                                DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
                            
                            # Tags 9F39/ FFEE01/ DFEE26
                            if DL.Check_RXResponse(1, "9F39 01 05") == False: 
                                DL.fails=DL.fails+1
                                DL.SetWindowText("Red", "Tag 9F39: FAIL")
                            if DL.Check_RXResponse(1, "FFEE01 ** DFEE300101") == False: 
                                DL.fails=DL.fails+1
                                DL.SetWindowText("Red", "Tag FFEE01: FAIL")				
                            if DL.Check_RXResponse(1, "DFEE26 02 E000") == False: 
                                DL.fails=DL.fails+1
                                DL.SetWindowText("Red", "Tag DFEE26: FAIL")

                    # cmd 60-11					
                    if  CTresultcode == "0010":
                        RetOfStep = DL.SendCommand('60-11 Contact Authenticate Transaction')
                        if (RetOfStep):
                            Result = DL.Check_RXResponse("60 63 00 00")
                            alldata = DL.Get_RXResponse(1)
                            CTresultcode = DL.GetTLV(alldata,"DFEE25")	
                            if (Result):
                                Result = DL.Check_RXResponse(1, '56 69 56 4F 74 65 63 68 32 00 60 00')
                                if (Result):
                                    # Tags 9F39/ FFEE01/ DFEE26
                                    if DL.Check_RXResponse(1, "9F39 01 05") == False: 
                                        DL.fails=DL.fails+1
                                        DL.SetWindowText("Red", "Tag 9F39: FAIL")
                                    if DL.Check_RXResponse(1, "FFEE01 ** DFEE300101") == False: 
                                        DL.fails=DL.fails+1
                                        DL.SetWindowText("Red", "Tag FFEE01: FAIL")				
                                    if DL.Check_RXResponse(1, "DFEE26 02 E000") == False: 
                                        DL.fails=DL.fails+1
                                        DL.SetWindowText("Red", "Tag DFEE26: FAIL")
                                
                    # cmd 60-12
                    if  CTresultcode == "0004":
                        RetOfStep = DL.SendCommand('60-12 Contact Apply Host Response')
                        if (RetOfStep):
                            Result = DL.Check_RXResponse("60 63 00 00")
                            alldata = DL.Get_RXResponse(1)
                            CTresultcode = DL.GetTLV(alldata,"DFEE25")
                            if (Result):
                                Result = DL.Check_RXResponse(1, '56 69 56 4F 74 65 63 68 32 00 60 00')
                                if (Result):
                                    # Tags 9F39/ FFEE01/ DFEE26
                                    if DL.Check_RXResponse(1, "9F39 01 05") == False: 
                                        DL.fails=DL.fails+1
                                        DL.SetWindowText("Red", "Tag 9F39: FAIL")
                                    if DL.Check_RXResponse(1, "FFEE01 ** DFEE300101") == False: 
                                        DL.fails=DL.fails+1
                                        DL.SetWindowText("Red", "Tag FFEE01: FAIL")				
                                    if DL.Check_RXResponse(1, "DFEE26 02 E000") == False: 
                                        DL.fails=DL.fails+1
                                        DL.SetWindowText("Red", "Tag DFEE26: FAIL")
    else:
        DL.fails=DL.fails+1
else:
    DL.SetWindowText("red", "Please use NSRED reader to test...")
    DL.fails=DL.fails+1

if lcdtype == 1:
	RetOfStep = DL.SendCommand('0105 default (VP3350)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")
        
# Reset to default
RetOfStep = DL.SendCommand('Reset to default')
if (RetOfStep):
    DL.Check_RXResponse("04 00 00 00")
        
# Set DFec60, mask/ truncate mode selection = default
RetOfStep = DL.SendCommand('Set DFec60, mask/ truncate mode selection = default')
if (RetOfStep):
    DL.Check_RXResponse("C7 00 00 00")
        
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )