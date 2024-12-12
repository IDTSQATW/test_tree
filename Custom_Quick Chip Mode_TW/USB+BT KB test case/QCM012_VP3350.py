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

# Objective: 
#[JIRA] GRN-56 >> [Quick Chip Mode] Swiped card (service code = 201) -> waited for fallback transaction timeout, reader returned timeout status but LED 3 was still ON.
#[JIRA] GRN-60 >> [Quick Chip Mode] Fallback to chip reader -> swiped IDT test card, reader can read the card.
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(6)
    
# Set CT terminal data = 5C (enable MSR fallback to CT function)
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C (enable MSR fallback to CT function)")
	DL.SendIOCommand("IDG", "60 06 09 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 DFEF62 01 01 DF EE 20 01 3C", 3000, 1) 
	Result = DL.Check_RXResponse("60 00 00 00")	
    
# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)

# Fallback to CT transaction
if (Result): 
    DL.SetWindowText("black", "*** Swipe the card that service code is 2xx or 6xx")
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    strCardData1 = DL.ReadKeyBoardCardData(10000)
    DL.SetWindowText("black", "*** Swipe any MSR card -> waited fallback timeout")
    strCardData2 = DL.ReadKeyBoardCardData(61000)
    if(-1 != strCardData2.find('DFEF61023013')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "Time-out data FAIL")
        DL.fails=DL.fails+1
        DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
        DL.SendIOCommand("IDG", "05 01", 3000, 1) 
    speedcheck = DL.ShowMessageBox("", "When fallback to chip reader, MSR reader did not work?", 0)
    if speedcheck == 1:
        DL.SetWindowText("Green", "PASS")
    else:
        DL.SetWindowText("Red", "MSR interface FAIL")
        DL.fails=DL.fails+1
#-----------------------------------------------------------------
# JIRA#GRN-515
if (Result): 
    DL.SetWindowText("black", "*** Insert any MSR only card")
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    strCardData1 = DL.ReadKeyBoardCardData(190000)
    DL.SetWindowText("black", "*** Remove the card")
    strCardData2 = DL.ReadKeyBoardCardData(4000)
    if strCardData2 != '':
        DL.SetWindowText("red", "Strange data FAIL")
        DL.fails=DL.fails+1

    # 05-01
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
    DL.SetWindowText("black", "*** Cancel the status")
    DL.SendIOCommand("IDG", "05 01", 3000, 1) 
    time.sleep(1)
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(6)
    
# Set transaction interface = CT+MSR
if (Result):
	DL.SetWindowText("black", "*** Set transaction interface = CT+MSR")
	DL.SendIOCommand("IDG", "04 00 DF EF 37 01 05", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
    
# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)

# Fallback to CT transaction
if (Result): 
    DL.SetWindowText("black", "*** Swipe the card that service code is 2xx or 6xx")
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    strCardData1 = DL.ReadKeyBoardCardData(10000)
    DL.SetWindowText("black", "*** Swipe any MSR card -> waited fallback timeout")
    strCardData2 = DL.ReadKeyBoardCardData(61000)
    if(-1 != strCardData2.find('DFEF61023013')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "Time-out data FAIL")
        DL.fails=DL.fails+1
        DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
        DL.SendIOCommand("IDG", "05 01", 3000, 1) 
    speedcheck = DL.ShowMessageBox("", "When fallback to chip reader, MSR reader did not work?", 0)
    if speedcheck == 1:
        DL.SetWindowText("Green", "PASS")
    else:
        DL.SetWindowText("Red", "MSR interface FAIL")
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
	time.sleep(10)
    
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )