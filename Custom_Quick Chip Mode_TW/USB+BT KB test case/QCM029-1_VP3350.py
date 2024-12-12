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
				

# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(6)

# Set tag DFED4F
if (Result):
	DL.SetWindowText("black", "*** Set tag DFED4F = $$$$$")
	DL.SendIOCommand("IDG", "04 00 DFED4F 05 2424242424", 3000, 1) 
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
    if(-1 != strCardData.find('$$$$$')):
        DL.SetWindowText("blue", "w/ $$$$$, PASS")
    else:
        DL.SetWindowText("red", "FAIL")
        DL.fails=DL.fails+1
        
    DL.SetWindowText("black", "*** Insert any card")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if(-1 != strCardData.find('$$$$$')):
        DL.SetWindowText("blue", "w/ $$$$$, PASS")
    else:
        DL.SetWindowText("red", "FAIL")
        DL.fails=DL.fails+1
        
    DL.SetWindowText("black", "*** Tap any card")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if(-1 != strCardData.find('$$$$$')):
        DL.SetWindowText("blue", "w/ $$$$$, PASS")
    else:
        DL.SetWindowText("red", "FAIL")
        DL.fails=DL.fails+1
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)

# Poll on demand
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(6)
    
# Set tag DFED4F
if (Result):
	DL.SetWindowText("black", "*** Set tag DFED4F = null")
	DL.SendIOCommand("IDG", "04 00 DFED4F 00", 3000, 1) 
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
    if(-1 != strCardData.find('$$$$$')):
        DL.SetWindowText("red", "FAIL")
        DL.fails=DL.fails+1
    else:
        DL.SetWindowText("blue", "w/o $$$$$, PASS")

    DL.SetWindowText("black", "*** Insert any card")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if(-1 != strCardData.find('$$$$$')):
        DL.SetWindowText("red", "FAIL")
        DL.fails=DL.fails+1
    else:
        DL.SetWindowText("blue", "w/o $$$$$, PASS")
        
    DL.SetWindowText("black", "*** Tap any card")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if(-1 != strCardData.find('$$$$$')):
        DL.SetWindowText("red", "FAIL")
        DL.fails=DL.fails+1
    else:
        DL.SetWindowText("blue", "w/o $$$$$, PASS")
    DL.ShowMessageBox("Connection check", "Reader connect w/ PC via USB cable and then click OK", 0)
        
if(0 < (DL.fails + DL.warnings)):
	DL.setText("RED", "[Test Result] - Fail\r\n Warning:" +str(DL.warnings)+"\r\n Fail:" + str(DL.fails))
else:
	DL.setText("GREEN", "[Test Result] - PASS\r\n Warning:0\r\n Fail:0" )
