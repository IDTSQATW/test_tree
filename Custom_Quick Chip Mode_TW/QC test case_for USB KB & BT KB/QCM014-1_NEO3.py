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

# Objective: NEO3-17020_DFEC4F B3b1 support disable CT fallback to MSR
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# Disable CT --> MSR Fallback
if (Result):
	DL.SetWindowText("black", "*** Disable CT → MSR Fallback")
	DL.SendIOCommand("IDG", "04 00 DFEC4F 08 01 00 02 00 00 00 00 00", 3000, 1) 
	DL.Check_RXResponse("04 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# Fallback to MSR: disable
if (Result): 
    DL.SetWindowText("black", "*** Insert IDT test card, @1st time")
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    strCardData1 = DL.ReadKeyBoardCardData(30000)
    if(-1 != strCardData1.find('DFEF6102F250')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "Error code FAIL")
        DL.fails=DL.fails+1
        
    DL.SetWindowText("black", "*** Insert IDT test card, @2nd time")
    strCardData1 = DL.ReadKeyBoardCardData(30000)
    if(-1 != strCardData1.find('DFEF6102F250')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "Error code FAIL")
        DL.fails=DL.fails+1
    
    DL.SetWindowText("black", "*** Insert IDT test card, @3rd time")
    strCardData1 = DL.ReadKeyBoardCardData(30000)
    if(-1 != strCardData1.find('DFEE25023004')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "RX data FAIL")
        DL.fails=DL.fails+1
        
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# Enable CT --> MSR Fallback (defalt)
if (Result):
	DL.SetWindowText("black", "*** Enable CT → MSR Fallback (defalt)")
	DL.SendIOCommand("IDG", "04 00 DFEC4F 08 01 00 00 00 00 00 00 00", 3000, 1) 
	DL.Check_RXResponse("04 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	DL.Check_RXResponse("01 00 00 00")	
	time.sleep(1)
        
DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
        
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )