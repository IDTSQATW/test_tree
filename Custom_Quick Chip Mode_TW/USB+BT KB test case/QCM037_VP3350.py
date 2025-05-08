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

# Objective: Verify tag DFEF7E
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(6)
    
# Set CT terminal data = 5C (w/ DFEF7E = 5005)
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C (w/ DFEF7E = 5005)")
	DL.SendIOCommand("IDG", "60 06 08 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 DFEF7E 02 5005", 3000, 1) 
	Result = DL.Check_RXResponse("60 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
#-----------------------------------------------------------------
# Fallback to MSR transaction (default: can retry ICC card 3 times)
if (Result): 
    DL.SetWindowText("black", "*** Insert card (P/N: 80005206-002)")
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    strCardData1 = DL.ReadKeyBoardCardData(30000)
    if(-1 != strCardData1.find('DFEF6102F221')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "Error code FAIL")
        DL.fails=DL.fails+1

    speedcheck = DL.ShowMessageBox("", "After inserted card, LED 3 was turned ON (flash status)?", 0)
    if speedcheck != 1:
        DL.SetWindowText("Red", "LED FAIL")
        DL.fails=DL.fails+1

    DL.SetWindowText("black", "*** swipe any card")
    strCardData1 = DL.ReadKeyBoardCardData(30000)
    if(-1 != strCardData1.find('DFEE25020007')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "DFEE25 FAIL")
        DL.fails=DL.fails+1
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(6)
    
# Set CT terminal data = 5C (w/ DFEF7E = 0203)
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C (w/ DFEF7E = 0203)")
	DL.SendIOCommand("IDG", "60 06 08 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 DFEF7E 02 0203", 3000, 1) 
	Result = DL.Check_RXResponse("60 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
#-----------------------------------------------------------------
# Fallback to MSR transaction (default: can retry ICC card 3 times)
if (Result): 
    DL.SetWindowText("black", "*** Insert card (P/N: 80005206-002)")
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    strCardData1 = DL.ReadKeyBoardCardData(30000)
    if(-1 != strCardData1.find('DFEE25025005')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "DFEE25 FAIL")
        DL.fails=DL.fails+1

    speedcheck = DL.ShowMessageBox("", "After inserted card, LED 3 did NOT be turned ON?", 0)
    if speedcheck != 1:
        DL.SetWindowText("Red", "LED FAIL")
        DL.fails=DL.fails+1
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(6)
    
# Set CT terminal data = 5C
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C")
	DL.SendIOCommand("IDG", "60 06 07 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00", 3000, 1) 
	Result = DL.Check_RXResponse("60 00 00 00")	
    
# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(2)

if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )