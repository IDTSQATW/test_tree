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

##### disable DFEF61
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(6)
    
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C (disable DFEF61 error report)")
	DL.SendIOCommand("IDG", "60 06 08 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 DFEF65 01 00", 3000, 1) 
	Result = DL.Check_RXResponse("60 00 00 00")	
    
if (Result):
	time.sleep(6)
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
    
if (Result): 
    DL.SetWindowText("black", "*** Fallback to MSR transaction (default: can retry ICC card 3 times)")
    DL.SetWindowText("black", "*** Click OK -> Insert IDT test card 3 times -> Remove card -> Swipe any card.")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if(-1 != strCardData.find('DFEF61')):
        DL.SetWindowText("red", "FAIL")
    else:
        DL.SetWindowText("blue", "PASS")
        
####### enable DFEF61
if (Result):
	DL.SetWindowText("black", "*** Poll on demand")
	DL.SendIOCommand("IDG", "01 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
	time.sleep(6)
   
if (Result):
	DL.SetWindowText("black", "*** Set CT terminal data = 5C (enable DFEF61 error report)")
	DL.SendIOCommand("IDG", "60 06 08 00 9F 33 03 60 28 C8 9F 35 01 21 9F 40 05 F0 00 F0 A0 01 DF 11 01 00 DF 26 01 01 DF 27 01 00 DF EE 1E 08 D0 9C 20 D0 C4 1E 16 00 DFEF65 01 01", 3000, 1) 
	Result = DL.Check_RXResponse("60 00 00 00")	
    
if (Result):
	time.sleep(6)
	DL.SetWindowText("black", "*** QuickChip mode (02)")
	DL.SendIOCommand("IDG", "01 01 02", 3000, 1) 
	Result = DL.Check_RXResponse("01 00 00 00")	
    
if (Result): 
    DL.SetWindowText("black", "*** Fallback to MSR transaction (default: can retry ICC card 3 times)")
    DL.SetWindowText("black", "*** Click OK -> Insert IDT test card 3 times -> Remove card -> Swipe any card.")
    strCardData = DL.ReadKeyBoardCardData(20000)
    if(-1 != strCardData.find('DFEF6102F220')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "FAIL")
    if(-1 != strCardData.find('DFEF6102F222')):
        DL.SetWindowText("blue", "PASS")
    else:
        DL.SetWindowText("red", "FAIL")