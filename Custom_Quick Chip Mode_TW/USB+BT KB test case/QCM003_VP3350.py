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

# Objective: set tag DFEF6F (output delay time) w/ data 30~36

#-----------------------------------------------------------------
# Check output interface
ointerface = DL.ShowMessageBox("Check output interface", "Do u test Bluetooth output interface?", 0)
    
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)

# Set tag DFEF6F = 31 (2000 us)
if (Result):
	DL.SetWindowText("black", "*** Character delay time = 2000 us")
	DL.SendIOCommand("IDG", "04 00 DF EF 6F 01 31", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
if (Result): 
    DL.SetWindowText("black", "*** Swipe any card")
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if ointerface == 0: #USB KB
        speedcheck = DL.ShowMessageBox("", "Data output speed correctly? (Character delay time = 2000 us)", 0)
    if ointerface == 1: #Bluetooth KB
        speedcheck = DL.ShowMessageBox("", "Data output speed correctly? (Character delay time = 2000 us)", 0)
    if speedcheck == 1:
        DL.SetWindowText("Green", "PASS")
    else:
        DL.SetWindowText("Red", "FAIL")
        DL.fails=DL.fails+1
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)

# Set tag DFEF6F = 32 (5000 us)
if (Result):
	DL.SetWindowText("black", "*** Character delay time = 5000 us")
	DL.SendIOCommand("IDG", "04 00 DF EF 6F 01 32", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
if (Result): 
    DL.SetWindowText("black", "*** Swipe any card")
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if ointerface == 0: 
        speedcheck = DL.ShowMessageBox("", "Data output speed correctly? (Character delay time = 5000 us)", 0)
    if ointerface == 1: #Bluetooth KB
        speedcheck = DL.ShowMessageBox("", "Data output speed correctly? (Character delay time = 5000 us)", 0)
    if speedcheck == 1:
        DL.SetWindowText("Green", "PASS")
    else:
        DL.SetWindowText("Red", "FAIL")
        DL.fails=DL.fails+1
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)

# Set tag DFEF6F = 33 (10000 us)
if (Result):
	DL.SetWindowText("black", "*** Character delay time = 10000 us")
	DL.SendIOCommand("IDG", "04 00 DF EF 6F 01 33", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
if (Result): 
    DL.SetWindowText("black", "*** Swipe any card")
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    strCardData = DL.ReadKeyBoardCardData(20000)
    speedcheck = DL.ShowMessageBox("", "Data output speed correctly? (Character delay time = 10000 us)", 0)
    if speedcheck == 1:
        DL.SetWindowText("Green", "PASS")
    else:
        DL.SetWindowText("Red", "FAIL")
        DL.fails=DL.fails+1
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)

# Set tag DFEF6F = 34 (20000 us)
if (Result):
	DL.SetWindowText("black", "*** Character delay time = 20000 us")
	DL.SendIOCommand("IDG", "04 00 DF EF 6F 01 34", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
if (Result): 
    DL.SetWindowText("black", "*** Swipe any card")
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    strCardData = DL.ReadKeyBoardCardData(20000)
    speedcheck = DL.ShowMessageBox("", "Data output speed correctly? (Character delay time = 20000 us)", 0)
    if speedcheck == 1:
        DL.SetWindowText("Green", "PASS")
    else:
        DL.SetWindowText("Red", "FAIL")
        DL.fails=DL.fails+1
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)

# Set tag DFEF6F = 35 (50000 us)
if (Result):
	DL.SetWindowText("black", "*** Character delay time = 50000 us")
	DL.SendIOCommand("IDG", "04 00 DF EF 6F 01 35", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
if (Result): 
    DL.SetWindowText("black", "*** Swipe any card")
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    strCardData = DL.ReadKeyBoardCardData(20000)
    speedcheck = DL.ShowMessageBox("", "Data output speed correctly? (Character delay time = 50000 us)", 0)
    if speedcheck == 1:
        DL.SetWindowText("Green", "PASS")
    else:
        DL.SetWindowText("Red", "FAIL")
        DL.fails=DL.fails+1
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)

# Set tag DFEF6F = 36 (0 us)
if (Result):
	DL.SetWindowText("black", "*** Character delay time = 0 us")
	DL.SendIOCommand("IDG", "04 00 DF EF 6F 01 36", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
if (Result): 
    DL.SetWindowText("black", "*** Swipe any card")
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if ointerface == 0:
        speedcheck = DL.ShowMessageBox("", "Data output speed correctly? (Character delay time = 0 us)", 0)
    if ointerface == 1: #Bluetooth KB
        speedcheck = DL.ShowMessageBox("", "Data output speed correctly? (Character delay time = 1000 us)", 0)
    if speedcheck == 1:
        DL.SetWindowText("Green", "PASS")
    else:
        DL.SetWindowText("Red", "FAIL")
        DL.fails=DL.fails+1
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
#-----------------------------------------------------------------
# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)

# Set tag DFEF6F = 30 (default, 1200 us)
if (Result):
	DL.SetWindowText("black", "*** Character delay time = 1200 us")
	DL.SendIOCommand("IDG", "04 00 DF EF 6F 01 30", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	

# QuickChip mode
if (Result):
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(10)
    
if (Result): 
    DL.SetWindowText("black", "*** Swipe any card")
    DL.SetWindowText("red", "/// Must remain only 1 connection w/ PC, USB or Bluetooth")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if ointerface == 0:
        speedcheck = DL.ShowMessageBox("", "Data output speed correctly? (Character delay time = 1200 us)", 0)
    if ointerface == 1: #Bluetooth KB
        speedcheck = DL.ShowMessageBox("", "Data output speed correctly? (Character delay time = 1000 us)", 0)
    if speedcheck == 1:
        DL.SetWindowText("Green", "PASS")
    else:
        DL.SetWindowText("Red", "FAIL")
        DL.fails=DL.fails+1
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
        
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )