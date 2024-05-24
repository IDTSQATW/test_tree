#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
strKey ='0123456789ABCDEFFEDCBA9876543210'
rx = 0

#Objective: to verify TDES DUKPT Management, AES-128 (Strong is AES-112) encryption/ decryption function

# Check platform
platform = DL.ShowMessageBox("", "Is the project NEOII and upward?", 0)
if platform == 1:
	DL.SetWindowText("Green", "*** The project is NEOII and upward ***")
else:
	DL.SetWindowText("Green", "*** The project is NEOI ***")
    
# Get encryption status(03)
if (Result):
	RetOfStep = DL.SendCommand('Get encryption status(03)')
	if (RetOfStep):
		Result = Result and DL.Check_RXResponse("C7 00 00 01 03")

# Set group A0
if platform == 1: #NEOII and upward
    if (Result):
        RetOfStep = DL.SendCommand('Set group A0')
        if (RetOfStep):
            Result = Result and DL.Check_RXResponse("04 00 00 00")		

# CL test
if (Result):
    # Check project
    modeltype = DL.ShowMessageBox("", "Is this VP3350?", 0)
    if modeltype == 1: # for VP3350
        rx = 5
        RetOfStep = DL.SendCommand('02-40 (enable CL only)')
    else: # for non-VP3350
        rx = 0
        RetOfStep = DL.SendCommand('02-40 (enable CL only) RX w/o cmd 61-01')
    if (RetOfStep):
        alldata = DL.Get_RXResponse(rx)
        if platform == 1: #NEOII and upward
            Result = DL.Check_RXResponse(rx, "56 69 56 4F 74 65 63 68 32 00 02 23 ** E3 ** DF EE 12")
            ksn = DL.GetTLV(alldata,"DFEE12")
        if platform == 0: #NEOI
            Result = DL.Check_RXResponse(rx, "56 69 56 4F 74 65 63 68 32 00 02 23 ** C3 ** FF EE 12")
            ksn = DL.GetTLV(alldata,"FFEE12")
            FF8105 = DL.GetTLV(alldata,"FF8105", 0)
        if (Result):
            # 57
            DL.SetWindowText("blue", "Tag 57 Mask/ Encryption data:")
            mask57 = DL.GetTLV(alldata,"57", 0)
            enc57 = DL.GetTLV(alldata,"57", 1)
            DL.SetWindowText("blue", "Tag 57 Decryption data:")
            dec57 = DL.DecryptDLL(0,2, strKey, ksn, enc57)	
            if platform == 1: #NEOII and upward
                correctMask57 = "57A1133742CCCCCCC0001D1410CCCCCCCCCCCCCCCCCC"
            else: #NEOI
                correctMask57 = "57A1133742CCCCCCC0001D1410702CCCCCCCCCCCCCCC"
            if DL.Check_RXResponse(rx, correctMask57) == False:
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag 57_Mask: FAIL")
            if DL.Check_StringAB(dec57, '5713374245455400001D141070210100000000000F0000000000000000000000') == False:
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag 57_Enc: FAIL")
            # 5A
            DL.SetWindowText("blue", "Tag 5A Mask/ Encryption data:")
            mask5A = DL.GetTLV(alldata,"5A", 0)
            enc5A = DL.GetTLV(alldata,"5A", 1)
            DL.SetWindowText("blue", "Tag 5A Decryption data:")
            dec5A = DL.DecryptDLL(0,2, strKey, ksn, enc5A)	
            if DL.Check_RXResponse(rx, '5AA108 3742CCCCCCC0001F') == False:
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
            if DL.Check_StringAB(dec5A, '5A08374245455400001F000000000000') == False:
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag 5A_Enc: FAIL")

            # Tags 9F39/ DFEE26
            if DL.Check_RXResponse(rx, "9F39 01 07") == False: 
                DL.fails=DL.fails+1
                DL.SetWindowText("Red", "Tag 9F39: FAIL")
               
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

if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )