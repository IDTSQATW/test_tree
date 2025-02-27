#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey=''
PAN=''
strKey ='FEDCBA9876543210F1F1F1F1F1F1F1F1'
rx = 0

#Objective: to verify AES DUKPT Management, AES-128 Working Key encryption/ decryption function

# Check reader is VP3350 or not
lcdtype = DL.ShowMessageBox("", "Is this VP3350?", 0)
if lcdtype == 1:
	DL.SetWindowText("Green", "*** This is VP3350 ***")
	RetOfStep = DL.SendCommand('0105 do not use LCD')
	if (RetOfStep):
		Result = DL.Check_RXResponse("01 00 00 00")
else:
	DL.SetWindowText("Green", "*** non-VP3350 reader ***")
    
# Check platform
platform = DL.ShowMessageBox("", "Is the project NEOII and upward?", 0)
if platform == 1:
	DL.SetWindowText("Green", "*** The project is NEOII and upward ***")
else:
	DL.SetWindowText("Green", "*** The project is NEOI ***")

# Check data encryption TYPE is TDES	
if (Result):
	RetOfStep = DL.SendCommand('Get DUKPT DEK Attribution based on KeySlot (C7-A3)')
	if (RetOfStep):
		Result = DL.Check_RXResponse("C7 00 00 06 01 02 00 00 00 00")
        if Result == False:
            RetOfStep = DL.SendCommand('Encryption Type -- TDES')
            if (RetOfStep):
                Result = DL.Check_RXResponse("C7 00 00 01 00")
   
# CL test
if (Result):
    if lcdtype == 1:
        RetOfStep = DL.SendCommand('02-40 (enable CL only)')
        rx = 0 # for VP3350
    if lcdtype == 0: 
        RetOfStep = DL.SendCommand('02-40 (enable CL only) w/ LCD')
        rx = 0 # for any project AT cmd did not return 61-01
    if (RetOfStep):
        alldata = DL.Get_RXResponse(rx)
        Result = DL.Check_RXResponse(rx, "56 69 56 4F 74 65 63 68 32 00 02 23 ** E5 ** DF EE 12")
        ksn = DL.GetTLV(alldata,"DFEE12")
        if (Result):  
            # 57
            DL.SetWindowText("blue", "Tag 57 Mask/ Encryption data:")
            mask57 = DL.GetTLV_Embedded(alldata,"57", 0)
            enc57 = DL.GetTLV_Embedded(alldata,"57", 1)
            DL.SetWindowText("blue", "Tag 57 Decryption data:")
            dec57 = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc57)	
            if platform == 1: # NEOII and upward
                Result = DL.Check_RXResponse(rx, '57A1136372CCCCCCCC9994D4912CCCCCCCCCCCCCCCCC')
            if platform == 0: # NEOI
                Result = DL.Check_RXResponse(rx, '57A1136372CCCCCCCC9994D4912201CCCCCCCCCCCCCC')
            if Result == False: 
                DL.fails=DL.fails+1
                DL.SetWindowText("red", "Tag 57_Mask: FAIL")
            if DL.Check_StringAB(dec57, '57136372040199999994D49122010000000000000F') == False:
                DL.SetWindowText("red", "Tag 57_Enc: FAIL")
                
            # 5A
            DL.SetWindowText("blue", "Tag 5A Mask/ Encryption data:")
            mask5A = DL.GetTLV_Embedded(alldata,"5A", 0)
            enc5A = DL.GetTLV_Embedded(alldata,"5A", 1)
            DL.SetWindowText("blue", "Tag 5A Decryption data:")
            dec5A = DL.AES_DUPKT_EMVData_Decipher(ksn, strKey, enc5A)	
            if DL.Check_RXResponse(rx, '5AA1086372CCCCCCCC9994') == False:
                DL.SetWindowText("red", "Tag 5A_Mask: FAIL")
            if DL.Check_StringAB(dec5A, '5A086372040199999994') == False:
                DL.SetWindowText("red", "Tag 5A_Enc: FAIL")

            # Tags 9F39/ DFEE26
            if DL.Check_RXResponse(rx, "9F39 01 07") == False: 
                DL.SetWindowText("Red", "Tag 9F39: FAIL")
            if platform == 1: # NEOII and upward
                Result = DL.Check_RXResponse(rx, "DFEE26 02 E501")
            if platform == 0: # NEOI
                Result = DL.Check_RXResponse(rx, "DFEE26 01 E5")
            if Result == False: 
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

if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )