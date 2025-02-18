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

# Check data encryption TYPE	
if platform == 1: #NEOII and upward
    if (Result):
        RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
        if (RetOfStep):
            Result = DL.Check_RXResponse("C7 00 00 06 00 01 00 00 00 00")
else:
    if (Result): #NEOI
        RetOfStep = DL.SendCommand('Set Encryption Type = AES')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("C7 00 00 00")
    if (Result): #NEOI
        RetOfStep = DL.SendCommand('Encryption Type -- AES')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("C7 00 00 01 01")
		
# Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")

# Set group 80 -- DF 81 1B = 80
if platform == 1: #NEOII and upward
    if (Result):
        RetOfStep = DL.SendCommand('Set group 80 -- DF 81 1B = 80')
        if (RetOfStep):
            Result = DL.Check_RXResponse("04 00 00 00")		
else:
    if (Result): #NEOI
        RetOfStep = DL.SendCommand('set FFFC 02 in G1')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("04 00 00 00")
		
# cmd 02-40, tap card
if (Result):
    if lcdtype == 1:
        RetOfStep = DL.SendCommand('Activate Transaction w/ LCD')
        rx = 0
    if lcdtype == 0:
        if platform == 1: #NEOII and upward
            RetOfStep = DL.SendCommand('Activate Transaction w/o LCD')	
            rx = 5
        if platform == 0: #NEOI
            RetOfStep = DL.SendCommand('Activate Transaction w/o LCD (NEOI)')	
            rx = 0
    if (RetOfStep):
        alldata = DL.Get_RXResponse(rx)
        if platform == 1: #NEOII and upward
            Result = DL.Check_RXResponse(rx, "56 69 56 4F 74 65 63 68 32 00 02 23 ** E3 ** DF EE 12")
            ksn = DL.GetTLV(alldata,"DFEE12")
        if platform == 0: #NEOI
            Result = DL.Check_RXResponse(rx, "56 69 56 4F 74 65 63 68 32 00 02 23 ** C3 ** FFEE12")
            ksn = DL.GetTLV(alldata,"FFEE12")
            
        if (Result):
            tagFF8105 = DL.GetTLV(alldata,"FF8105", 0)
            mask5A = DL.GetTLV(tagFF8105,"5A", 0)
            enc5A = DL.GetTLV(tagFF8105,"5A", 1)
            dec5A = DL.DecryptDLL(0,2, strKey, ksn, enc5A)	
            mask57 = DL.GetTLV(tagFF8105,"57", 0)
            enc57 = DL.GetTLV(tagFF8105,"57", 1)
            dec57 = DL.DecryptDLL(0,2, strKey, ksn, enc57)	

            if lcdtype == 1:		
            # Tag 5A
                Result = DL.Check_StringAB(mask5A, '5413CCCCCCCC0010')
                if Result == True and DL.Check_RXResponse(rx, "5A A1 08"):
                    DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
                else:
                    DL.fails=DL.fails+1
                    DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
                    
                Result = DL.Check_StringAB(dec5A, '5A085413330089600010000000000000')
                if Result == True and DL.Check_RXResponse(rx, "5A C1 10"):
                    DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
                else:
                    DL.fails=DL.fails+1
                    DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
                    
            # Tag 57
                if platform == 0: #NEOI
                    Result = DL.Check_RXResponse(rx, '5413CCCCCCCC0010D1412201CCCCCCCCCC')
                else: #NEOII and upward
                    Result = DL.Check_StringAB(mask57, '5413CCCCCCCC0010D1412CCCCCCCCCCCCC')
                if Result == True and DL.Check_RXResponse(rx, "57 A1 11"):
                    DL.SetWindowText("blue", "Tag 57_Mask: PASS")
                else:
                    DL.fails=DL.fails+1
                    DL.SetWindowText("red", "Tag 57_Mask: FAIL")
                    
                Result = DL.Check_StringAB(dec57, '57115413330089600010D141220101234091720000000000')
                if Result == True and DL.Check_RXResponse(rx, "57 C1 20"):
                    DL.SetWindowText("blue", "Tag 57_Enc: PASS")
                else:
                    DL.fails=DL.fails+1
                    DL.SetWindowText("red", "Tag 57_Enc: FAIL")

            if lcdtype == 0:
            # Tag 5A
                Result = DL.Check_StringAB(mask5A, '5413CCCCCCCC0010')
                if Result == True and DL.Check_RXResponse(rx, "5A A1 08"):
                    DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
                else:
                    DL.fails=DL.fails+1
                    DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
                    
                Result = DL.Check_StringAB(dec5A, '5A085413330089600010000000000000')
                if Result == True and DL.Check_RXResponse(rx, "5A C1 10"):
                    DL.SetWindowText("blue", "Tag 5A_Enc: PASS")
                else:
                    DL.fails=DL.fails+1
                    DL.SetWindowText("red", "Tag 5A_Enc: FAIL")
                    
            # Tag 57
                if platform == 0: #NEOI
                    Result = DL.Check_RXResponse(rx, '5413CCCCCCCC0010D1412201CCCCCCCCCC')
                else: #NEOII and upward
                    Result = DL.Check_StringAB(mask57, '5413CCCCCCCC0010D1412CCCCCCCCCCCCC')
                if Result == True and DL.Check_RXResponse(rx, "57A111"):
                    DL.SetWindowText("blue", "Tag 57_Mask: PASS")
                else:
                    DL.fails=DL.fails+1
                    DL.SetWindowText("red", "Tag 57_Mask: FAIL")
                    
                Result = DL.Check_StringAB(dec57, '57115413330089600010D141220101234091720000000000')
                if Result == True and DL.Check_RXResponse(rx, "57 C1 20"):
                    DL.SetWindowText("blue", "Tag 57_Enc: PASS")
                else:
                    DL.fails=DL.fails+1
                    DL.SetWindowText("red", "Tag 57_Enc: FAIL")	
                    
            # Tags 9F39/ FFEE01/ DFEE26
            if DL.Check_RXResponse(rx, "9F39 01 07") == False: 
                DL.fails=DL.fails+1
                DL.SetWindowText("Red", "Tag 9F39: FAIL")
                    
            if platform == 1: #NEOII and upward
                Result = DL.Check_RXResponse(rx, "FFEE01 ** DFEE300100")
            if platform == 0: #NEOI
                Result = DL.Check_RXResponse(rx, "FFEE01 ** DF300100")
            if Result == False:
                DL.fails=DL.fails+1
                DL.SetWindowText("Red", "Tag DF**30: FAIL")			
                    
            if platform == 1: #NEOII and upward
                Result = DL.Check_RXResponse(rx, "DFEE26 02 E300")
            if platform == 0: #NEOI
                Result = DL.Check_RXResponse(rx, "DFEE26 01 C3")
            if Result == False:
                DL.fails=DL.fails+1
                DL.SetWindowText("Red", "Tag DFEE26: FAIL")			
        else:
            DL.fails=DL.fails+1
else:
    DL.fails=DL.fails+1

# Reset to default
RetOfStep = DL.SendCommand('Reset to default')
if (RetOfStep):
	DL.Check_RXResponse("04 00 00 00")	
    
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )