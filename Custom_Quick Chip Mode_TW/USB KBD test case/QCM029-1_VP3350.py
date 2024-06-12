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
    
if (Result):
	DL.SetWindowText("black", "*** Set tag DFED4F = $$$$$")
	DL.SendIOCommand("IDG", "04 00 DFED4F 05 2424242424", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
    
if (Result):
	time.sleep(6)
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
    
if (Result): 
    DL.SetWindowText("black", "*** Swipe any card")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if(-1 != strCardData.find('$$$$$')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "FAIL")
        
    DL.SetWindowText("black", "*** Insert any card")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if(-1 != strCardData.find('$$$$$')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "FAIL")
        
    DL.SetWindowText("black", "*** Tap any card")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if(-1 != strCardData.find('$$$$$')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "FAIL")
        
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(6)
    
if (Result):
	DL.SetWindowText("black", "*** Set tag DFED4F = null")
	DL.SendIOCommand("IDG", "04 00 DFED4F 00", 3000, 1) 
	Result = DL.Check_RXResponse("04 00 00 00")	
    
if (Result):
	time.sleep(6)
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
    
if (Result): 
    DL.SetWindowText("black", "*** Swipe any card")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if(-1 != strCardData.find('$$$$$')):
        DL.SetWindowText("red", "FAIL")
    else:
        DL.SetWindowText("blue", "PASS")

    DL.SetWindowText("black", "*** Insert any card")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if(-1 != strCardData.find('$$$$$')):
        DL.SetWindowText("red", "FAIL")
    else:
        DL.SetWindowText("blue", "PASS")
        
    DL.SetWindowText("black", "*** Tap any card")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if(-1 != strCardData.find('$$$$$')):
        DL.SetWindowText("red", "FAIL")
    else:
        DL.SetWindowText("blue", "PASS")
