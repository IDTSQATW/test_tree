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

# Objective: Verify tag DFED0A
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# Set CT terminal data = 5C (disable DFED0A)
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C (disable DFED0A)")
	DL.SendIOCommand("IDG", "60 06 17 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 5F 36 01 02 9F 1A 02 08 40 9F 1E 08 54 65 72 6D 69 6E 61 6C 9F 15 02 12 34 9F 16 0F 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 9F 1C 08 38 37 36 35 34 33 32 31 9F 4E 22 31 30 37 32 31 20 57 61 6C 6B 65 72 20 53 74 2E 20 43 79 70 72 65 73 73 2C 20 43 41 20 2C 55 53 41 2E DF EE 15 01 01 DF EE 16 01 00 DF EE 17 01 05 DF EE 18 01 80 DF EE 1F 01 80 DF EE 1B 08 30 30 30 31 35 31 30 30 DF EE 22 03 32 3C 3C DF 10 08 65 6E 66 72 65 73 7A 68 DFED0A 01 00", 3000, 1) 
	DL.Check_RXResponse("60 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# Fallback to MSR transaction (default: can retry ICC card 3 times)
if (Result): 
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    DL.SetWindowText("black", "*** Insert IDT test card, @1st time")
    strCardData1 = DL.ReadKeyBoardCardData(10000)
    if(-1 != strCardData1.find('DFEF6102F250')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "Error code FAIL")
        DL.fails=DL.fails+1
    DL.SetWindowText("black", "*** Insert IDT test card, @2nd time")
    strCardData1 = DL.ReadKeyBoardCardData(10000)
    if(-1 != strCardData1.find('DFEF6102F250')):
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
        
    DL.SetWindowText("black", "*** Swipe any card")
    strCardData2 = DL.ReadKeyBoardCardData(10000)
    if(-1 != strCardData2.find('DFEE25')):
        DL.SetWindowText("red", "w/ DFEE25, FAIL")
        DL.fails=DL.fails+1
    else:
        DL.SetWindowText("blue", "PASS")
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# Set CT terminal data = 5C (enable DFED0A)
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C (disable DFED0A)")
	DL.SendIOCommand("IDG", "60 06 17 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 5F 36 01 02 9F 1A 02 08 40 9F 1E 08 54 65 72 6D 69 6E 61 6C 9F 15 02 12 34 9F 16 0F 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 9F 1C 08 38 37 36 35 34 33 32 31 9F 4E 22 31 30 37 32 31 20 57 61 6C 6B 65 72 20 53 74 2E 20 43 79 70 72 65 73 73 2C 20 43 41 20 2C 55 53 41 2E DF EE 15 01 01 DF EE 16 01 00 DF EE 17 01 05 DF EE 18 01 80 DF EE 1F 01 80 DF EE 1B 08 30 30 30 31 35 31 30 30 DF EE 22 03 32 3C 3C DF 10 08 65 6E 66 72 65 73 7A 68 DFED0A 01 01", 3000, 1) 
	DL.Check_RXResponse("60 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)

# Fallback to MSR transaction (default: can retry ICC card 3 times)
if (Result): 
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    DL.SetWindowText("black", "*** Insert IDT test card, @1st time")
    strCardData1 = DL.ReadKeyBoardCardData(10000)
    if(-1 != strCardData1.find('DFEF6102F250')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "Error code FAIL")
        DL.fails=DL.fails+1
    DL.SetWindowText("black", "*** Insert IDT test card, @2nd time")
    strCardData1 = DL.ReadKeyBoardCardData(10000)
    if(-1 != strCardData1.find('DFEF6102F250')):
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
        
    DL.SetWindowText("black", "*** Swipe any card")
    strCardData2 = DL.ReadKeyBoardCardData(10000)
    if(-1 != strCardData2.find('DFEE25020007')):
        if(-1 != strCardData2.find('9F390180')):
            DL.SetWindowText("blue", "9F39 PASS")
        else:
            DL.SetWindowText("red", "9F39 FAIL")
            DL.fails=DL.fails+1
    else:
        DL.SetWindowText("red", "DFEE25 FAIL")
        DL.fails=DL.fails+1
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
#-----------------------------------------------------------------
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )