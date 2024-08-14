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

# Objective: check Timeout feature if Fallback to MSR transaction
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(6)
    
# Set tags DFEE20/ DFEE22
if (Result):
	DL.SetWindowText("black", "*** Set tags DFEE20/ DFEE22")
	DL.SendIOCommand("IDG", "60 06 0a 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 DF EE 20 01 3C DF EE 21 01 0A DF EE 22 03 32 3C 3C", 3000, 1) 
	Result = DL.Check_RXResponse("60 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# Fallback to CT, then Fallback to MSR
if (Result): 
    DL.SetWindowText("black", "*** Insert IDT test card, @1st time")
    strCardData1 = DL.ReadKeyBoardCardData(10000)
    if(-1 != strCardData1.find('DFEF6102F220')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "Error code FAIL")
        DL.fails=DL.fails+1
        
    DL.SetWindowText("black", "*** Insert IDT test card, @2nd time")
    strCardData1 = DL.ReadKeyBoardCardData(10000)
    if(-1 != strCardData1.find('DFEF6102F220')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "Error code FAIL")
        DL.fails=DL.fails+1
    
    DL.SetWindowText("black", "*** Insert IDT test card, @3rd time")
    strCardData1 = DL.ReadKeyBoardCardData(10000)
    if(-1 != strCardData1.find('DFEF6102F222')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "Error code FAIL")
        DL.fails=DL.fails+1
        
    DL.SetWindowText("black", "*** Waiting for 60 sec, shuold see timeout...")
    strCardData2 = DL.ReadKeyBoardCardData(61000)
    if(-1 != strCardData2.find('DFEF61023013')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "Time-out data FAIL")
        DL.fails=DL.fails+1
        DL.SendIOCommand("IDG", "05 01", 3000, 1) 
        
    speedcheck = DL.ShowMessageBox("", "LED 3 is ON (flash status) if fallback to MSR reader, LED 3 is OFF if fallback timeout?", 0)
    if speedcheck != 1:
        DL.SetWindowText("Red", "LED FAIL")
        DL.fails=DL.fails+1
        
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )