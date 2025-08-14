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

#Objective: for issue #CS-4237
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# Set transaction interface = CT+MSR
if (Result):
	DL.SetWindowText("black", "*** Set transaction interface = CT+MSR")
	DL.SendIOCommand("IDG", "04 00 DF EF 37 01 05", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
    
# DFED5A Byte 4 = 02
if (Result):
	DL.SetWindowText("black", "*** DFED5A Byte 4 = 02")
	DL.SendIOCommand("IDG", "04 00 DFED5A 08 00 00 00 02 00 00 00 00", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)

# CT transaction
if (Result): 
    DL.SetWindowText("black", "*** Insert T=0 card")
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    strCardData = DL.ReadKeyBoardCardData(30000)
    if(-1 != strCardData.find('DFEE25020003')):
        DL.SetWindowText("blue", "DFEE25 PASS")
    else:
        DL.SetWindowText("red", "DFEE25 FAIL")
        DL.fails=DL.fails+1
        
    speedcheck = DL.ShowMessageBox("", "Reader will beep 'AFTER' outputting data?", 0)
    if speedcheck != 1:
        DL.SetWindowText("Red", "Buzzer FAIL")
        DL.fails=DL.fails+1
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# DFED5A Byte 4 = 00 (default)
if (Result):
	DL.SetWindowText("black", "*** DFED5A Byte 4 = 00 (default)")
	DL.SendIOCommand("IDG", "04 00 DFED5A 08 00 00 00 00 00 00 00 00", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)

# CT transaction
if (Result): 
    DL.SetWindowText("black", "*** Insert T=0 card")
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    strCardData = DL.ReadKeyBoardCardData(30000)
    if(-1 != strCardData.find('DFEE25020003')):
        DL.SetWindowText("blue", "DFEE25 PASS")
    else:
        DL.SetWindowText("red", "DFEE25 FAIL")
        DL.fails=DL.fails+1
        
    speedcheck = DL.ShowMessageBox("", "Reader will beep 'DURING' outputting data?", 0)
    if speedcheck != 1:
        DL.SetWindowText("Red", "Buzzer FAIL")
        DL.fails=DL.fails+1
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
    
#-----------------------------------------------------------------Set to default
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# Set transaction interface = ALL
if (Result):
	DL.SetWindowText("black", "*** Set transaction interface = ALL")
	DL.SendIOCommand("IDG", "04 00 DF EF 37 01 07", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(2)

#-----------------------------------------------------------------
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )