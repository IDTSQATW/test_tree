#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
RetOfStep = True
Result= True

Key='0123456789abcdeffedcba9876543210'
MacKey='0123456789abcdeffedcba9876543210'
PAN=''
strKey ='FEDCBA9876543210F1F1F1F1F1F1F1F1'

#Objective: Encryption OFF, CL test under Quick Chip Mode. (Discover/ VISA MSD/ VISA qVSDC (EMV)/ MasterCard (MSD)/ MChip (EMV)/ INTERAC)

#-----------------------------------------------------------------
# Check HW function
hwcheck = DL.ShowMessageBox("", "Does the project support CT readr", 0)
if hwcheck == 1:
    n = 4
else:
    n = 3

# Get Data Encryption (C7-37) = encryption OFF
if (Result):
	DL.SetWindowText("black", "*** Get Data Encryption (C7-37)")
	DL.SendIOCommand("IDG", "C7 37", 3000, 1) 
	DL.Check_RXResponse("C7 00 00 01 00")
	time.sleep(0.5)
#-----------------------------------------------------------------
if (Result):       
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, RS232 or USB")
    for i in range (1, n):
        if i == 1:
            DL.ShowMessageBox("Notice", "swipe card w/ abnormal method (transaction is failed) --> Click OK")
        if i == 2:
            DL.ShowMessageBox("Notice", "tap T=0 card --> Click OK")
        if i == 3:
            DL.ShowMessageBox("Notice", "insert card P/N: 80005206-002 (until reader beep, remove card) --> Click OK")
        strCardData = DL.GetResponse()
        DL.SetWindowText("blue", strCardData)
        target_patterns = [
            '56 69 56 4F 74 65 63 68 32 00 02',]
        if all(pattern in strCardData for pattern in target_patterns):
            DL.SetWindowText("GREEN", "Format PASS")
        else:
            DL.SetWindowText("red", "Format FAIL")
            DL.fails=DL.fails+1
        if i == 1:#MSR----------------------------
            target_patterns1 = [
                'DF EE 25 02 30 12',
                'DF EF 57',
                'DF EF 61 02 50 24',
                'DF EF 61 02 F2 20',]
            if all(pattern in strCardData for pattern in target_patterns1):
                DL.SetWindowText("GREEN", "MSR PASS")
            else:
                DL.SetWindowText("red", "MSR FAIL")
                DL.fails=DL.fails+1
        
        if i == 2:#CL----------------------------
            target_patterns1 = [
                'DF EE 02 04',]
            if all(pattern in strCardData for pattern in target_patterns1):
                DL.SetWindowText("GREEN", "CL PASS")
            else:
                DL.SetWindowText("red", "CL FAIL")
                DL.fails=DL.fails+1
        
        if i == 3:#CT----------------------------
            target_patterns1 = [
                'DF EE 25 02 50',]
            if all(pattern in strCardData for pattern in target_patterns1):
                DL.SetWindowText("GREEN", "CT PASS")
            else:
                DL.SetWindowText("red", "CT FAIL")
                DL.fails=DL.fails+1
else:
    DL.fails=DL.fails+1
#-----------------------------------------------------------------Change to 
#-----------------------------------------------------------------
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )