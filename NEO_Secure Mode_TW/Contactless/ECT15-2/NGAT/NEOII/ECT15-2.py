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

# Encryption Type -- TDES
if (Result):
	RetOfStep = DL.SendCommand('Encryption Type -- TDES')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 00")		
		
# Burst mode OFF & Poll on demand		
if (Result):
	RetOfStep = DL.SendCommand('Burst mode Off')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("04 00 00 00")	
if (Result):
	RetOfStep = DL.SendCommand('Poll on Demand')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("01 00 00 00")
		
# # TTQ 20 00 40 00
# if (Result):
	# RetOfStep = DL.SendCommand('TTQ 20 00 40 00')
	# if (RetOfStep):
		# Result = Result and DL.Check_RXResponse("04 00 00 00")	

# cmd 02-40, tap card
if (Result):
    RetOfStep = DL.SendCommand('Activate Transaction')
    if (RetOfStep):
        Result = DL.Check_RXResponse("56 69 56 4F 74 65 63 68 32 00 02 23 ** 61")
        if (Result):
            alldata = DL.Get_RXResponse(0)
            mask57 = DL.GetTLV(alldata,"57", 0)
            mask5A = DL.GetTLV(alldata,"5A", 0)
            
        # Tag 57
            Result = DL.Check_StringAB(mask57, '47 61 73 90 01 01 00 10 D3 01 21 20 00 12 33 99 00 03 1F')
            if Result == False:
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag 57: FAIL")
            else:
                DL.SetWindowText("blue", "Tag 57: PASS")

        # Tag 5A
            Result = DL.Check_StringAB(mask5A, '47 61 73 90 01 01 00 10')
            if Result == False:
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag 5A: FAIL")
            else:
                DL.SetWindowText("blue", "Tag 5A: PASS")
                
        # Tags 9F39/ FFEE01/ DFEE26
            if DL.Check_RXResponse("9F39 01 07"): 
                DL.SetWindowText("blue", "Tag 9F39: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("Red", "Tag 9F39: FAIL")
            
            if DL.Check_RXResponse("FFEE01 ** DFEE300100"): 
                DL.SetWindowText("blue", "Tag FFEE01: PASS")
            else:
                DL.fails=DL.fails+1
                DL.SetWindowText("Red", "Tag FFEE01: FAIL")
            
            if DL.Check_RXResponse("DFEE26 02 6100"): 
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