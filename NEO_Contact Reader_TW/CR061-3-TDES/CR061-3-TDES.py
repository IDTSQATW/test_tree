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
	DL.SetWindowText("Green", "*** This is VP3350 ***")
	RetOfStep = DL.SendCommand('0105 do not use LCD')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")
else:
	DL.SetWindowText("Green", "*** This is Non-VP3350 ***")
		
# Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")
        
# CT config		
if (Result):
	RetOfStep = DL.SendCommand('60-16 Contact Set ICS Identification (02)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('60-03 Contact Set Application Data (VISA)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('60-03 Contact Set Application Data (MC)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('60-03 Contact Set Application Data (Discover)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('60-03 Contact Set Application Data (JCB)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('60-03 Contact Set Application Data (CUP)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('60-03 Contact Set Application Data (AMEX)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('60-06 Contact Set Terminal Data')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('60-0A Contact Set CA Public Key')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("60 00 00 00")			
        
# JUST write data in DFEE1D.
if (Result):
    RetOfStep = DL.SendCommand('DFEE1D--02 04 2A 0C 31')
    if (RetOfStep):
        Result = Result and DL.Check_RXResponse("C7 00 00 00")	
        
# Set DFec60, mask/ truncate mode selection = 3	
if (Result):
    RetOfStep = DL.SendCommand('Set DFec60, mask/ truncate mode selection = 3')
    if (RetOfStep):
        Result = Result and DL.Check_RXResponse("C7 00")

readertype = DL.ShowMessageBox("", "Is this SRED project?", 0)

if readertype == 1:
    if (Result):
        for i in range(1, 8):
            time.sleep(0.3)
            # cmd 60-10, insert card		
            if (Result):
                if i == 1:
                    RetOfStep = DL.SendCommand('Activate Transaction-1')
                if i == 2:
                    RetOfStep = DL.SendCommand('Activate Transaction-2')
                if i == 3:
                    RetOfStep = DL.SendCommand('Activate Transaction-3')
                if i == 4:
                    RetOfStep = DL.SendCommand('Activate Transaction-4')
                if i == 5:
                    RetOfStep = DL.SendCommand('Activate Transaction-5')
                if i == 6:
                    RetOfStep = DL.SendCommand('Activate Transaction-6')
                if i == 7:
                    RetOfStep = DL.SendCommand('Activate Transaction-7')
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
                                Result = DL.Check_StringAB(mask57, '57 A1 11 47 61 73 90 CC CC 00 10 D2 01 2C CC CC CC CC CC CC')
                            if i == 2:
                                Result = DL.Check_StringAB(mask57, '57 A1 11 54 13 33 00 CC CC 90 49 D2 51 2C CC CC CC CC CC CC')
                            if i == 3:
                                Result = DL.Check_StringAB(mask57, '57 A1 13 60 11 97 37 CC CC 00 05 D2 31 2C CC CC CC CC CC CC CC CC')
                            if i == 4:
                                Result = DL.Check_StringAB(mask57, '57 A1 13 62 10 94 80 CC CC 00 11 D3 01 0C CC CC CC CC CC CC CC CC')
                            if i == 5:
                                Result = DL.Check_StringAB(mask57, '57 A1 13 35 40 82 99 CC CC 10 12 D4 91 2C CC CC CC CC CC CC CC CC')
                            if i == 6:
                                Result = DL.Check_StringAB(mask57, '57 A1 13 37 42 45 CC CC C1 00 6D 24 12 CC CC CC CC CC CC CC CC CC')
                            if i == 7:
                                Result = DL.Check_StringAB(mask57, '57 A1 10 47 CC CC CC CC 01 01 D2 21 2C CC CC CC CC CC CC')
                            if Result == True:
                                DL.SetWindowText("blue", "Tag 57_Mask: PASS")
                            else:
                                DL.fails=DL.fails+1
                                DL.SetWindowText("red", "Tag 57_Mask: FAIL")
                            
                            if i == 1:
                                Result = DL.Check_StringAB(dec57, '57 11 47 61 73 90 01 01 00 10 D2 01 22 01 01 23 45 67 89')
                            if i == 2:
                                Result = DL.Check_StringAB(dec57, '57 11 54 13 33 00 89 09 90 49 D2 51 22 20 08 08 10 79 0F')
                            if i == 3:
                                Result = DL.Check_StringAB(dec57, '57 13 60 11 97 37 00 00 00 05 D2 31 22 01 10 00 05 57 00 00 0F')
                            if i == 4:
                                Result = DL.Check_StringAB(dec57, '57 13 62 10 94 80 00 00 00 11 D3 01 02 01 00 00 00 00 00 00 0F')
                            if i == 5:
                                Result = DL.Check_StringAB(dec57, '57 13 35 40 82 99 99 42 10 12 D4 91 22 01 00 00 00 00 00 00 0F')
                            if i == 6:
                                Result = DL.Check_StringAB(dec57, '57 13 37 42 45 00 17 51 00 6D 24 12 20 11 50 21 23 45 00 00 0F')
                            if i == 7:
                                Result = DL.Check_StringAB(dec57, '57 10 47 61 73 90 01 01 01 D2 21 22 01 17 58 92 88 89 00 00 00 00 00 00')
                            if Result == True:
                                DL.SetWindowText("blue", "Tag 57_Enc: PASS")
                            else:
                                DL.fails=DL.fails+1
                                DL.SetWindowText("red", "Tag 57_Enc: FAIL")

                            # Tag 5A
                            if i == 1:
                                Result = DL.Check_StringAB(mask5A, '5A A1 08 47 61 73 90 CC CC 00 10')
                            if i == 2:
                                Result = DL.Check_StringAB(mask5A, '5A A1 08 54 13 33 00 CC CC 90 49')
                            if i == 3:
                                Result = DL.Check_StringAB(mask5A, '5A A1 08 60 11 97 37 CC CC 00 05')
                            if i == 4:
                                Result = DL.Check_StringAB(mask5A, '5A A1 08 62 10 94 80 CC CC 00 11')
                            if i == 5:
                                Result = DL.Check_StringAB(mask5A, '5A A1 08 35 40 82 99 CC CC 10 12')
                            if i == 6:
                                Result = DL.Check_StringAB(mask5A, '5A A1 08 37 42 45 CC CC C1 00 6F')
                            if i == 7:
                                Result = DL.Check_StringAB(mask5A, '5A A1 07 47 CC CC CC CC 01 01')
                            if Result == True:
                                DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
                            else:
                                DL.fails=DL.fails+1
                                DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
                            
                            if i == 1:
                                Result = DL.Check_StringAB(dec5A, '5A 08 47 61 73 90 01 01 00 10')
                            if i == 2:
                                Result = DL.Check_StringAB(dec5A, '5A 08 54 13 33 00 89 09 90 49')
                            if i == 3:
                                Result = DL.Check_StringAB(dec5A, '5A 08 60 11 97 37 00 00 00 05')
                            if i == 4:
                                Result = DL.Check_StringAB(dec5A, '5A 08 62 10 94 80 00 00 00 11')
                            if i == 5:
                                Result = DL.Check_StringAB(dec5A, '5A 08 35 40 82 99 99 42 10 12')
                            if i == 6:
                                Result = DL.Check_StringAB(dec5A, '5A 08 37 42 45 00 17 51 00 6F')
                            if i == 7:
                                Result = DL.Check_StringAB(dec5A, '5A 07 47 61 73 90 01 01 01 00 00 00 00 00 00 00')
                            if Result == True:
                                DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
                            else:
                                DL.fails=DL.fails+1
                                DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
                            
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
                                    if DL.Check_RXResponse(1, "FFEE01 ** DFEE300101") == False: 
                                        DL.fails=DL.fails+1
                                        DL.SetWindowText("Red", "Tag FFEE01: FAIL")				
                                    if DL.Check_RXResponse(1, "DFEE26 02 E000") == False: 
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