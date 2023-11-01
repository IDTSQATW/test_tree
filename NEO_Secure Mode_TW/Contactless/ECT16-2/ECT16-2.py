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

# Check data encryption TYPE	
if platform == 1: #NEOII and upward
    if (Result):
        RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
        if (RetOfStep):
            Result = DL.Check_RXResponse("C7 00 00 06 00 01 00 00 00 00")
else:
    if (Result): #NEOI
        RetOfStep = DL.SendCommand('Encryption Type -- TDES')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("C7 00 00 01 00")

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
    alldata = DL.Get_RXResponse(0)
    if (RetOfStep):
        if platform == 1: #NEOII and upward
            Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** 61")
        if platform == 0: #NEOI
            Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** 41")
            
        if (Result):     
            # Tag 5A
            Result = DL.Check_RXResponse('5A085413330089600010')
            if Result == True:
                DL.SetWindowText("blue", "Tag 5A_Mask: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
                
            # Tag 57
            Result = DL.Check_RXResponse('57115413330089600010D14122010123409172')
            if Result == True:
                DL.SetWindowText("blue", "Tag 57_Mask: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag 57_Mask: FAIL")
                
            # Tags 9F39/ FFEE01/ DFEE26
            if DL.Check_RXResponse("9F39 01 07"): 
                DL.SetWindowText("blue", "Tag 9F39: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("Red", "Tag 9F39: FAIL")
            
            if platform == 1: #NEOII and upward
                Result = DL.Check_RXResponse("FFEE01 ** DFEE300100")
            if platform == 0: #NEOI
                Result = DL.Check_RXResponse("FFEE01 ** DF300100")
            if Result == False:
                DL.fails=DL.fails+1
                DL.SetWindowText("Red", "Tag DF**30: FAIL")			
                
            if platform == 1: #NEOII and upward
                Result = DL.Check_RXResponse("DFEE26 02 6100")
            if platform == 0: #NEOI
                Result = DL.Check_RXResponse("DFEE26 01 41")
            if Result == False:
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