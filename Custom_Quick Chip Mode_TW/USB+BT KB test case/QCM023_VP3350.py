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

#Objective: check Cancel feature if Fallback to MSR or Fallback to CT transaction
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# Set CT terminal data = 5C (enable MSR fallback to CT function)
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C (enable MSR fallback to CT function)")
	DL.SendIOCommand("IDG", "60 06 08 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 DFEF62 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("60 00 00 00")	
    
# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
#-----------------------------------------------------------------
# Fallback to CT transaction
if (Result): 
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    DL.SetWindowText("black", "*** Swipe the card that service code is 2xx or 6xx")
    strCardData1 = DL.ReadKeyBoardCardData(20000)
    
    speedcheck = DL.ShowMessageBox("", "When fallback to chip reader, LED 4 is ON (steady status)?", 0)
    if speedcheck == 1:
        DL.SetWindowText("Green", "PASS")
    else:
        DL.SetWindowText("Red", "LED FAIL")
        DL.fails=DL.fails+1
    
    # 05-01
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
    DL.SetWindowText("black", "*** Cancel the status")
    DL.SendIOCommand("IDG", "05 01", 3000, 1) 
    Result = DL.Check_RXResponse("05 00 00 00")	
    
    speedcheck = DL.ShowMessageBox("", "LED 4 is OFF?", 0)
    if speedcheck == 1:
        DL.SetWindowText("Green", "PASS")
    else:
        DL.SetWindowText("Red", "LED FAIL")
        DL.fails=DL.fails+1

# Fallback to MSR transaction
if (Result): 
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    DL.SetWindowText("black", "*** Insert IDT test card, @1st time")
    strCardData1 = DL.ReadKeyBoardCardData(15000)
    DL.SetWindowText("black", "*** Insert IDT test card, @2nd time")
    strCardData1 = DL.ReadKeyBoardCardData(15000)
    DL.SetWindowText("black", "*** Insert IDT test card, @3rd time")
    strCardData1 = DL.ReadKeyBoardCardData(15000)
    
    speedcheck = DL.ShowMessageBox("", "When fallback to MSR reader, LED 4 is ON (flash status)?", 0)
    if speedcheck == 1:
        DL.SetWindowText("Green", "PASS")
    else:
        DL.SetWindowText("Red", "LED FAIL")
        DL.fails=DL.fails+1
    
    # 05-01
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
    DL.SetWindowText("black", "*** Cancel the status")
    DL.SendIOCommand("IDG", "05 01", 3000, 1) 
    Result = DL.Check_RXResponse("05 00 00 00")	
    
    speedcheck = DL.ShowMessageBox("", "LED 4 is OFF?", 0)
    if speedcheck == 1:
        DL.SetWindowText("Green", "PASS")
    else:
        DL.SetWindowText("Red", "LED FAIL")
        DL.fails=DL.fails+1

#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(11)
    
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
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    DL.SetWindowText("black", "*** Swipe the card that service code is 2xx or 6xx")
    strCardData1 = DL.ReadKeyBoardCardData(20000)
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    speedcheck = DL.ShowMessageBox("", "When fallback to chip reader, LED 4 is ON (steady status)?", 0)
    if speedcheck == 1:
        DL.SetWindowText("Green", "PASS")
    else:
        DL.SetWindowText("Red", "LED FAIL")
        DL.fails=DL.fails+1
    
    # 05-01
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
    DL.SetWindowText("black", "*** Cancel the status")
    DL.SendIOCommand("IDG", "05 01", 3000, 1) 
    Result = DL.Check_RXResponse("05 00 00 00")	
    
    speedcheck = DL.ShowMessageBox("", "LED 4 is OFF?", 0)
    if speedcheck == 1:
        DL.SetWindowText("Green", "PASS")
    else:
        DL.SetWindowText("Red", "LED FAIL")
        DL.fails=DL.fails+1

# Fallback to MSR transaction
if (Result): 
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    DL.SetWindowText("black", "*** Insert IDT test card, @1st time")
    strCardData1 = DL.ReadKeyBoardCardData(15000)
    DL.SetWindowText("black", "*** Insert IDT test card, @2nd time")
    strCardData1 = DL.ReadKeyBoardCardData(15000)
    DL.SetWindowText("black", "*** Insert IDT test card, @3rd time")
    strCardData1 = DL.ReadKeyBoardCardData(15000)
    
    speedcheck = DL.ShowMessageBox("", "When fallback to MSR reader, LED 4 is ON (flash status)?", 0)
    if speedcheck == 1:
        DL.SetWindowText("Green", "PASS")
    else:
        DL.SetWindowText("Red", "LED FAIL")
        DL.fails=DL.fails+1
    
    # 05-01
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
    DL.SetWindowText("black", "*** Cancel the status")
    DL.SendIOCommand("IDG", "05 01", 3000, 1) 
    Result = DL.Check_RXResponse("05 00 00 00")	
    
    speedcheck = DL.ShowMessageBox("", "LED 4 is OFF?", 0)
    if speedcheck == 1:
        DL.SetWindowText("Green", "PASS")
    else:
        DL.SetWindowText("Red", "LED FAIL")
        DL.fails=DL.fails+1
	time.sleep(0.5)

#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
# Set CT terminal data = 5C (disable MSR fallback to CT function)
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C (enable MSR fallback to CT function)")
	DL.SendIOCommand("IDG", "60 06 08 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 DFEF62 01 00", 3000, 1) 
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
	time.sleep(2)
#-----------------------------------------------------------------
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )