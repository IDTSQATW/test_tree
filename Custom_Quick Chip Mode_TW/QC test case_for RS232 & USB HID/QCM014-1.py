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

# Check which interface
hwcheck = DL.ShowMessageBox("", "Do you test USB-HID now?", 0)
#-----------------------------------------------------------------
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
    if hwcheck == 1:#USB-HID
        DL.SendIOCommand("IDG", "04 00 DFEC4F 08 05 00 02 00 00 00 00 00", 3000, 1) 
        DL.Check_RXResponse("04 00 00 00")	
    if hwcheck == 0:#RS232
        DL.SendIOCommand("IDG", "04 00 DFEC4F 08 03 00 02 00 00 00 00 00", 3000, 1) 
        DL.Check_RXResponse("04 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# 18-01 to let NGAT to reconnect
if (Result):
	DL.SetWindowText("black", "*** Ping the reader")
	DL.SendIOCommand("IDG", "1801", 3000, 1) 
	DL.Check_RXResponse("18 00 00 00")	
	time.sleep(0.2)
    
# Fallback to MSR: disable
if (Result): 
    DL.ShowMessageBox("Notice", "Insert MSR card: the 1st time (remove card) --> Click OK")
    strCardData = DL.GetResponse()
    DL.SetWindowText("blue", strCardData)
    target_patterns1 = [
        '56 69 56 4F 74 65 63 68 32 00 02',
        'DF EF 61 02 F2 50',]
    if all(pattern in strCardData for pattern in target_patterns1):
        DL.SetWindowText("GREEN", "Format PASS")
    else:
        DL.SetWindowText("red", "Format FAIL")
        DL.fails=DL.fails+1
    
    DL.ShowMessageBox("Notice", "Insert MSR card: the 2nd time (remove card) --> Click OK")
    strCardData = DL.GetResponse()
    DL.SetWindowText("blue", strCardData)
    target_patterns1 = [
        '56 69 56 4F 74 65 63 68 32 00 02',
        'DF EF 61 02 F2 50',]
    if all(pattern in strCardData for pattern in target_patterns1):
        DL.SetWindowText("GREEN", "Format PASS")
    else:
        DL.SetWindowText("red", "Format FAIL")
        DL.fails=DL.fails+1
    
    DL.ShowMessageBox("Notice", "Insert MSR card: the 3rd time (remove card) --> Click OK")
    strCardData = DL.GetResponse()
    DL.SetWindowText("blue", strCardData)
    target_patterns1 = [
        '56 69 56 4F 74 65 63 68 32 00 02',
        'DF EE 25 02 30 04',]
    if all(pattern in strCardData for pattern in target_patterns1):
        DL.SetWindowText("GREEN", "Format PASS")
    else:
        DL.SetWindowText("red", "Format FAIL")
        DL.fails=DL.fails+1      
#-----------------------------------------------------------------Reset default
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# Enable CT --> MSR Fallback (defalt)
if (Result):
    DL.SetWindowText("black", "*** Enable CT → MSR Fallback (defalt)")
    if hwcheck == 1:#USB-HID
        DL.SendIOCommand("IDG", "04 00 DFEC4F 08 05 00 00 00 00 00 00 00", 3000, 1) 
        DL.Check_RXResponse("04 00 00 00")	
    if hwcheck == 0:#RS232
        DL.SendIOCommand("IDG", "04 00 DFEC4F 08 03 00 00 00 00 00 00 00", 3000, 1) 
        DL.Check_RXResponse("04 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	DL.Check_RXResponse("01 00 00 00")	
	time.sleep(1)
        
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )